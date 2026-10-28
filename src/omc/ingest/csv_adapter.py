"""CSV adapters (arc42 BB1 and BB2, read-only). Adapters map vendor exports to canonical records."""
from __future__ import annotations

import csv
import json
from pathlib import Path

from omc.canonical.models import DecisionRecord, ModelIdentity, RetirementNotice


def read_predictions(path: str | Path) -> tuple[list[str], dict[str, str]]:
    """Return (case ids in arrival order, case_id -> prediction). Columns: case_id, prediction
    and optionally ts. Order is by ts when present, otherwise file order."""
    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
    if rows and "ts" in rows[0]:
        rows.sort(key=lambda r: r["ts"])
    ids = [r["case_id"] for r in rows]
    return ids, {r["case_id"]: r["prediction"] for r in rows}


def read_gold(path: str | Path) -> dict[str, str]:
    return {r["case_id"]: r["gold"] for r in csv.DictReader(open(path, newline="", encoding="utf-8"))}


def read_decisions(path: str | Path) -> list[DecisionRecord]:
    out = []
    for r in csv.DictReader(open(path, newline="", encoding="utf-8")):
        out.append(DecisionRecord(
            case_ref=r["case_id"], ts=r["ts"], workflow_id=r["workflow"],
            model=ModelIdentity(r["provider"], r["model"], r["version"])))
    return out


def read_retirements(path: str | Path) -> list[RetirementNotice]:
    data = json.load(open(path, encoding="utf-8"))
    return [RetirementNotice(ModelIdentity(d["provider"], d["model"], d["version"]),
                             d["retirement_date"], d.get("source", "")) for d in data]
