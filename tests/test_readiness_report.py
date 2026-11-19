import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("readiness_report", ROOT / "scripts" / "readiness_report.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_checklist_is_well_formed_and_honest():
    rows = mod.load(ROOT / "docs" / "production" / "READINESS-CHECKLIST.csv")
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)) > 60
    assert {r["status"] for r in rows} <= {"done", "partial", "not_started"} and {r["priority"] for r in rows} <= {"P0", "P1", "P2"}
    s = mod.summarize(rows)
    assert s["gate_p_ready"] is False            # we are not pilot-ready, and the report must say so
    assert 0 < s["p0_weighted"] < 1


def test_done_items_point_to_evidence():
    rows = mod.load(ROOT / "docs" / "production" / "READINESS-CHECKLIST.csv")
    for r in rows:
        if r["status"] == "done":
            assert r["evidence"], f"{r['id']} is marked done without evidence"
