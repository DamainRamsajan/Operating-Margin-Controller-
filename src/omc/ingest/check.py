"""Data readiness checks. Output contains only aggregate counts, never raw rows, so a summary can be
shared safely (DATA-REQUEST.md)."""
from __future__ import annotations

import csv
import hashlib
import hmac
from collections import Counter
from pathlib import Path


def _rows(path):
    return list(csv.DictReader(open(path, newline="", encoding="utf-8")))


def check_predictions(path, name):
    issues, rows = [], _rows(path)
    cols = set(rows[0].keys()) if rows else set()
    for need in ("case_id", "prediction"):
        if need not in cols:
            issues.append(f"{name}: missing column {need}")
    if issues:
        return {"file": name, "rows": len(rows), "issues": issues}
    ids = [r["case_id"] for r in rows]
    dup = len(ids) - len(set(ids))
    empty = sum(1 for r in rows if not r["prediction"].strip())
    if dup:
        issues.append(f"{name}: {dup} duplicate case_id values")
    if empty:
        issues.append(f"{name}: {empty} empty predictions")
    if "ts" not in cols:
        issues.append(f"{name}: no ts column; file order will be used as arrival order")
    classes = Counter(r["prediction"] for r in rows)
    return {"file": name, "rows": len(rows), "distinct_predictions": len(classes),
            "top_share": round(classes.most_common(1)[0][1] / max(len(rows), 1), 4), "issues": issues}


def check_gate_inputs(incumbent, candidate, labels=None):
    a, b = check_predictions(incumbent, "incumbent"), check_predictions(candidate, "candidate")
    out = {"incumbent": a, "candidate": b, "issues": a["issues"] + b["issues"]}
    if not out["issues"] or all("no ts column" in i for i in out["issues"]):
        ia = {r["case_id"]: r["prediction"] for r in _rows(incumbent)}
        ib = {r["case_id"]: r["prediction"] for r in _rows(candidate)}
        common = set(ia) & set(ib)
        out["cases_in_both"] = len(common)
        out["disagreement_rate"] = round(sum(ia[c] != ib[c] for c in common) / max(len(common), 1), 6)
        if len(common) != len(ia) or len(common) != len(ib):
            out["issues"].append("incumbent and candidate cover different case ids")
        if labels:
            g = {r["case_id"]: r["gold"] for r in _rows(labels)}
            dis = [c for c in common if ia[c] != ib[c]]
            out["gold_coverage_all"] = round(len(set(g) & common) / max(len(common), 1), 4)
            out["gold_coverage_on_disagreements"] = round(len(set(g) & set(dis)) / max(len(dis), 1), 4)
            out["incumbent_accuracy_on_labeled"] = round(sum(ia[c] == g[c] for c in g if c in ia) / max(len(set(g) & set(ia)), 1), 4)
            out["candidate_accuracy_on_labeled"] = round(sum(ib[c] == g[c] for c in g if c in ib) / max(len(set(g) & set(ib)), 1), 4)
    return out


def pseudonymize_column(src, dst, column, secret: bytes):
    """Replace an id column with a keyed hash (HMAC-SHA256, 16 hex chars). Keep the secret private."""
    rows = _rows(src)
    if not rows or column not in rows[0]:
        raise ValueError(f"column {column} not found")
    for r in rows:
        r[column] = hmac.new(secret, r[column].encode(), hashlib.sha256).hexdigest()[:16]
    with open(dst, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return len(rows)


def safe_path(p):
    return str(Path(p))
