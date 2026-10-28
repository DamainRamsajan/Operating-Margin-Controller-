"""Model-exposure inventory and retirement calendar (FR14, arc42 BB15 Exposure Inventory)."""
from __future__ import annotations

from collections import defaultdict
from datetime import date

from omc.canonical.models import DecisionRecord, RetirementNotice


def build_inventory(decisions: list[DecisionRecord], notices: list[RetirementNotice],
                    as_of: date, critical_days: int = 60, warning_days: int = 120) -> list[dict]:
    by_model: dict[str, dict] = defaultdict(lambda: {"decisions": 0, "workflows": set(),
                                                     "first": None, "last": None, "id": None})
    for d in decisions:
        e = by_model[d.model.key()]
        e["id"] = d.model
        e["decisions"] += 1
        e["workflows"].add(d.workflow_id)
        e["first"] = d.ts if e["first"] is None or d.ts < e["first"] else e["first"]
        e["last"] = d.ts if e["last"] is None or d.ts > e["last"] else e["last"]
    retire = {n.model.key(): n for n in notices}
    total = sum(e["decisions"] for e in by_model.values()) or 1
    rows = []
    for key, e in by_model.items():
        notice = retire.get(key)
        days = None
        status = "no-date"
        if notice:
            days = (date.fromisoformat(notice.retirement_date) - as_of).days
            status = ("retired" if days < 0 else "critical" if days <= critical_days
                      else "warning" if days <= warning_days else "ok")
        rows.append({
            "provider": e["id"].provider, "model": e["id"].model, "version": e["id"].version,
            "decisions": e["decisions"], "share": round(e["decisions"] / total, 6),
            "workflows": sorted(e["workflows"]), "first_seen": e["first"], "last_seen": e["last"],
            "retirement_date": notice.retirement_date if notice else None,
            "days_remaining": days, "status": status,
            "source": notice.source if notice else None,
        })
    order = {"retired": 0, "critical": 1, "warning": 2, "ok": 3, "no-date": 4}
    rows.sort(key=lambda r: (order[r["status"]], r["days_remaining"] if r["days_remaining"] is not None else 10**9, -r["decisions"]))
    return rows


def to_markdown(rows: list[dict], as_of: date) -> str:
    out = [f"# Model exposure inventory (as of {as_of.isoformat()})", "",
           "| Model | Decisions | Share | Workflows | Retires | Days left | Status |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        out.append(f"| {r['provider']}/{r['model']}@{r['version']} | {r['decisions']} | {r['share']:.1%} | "
                   f"{', '.join(r['workflows'])} | {r['retirement_date'] or 'unknown'} | "
                   f"{'' if r['days_remaining'] is None else r['days_remaining']} | {r['status']} |")
    return "\n".join(out) + "\n"
