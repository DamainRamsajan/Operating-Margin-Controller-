"""Weekly pipeline summary from launch/pipeline.csv.
stages: target, contacted, replied, call, qualified, design_partner, pilot, paid, lost
Usage: python scripts/pipeline_report.py launch/pipeline.csv [--today YYYY-MM-DD]"""
import argparse
import csv
from collections import Counter
from datetime import date

STAGES = ["target", "contacted", "replied", "call", "qualified", "design_partner", "pilot", "paid"]


def report(path, today: date) -> dict:
    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
    stage = Counter(r["stage"] for r in rows)
    reached = {s: sum(stage[t] for t in STAGES[STAGES.index(s):]) for s in STAGES}
    def rate(a, b):
        return round(reached[b] / reached[a], 3) if reached[a] else None
    overdue = [r["org"] for r in rows if r["stage"] not in ("lost", "paid") and r["next_date"] and date.fromisoformat(r["next_date"]) < today]
    return {"total": len(rows), "by_stage": dict(stage), "reached": reached,
            "reply_rate": rate("contacted", "replied"), "call_rate": rate("replied", "call"),
            "partner_rate": rate("call", "design_partner"), "overdue_next_steps": overdue}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--today", default=date.today().isoformat())
    a = ap.parse_args()
    r = report(a.path, date.fromisoformat(a.today))
    print(f"organizations: {r['total']}")
    for s in STAGES:
        print(f"  reached {s:<15} {r['reached'][s]}")
    print(f"reply rate {r['reply_rate']}  call rate {r['call_rate']}  design-partner rate {r['partner_rate']}")
    print("overdue next steps:", ", ".join(r["overdue_next_steps"]) or "none")


if __name__ == "__main__":
    main()
