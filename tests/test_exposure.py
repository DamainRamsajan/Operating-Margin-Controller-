from datetime import date

from omc.canonical.models import DecisionRecord, ModelIdentity, RetirementNotice
from omc.exposure.inventory import build_inventory


def _d(i, v):
    return DecisionRecord(f"c{i}", f"2026-10-0{1 + i % 5}T00:00:00", "chat", ModelIdentity("p", "m", v))


def test_status_and_days_remaining():
    ds = [_d(i, "1") for i in range(8)] + [_d(i + 8, "2") for i in range(2)]
    notices = [RetirementNotice(ModelIdentity("p", "m", "1"), "2026-12-15"),
               RetirementNotice(ModelIdentity("p", "m", "2"), "2027-09-01")]
    rows = build_inventory(ds, notices, date(2026, 10, 27))
    assert rows[0]["version"] == "1" and rows[0]["status"] == "critical" and rows[0]["days_remaining"] == 49
    assert abs(rows[0]["share"] - 0.8) < 1e-9 and rows[1]["status"] == "ok"


def test_unknown_retirement_is_flagged():
    rows = build_inventory([_d(0, "9")], [], date(2026, 10, 27))
    assert rows[0]["status"] == "no-date"
