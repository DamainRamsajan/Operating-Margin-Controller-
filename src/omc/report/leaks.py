"""Leak report v0 (FR2, FR3): cost per accepted outcome and wasted cost by case class.
accepted outcome = accepted == 1 and reopened == 0. Evidence grade E0 or E1: descriptive only."""
from __future__ import annotations

import csv
from collections import defaultdict


def leak_report(path) -> dict:
    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
    agg = defaultdict(lambda: {"cases": 0, "cost": 0.0, "accepted": 0, "wasted": 0.0})
    for r in rows:
        cost = float(r["cost"]); ok = r["accepted"] == "1" and r["reopened"] == "0"
        for k in (("class", r["case_class"]), ("handler", r["handled_by"]), ("all", "all")):
            a = agg[k]; a["cases"] += 1; a["cost"] += cost
            if ok: a["accepted"] += 1
            else: a["wasted"] += cost
    def fin(a):
        return {**a, "cost": round(a["cost"], 2), "wasted": round(a["wasted"], 2),
                "cost_per_accepted": round(a["cost"] / a["accepted"], 4) if a["accepted"] else None,
                "accept_rate": round(a["accepted"] / a["cases"], 4)}
    out = {"overall": fin(agg[("all", "all")]), "by_class": {}, "by_handler": {}}
    for (kind, name), a in agg.items():
        if kind == "class": out["by_class"][name] = fin(a)
        if kind == "handler": out["by_handler"][name] = fin(a)
    out["ranked_leaks"] = sorted(out["by_class"].items(), key=lambda kv: -kv[1]["wasted"])
    out["grade"] = "E0"
    return out
