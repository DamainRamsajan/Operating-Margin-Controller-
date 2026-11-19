"""CI promotion gate (FR26, arc42 6.18): runs the certified paired audit and returns a signed verdict."""
from __future__ import annotations

import hashlib
from pathlib import Path

from omc.audit.paired import AuditConfig, run_audit
from omc.ingest.csv_adapter import read_gold, read_predictions
from omc.vault import chain
from omc.vault.statement import dec, load_private_key, now_iso, sign_statement

EXIT = {"promote": 0, "hold": 10, "reject": 20}
ASSUMPTIONS = [
    "cases are i.i.d. from a stationary stream over the audit window",
    "loss is 0-1 against a gold label and is determined by the decision",
    "label selection is a hash threshold that never reads the gold label",
]


def _sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run_gate(incumbent, candidate, labels, key, out_dir, *, epsilon=0.01, alpha=0.05, label_rate=0.5,
             workflow="support", incumbent_name="incumbent", candidate_name="candidate",
             issuer="omc-dev", issued_at=None) -> tuple[int, dict]:
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    ids, inc = read_predictions(incumbent)
    cand_ids, cand = read_predictions(candidate)
    if set(ids) != set(cand_ids):
        raise ValueError("incumbent and candidate must cover the same case ids")
    gold = read_gold(labels) if labels else {}
    cfg = AuditConfig(epsilon=epsilon, alpha=alpha, label_rate=label_rate)
    res = run_audit(ids, inc, cand, gold, cfg)
    from omc.audit.stationarity import check as stationarity_check
    stat = stationarity_check([int(inc[c] != cand[c]) for c in ids])
    grade = "E1" if res.verdict == "hold" else "E3"
    payload = {
        "schema": "omc.evidence.v0", "type": "model-promotion-verdict",
        "subject": {"workflow": workflow, "incumbent": incumbent_name, "candidate": candidate_name},
        "verdict": res.verdict, "tier": res.tier, "reason": res.reason, "grade": grade,
        "tolerance": dec(epsilon), "alpha": dec(alpha),
        "n_cases": res.n_cases, "n_disagree": res.n_disagree, "n_labeled": res.n_labeled,
        "stopping_index": res.stopping_index,
        "rho_ub": dec(res.rho_ub), "rho_lb": dec(res.rho_lb),
        "delta_ub": dec(res.delta_ub), "delta_lb": dec(res.delta_lb),
        "label_routing": {"rule": "sha256-threshold", "salt": cfg.salt, "rate": dec(label_rate)},
        "inputs": {"incumbent_sha256": _sha(incumbent), "candidate_sha256": _sha(candidate),
                   "labels_sha256": _sha(labels) if labels else None},
        "estimator": {"name": "omc.audit.paired", "version": "0.1.0"},
        "stationarity": {"first_half_rate": dec(stat["first_half_rate"]), "second_half_rate": dec(stat["second_half_rate"]),
                         "p_value": dec(stat["p_value"]), "warning": stat["warning"]},
        "assumptions": ASSUMPTIONS, "issued_at": issued_at or now_iso(),
    }
    priv = load_private_key(key)
    cose = sign_statement(payload, priv, issuer, f"{workflow}:{candidate_name}")
    (out / "verdict.cose").write_bytes(cose)
    from omc.vault.statement import canonical_json
    (out / "verdict.json").write_bytes(canonical_json(payload))
    (out / "label_requests.txt").write_text("\n".join(res.labels_requested))
    chain.append(out / "chain.jsonl", cose)
    from omc.render import to_markdown
    (out / "verdict.md").write_text(to_markdown(payload))
    _write_console_artifacts(out, ids, inc, cand, gold, cfg, res)
    return EXIT[res.verdict], payload



def _write_console_artifacts(out: Path, ids, inc, cand, gold, cfg, res) -> None:
    """Files the console reads: evidence trajectory and a blinded review queue (no model identity)."""
    import csv
    import json

    import numpy as np

    from omc.audit.paired import selected_for_label, trajectory
    stop = res.stopping_index + 1 if res.stopping_index is not None else len(ids)
    use = ids[:stop]
    dis = np.array([int(inc[c] != cand[c]) for c in use])
    mask = np.array([int(selected_for_label(c, cfg.salt, cfg.label_rate) and c in gold and inc[c] != cand[c]) for c in use])
    dval = np.array([((int(cand[c] != gold[c]) - int(inc[c] != gold[c])) if c in gold else 0) for c in use])
    step = max(50, stop // 60)
    tr = trajectory(dis, dval, mask, cfg, check_every=step)
    pts = [{"n": int(n), "ub": round(float(u) * 1000, 3), "lb": round(float(lo) * 1000, 3), "m": int(m)}
           for n, u, lo, m in zip(tr["n"], tr["delta_ub"], tr["delta_lb"], tr["m"])]
    json.dump({"epsilon_per_1000": cfg.epsilon * 1000, "points": pts}, open(out / "trajectory.json", "w"))
    with open(out / "review_queue.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["case_id", "option_1", "option_2"])
        for cid in res.labels_requested:
            a, b = inc[cid], cand[cid]
            flip = int(hashlib.sha256(("order:" + cid).encode()).hexdigest(), 16) % 2 == 1
            w.writerow([cid, b if flip else a, a if flip else b])
