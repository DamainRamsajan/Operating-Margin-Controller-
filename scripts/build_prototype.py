"""Build ui/prototype/index.html: a clickable, self-contained UX prototype using REAL audit trajectories
from the synthetic scenarios (the rest is labeled demo data). Run: python scripts/build_prototype.py"""
import json
import tempfile
from pathlib import Path

import numpy as np

from omc.audit.gate import run_gate
from omc.audit.paired import AuditConfig, selected_for_label, trajectory
from omc.ingest.csv_adapter import read_gold, read_predictions
from omc.render import headline, to_markdown
from omc.sample import make_scenario
from omc.vault.statement import generate_keypair

ROOT = Path(__file__).resolve().parents[1]


def scenario_data(name, workdir, key):
    d = workdir / name
    make_scenario(d, name, n=30000)
    ids, inc = read_predictions(d / "incumbent.csv")
    _, cand = read_predictions(d / "candidate.csv")
    gold = read_gold(d / "gold.csv")
    cfg = AuditConfig(epsilon=0.01, alpha=0.05, label_rate=0.5)
    dis = np.array([int(inc[c] != cand[c]) for c in ids])
    dval = np.array([(int(cand[c] != gold[c]) - int(inc[c] != gold[c])) for c in ids])
    mask = np.array([int(selected_for_label(c, cfg.salt, cfg.label_rate)) for c in ids])
    tr = trajectory(dis, dval, mask, cfg, check_every=250)
    code, payload = run_gate(d / "incumbent.csv", d / "candidate.csv", d / "gold.csv", key, workdir / ("gate_" + name),
                             incumbent_name="model-a", candidate_name=f"model-b ({name})", issued_at="2026-10-28T00:00:00Z")
    word, sentence = headline(payload)
    pts = [{"n": int(n), "ub": round(float(u) * 1000, 2), "lb": round(float(lo) * 1000, 2), "m": int(m)}
           for n, u, lo, m in zip(tr["n"], tr["delta_ub"], tr["delta_lb"], tr["m"])]
    return {"payload": payload, "word": word, "sentence": sentence, "markdown": to_markdown(payload),
            "points": pts, "exit": code}


def main():
    with tempfile.TemporaryDirectory() as td:
        wd = Path(td)
        priv, _ = generate_keypair(wd / "k")
        data = {"scenarios": {s: scenario_data(s, wd, priv) for s in ("benign", "regression", "unclear")}}
    html = (ROOT / "ui" / "prototype" / "template.html").read_text().replace("/*DATA*/null", json.dumps(data))
    (ROOT / "ui" / "prototype" / "index.html").write_text(html)
    print("wrote ui/prototype/index.html", {k: v["word"] for k, v in data["scenarios"].items()})


if __name__ == "__main__":
    main()
