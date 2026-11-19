"""Build a demo workspace for the console: keys, three labeled runs, one run waiting for labels, exposure, readiness."""
from __future__ import annotations

import json
import tempfile
from datetime import date
from pathlib import Path

from omc.audit.gate import run_gate
from omc.exposure.inventory import build_inventory
from omc.ingest.check import check_gate_inputs
from omc.ingest.csv_adapter import read_decisions, read_retirements
from omc.sample import make_ops_data, make_scenario
from omc.vault.statement import generate_keypair


def build_workspace(ws, n: int = 30000) -> Path:
    ws = Path(ws)
    (ws / "gates").mkdir(parents=True, exist_ok=True)
    priv, _ = generate_keypair(ws / "keys")
    with tempfile.TemporaryDirectory() as td:
        data = Path(td)
        for sc, name in (("benign", "benign-update"), ("regression", "clear-regression"), ("unclear", "borderline")):
            make_scenario(data / sc, sc, n=n)
            d = data / sc
            run_gate(d / "incumbent.csv", d / "candidate.csv", d / "gold.csv", priv, ws / "gates" / name,
                     incumbent_name="model-a", candidate_name=f"model-b ({sc})", issued_at="2026-10-28T00:00:00Z")
        d = data / "unclear"          # the same traffic with no labels yet: the review queue fills up
        run_gate(d / "incumbent.csv", d / "candidate.csv", None, priv, ws / "gates" / "borderline-needs-labels",
                 incumbent_name="model-a", candidate_name="model-b (needs labels)", issued_at="2026-10-28T00:00:00Z")
        report = check_gate_inputs(d / "incumbent.csv", d / "candidate.csv", d / "gold.csv")
        (ws / "readiness.json").write_text(json.dumps(report, indent=2))
        make_ops_data(data / "ops")
        rows = build_inventory(read_decisions(data / "ops" / "decisions.csv"), read_retirements(data / "ops" / "deprecations.json"), date(2026, 10, 27))
        (ws / "exposure.json").write_text(json.dumps(rows, indent=2))
    return ws
