"""Progress report from docs/production/READINESS-CHECKLIST.csv.
Usage: python scripts/readiness_report.py [path]   (statuses: done, partial, not_started)"""
import argparse
import csv
from collections import Counter, defaultdict

SCORE = {"done": 1.0, "partial": 0.5, "not_started": 0.0}


def load(path):
    return list(csv.DictReader(open(path, newline="", encoding="utf-8")))


def summarize(rows):
    by_ws = defaultdict(Counter)
    for r in rows:
        by_ws[r["workstream"]][r["status"]] += 1
    p0 = [r for r in rows if r["priority"] == "P0"]
    p0_score = sum(SCORE[r["status"]] for r in p0) / len(p0) if p0 else 1.0
    return {"total": len(rows), "p0_total": len(p0), "p0_done": sum(1 for r in p0 if r["status"] == "done"),
            "p0_weighted": round(p0_score, 3), "by_workstream": {k: dict(v) for k, v in sorted(by_ws.items())},
            "p0_open": [(r["id"], r["status"], r["owner"], r["item"]) for r in p0 if r["status"] != "done"],
            "gate_p_ready": all(r["status"] == "done" for r in p0)}


def render(s):
    lines = [f"Items: {s['total']}   P0: {s['p0_done']}/{s['p0_total']} done   weighted P0 progress: {s['p0_weighted']:.0%}   Gate P ready: {s['gate_p_ready']}", "",
             f"{'Workstream':<11}{'done':>6}{'partial':>9}{'not started':>13}"]
    for ws, c in s["by_workstream"].items():
        lines.append(f"{ws:<11}{c.get('done', 0):>6}{c.get('partial', 0):>9}{c.get('not_started', 0):>13}")
    lines += ["", "Open P0 items:"] + [f"  {i} [{st}] ({owner}) {item}" for i, st, owner, item in s["p0_open"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", default="docs/production/READINESS-CHECKLIST.csv")
    print(render(summarize(load(ap.parse_args().path))))
