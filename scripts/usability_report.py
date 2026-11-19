"""Usability report from the CSVs in a results folder (see docs/ux/usability/).
Usage: python scripts/usability_report.py docs/ux/usability/results
Folder must contain participants.csv, task_results.csv, comprehension_results.csv, sus_results.csv, issues.csv
(copy the templates and fill them in). Small samples give wide intervals; the report says so."""
import argparse
import csv
import math
import random
import statistics
from collections import defaultdict
from pathlib import Path

from scipy.stats import binomtest

TARGETS = {"sus": 80.0, "task_success": 0.90, "comprehension": 0.85}


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def sus_score(answers: list[int]) -> float:
    assert len(answers) == 10
    odd = sum(a - 1 for i, a in enumerate(answers) if i % 2 == 0)
    even = sum(5 - a for i, a in enumerate(answers) if i % 2 == 1)
    return (odd + even) * 2.5


def _rows(folder: Path, name: str) -> list[dict]:
    p = folder / name
    return list(csv.DictReader(open(p, newline="", encoding="utf-8"))) if p.exists() else []


def mcnemar_exact(a: dict, b: dict) -> dict:
    """Paired comparison on per-participant correctness (1/0). a and b map participant -> correct."""
    ids = sorted(set(a) & set(b))
    only_a = sum(1 for i in ids if a[i] == 1 and b[i] == 0)
    only_b = sum(1 for i in ids if a[i] == 0 and b[i] == 1)
    n = only_a + only_b
    p = binomtest(min(only_a, only_b), n, 0.5).pvalue if n else 1.0
    return {"pairs": len(ids), "first_only_correct": only_a, "second_only_correct": only_b, "p_exact": round(p, 4)}


def bootstrap_ci(values: list[float], iters: int = 2000, seed: int = 1) -> tuple[float, float]:
    if not values:
        return (float("nan"), float("nan"))
    rng = random.Random(seed)
    means = sorted(statistics.fmean(rng.choices(values, k=len(values))) for _ in range(iters))
    return (means[int(0.025 * iters)], means[int(0.975 * iters) - 1])


def build(folder) -> dict:
    folder = Path(folder)
    parts = {r["participant_id"]: r for r in _rows(folder, "participants.csv")}
    out: dict = {"participants": len(parts)}
    tasks = defaultdict(list)
    for r in _rows(folder, "task_results.csv"):
        tasks[r["task_id"]].append(r)
    out["tasks"] = {}
    for tid, rs in sorted(tasks.items()):
        full = sum(1 for r in rs if float(r["success"]) == 1.0)
        lo, hi = wilson(full, len(rs))
        out["tasks"][tid] = {"n": len(rs), "full_success": full, "rate": full / len(rs), "ci": (round(lo, 3), round(hi, 3)),
                             "median_sec": statistics.median(float(r["time_sec"]) for r in rs),
                             "assisted": sum(int(r["assisted"]) for r in rs)}
    sus = [sus_score([int(r[f"q{i}"]) for i in range(1, 11)]) for r in _rows(folder, "sus_results.csv")]
    out["sus"] = {"n": len(sus), "mean": round(statistics.fmean(sus), 1) if sus else None,
                  "ci": tuple(round(x, 1) for x in bootstrap_ci(sus)) if sus else None}
    comp = _rows(folder, "comprehension_results.csv")
    by = defaultdict(list)
    for r in comp:
        by[r["phrasing"]].append(r)
    out["comprehension"] = {}
    for ph, rs in sorted(by.items()):
        def acc(key, rs=rs):
            vals = [r[key] for r in rs if r[key] != ""]
            k, n = sum(int(v) for v in vals), len(vals)
            lo, hi = wilson(k, n)
            return {"k": k, "n": n, "rate": round(k / n, 3) if n else None, "ci": (round(lo, 3), round(hi, 3))}
        out["comprehension"][ph] = {"q1": acc("q1_correct"), "q2": acc("q2_correct"), "q3": acc("q3_correct"),
                                    "q4_mean": round(statistics.fmean(float(r["q4_confidence"]) for r in rs), 2),
                                    "median_sec": statistics.median(float(r["seconds"]) for r in rs)}
    out["paired"] = {}
    for q in ("q1_correct", "q3_correct"):
        per = {ph: {r["participant_id"]: int(r[q]) for r in rs if r[q] != ""} for ph, rs in by.items()}
        for x, y in (("A", "B"), ("A", "C"), ("B", "C")):
            if x in per and y in per:
                out["paired"][f"{q}:{x} vs {y}"] = mcnemar_exact(per[x], per[y])
    issues = _rows(folder, "issues.csv")
    out["issues"] = {"count": len(issues), "by_severity": {s: sum(1 for r in issues if r["severity"] == s) for s in "1234"},
                     "top": sorted(issues, key=lambda r: -int(r["severity"]))[:5]}
    return out


def render(rep: dict) -> str:
    L = [f"# Usability report ({rep['participants']} participants)", "", "## Tasks", "| Task | n | Full success | 95% Wilson | Median sec | Assisted |", "|---|---|---|---|---|---|"]
    for tid, t in rep["tasks"].items():
        L.append(f"| {tid} | {t['n']} | {t['rate']:.0%} | {t['ci'][0]:.0%} to {t['ci'][1]:.0%} | {t['median_sec']:.0f} | {t['assisted']} |")
    s = rep["sus"]
    L += ["", "## SUS", f"n = {s['n']}" + (f", mean {s['mean']} (95% bootstrap {s['ci'][0]} to {s['ci'][1]}); target {TARGETS['sus']:.0f}" if s["n"] else ""), "",
          "## Comprehension by phrasing", "| Phrasing | Q1 correct | Q2 correct | Q3 correct | Q4 mean | Median sec |", "|---|---|---|---|---|---|"]
    for ph, c in rep["comprehension"].items():
        f = lambda a: f"{a['k']}/{a['n']} ({a['ci'][0]:.0%} to {a['ci'][1]:.0%})"  # noqa: E731
        L.append(f"| {ph} | {f(c['q1'])} | {f(c['q2'])} | {f(c['q3'])} | {c['q4_mean']} | {c['median_sec']:.0f} |")
    L += ["", "Paired exact tests (participants who got both phrasings):"]
    for k, v in rep["paired"].items():
        L.append(f"- {k}: first-only correct {v['first_only_correct']}, second-only correct {v['second_only_correct']}, p = {v['p_exact']} ({v['pairs']} pairs)")
    iss = rep["issues"]
    L += ["", "## Issues", f"{iss['count']} logged; by severity 1 to 4: " + ", ".join(f"{k}: {v}" for k, v in iss["by_severity"].items()), "",
          "Reminder: with fewer than 30 participants, treat rates as directional (README, decision rules)."]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    print(render(build(ap.parse_args().folder)))


if __name__ == "__main__":
    main()
