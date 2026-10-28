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
        "assumptions": ASSUMPTIONS, "issued_at": issued_at or now_iso(),
    }
    priv = load_private_key(key)
    cose = sign_statement(payload, priv, issuer, f"{workflow}:{candidate_name}")
    (out / "verdict.cose").write_bytes(cose)
    from omc.vault.statement import canonical_json
    (out / "verdict.json").write_bytes(canonical_json(payload))
    (out / "label_requests.txt").write_text("\n".join(res.labels_requested))
    chain.append(out / "chain.jsonl", cose)
    return EXIT[res.verdict], payload
