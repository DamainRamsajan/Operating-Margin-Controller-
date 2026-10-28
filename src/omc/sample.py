"""Synthetic sample data for demos and tests. All names, dates and values are fictional."""
from __future__ import annotations

import csv
import json
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

CLASSES = ["billing", "shipping", "refund", "account", "technical"]
SCENARIOS = {  # d = disagreement rate, p_inc_only, p_cand_only (true Delta = d * (p_inc_only - p_cand_only))
    "benign": (0.004, 0.40, 0.40),
    "regression": (0.060, 0.70, 0.15),
    "unclear": (0.030, 0.45, 0.35),
}


def _wrong(rng, y):
    return rng.choice([c for c in CLASSES if c != y])


def make_scenario(out_dir, scenario: str, n: int = 30000, seed: int = 7) -> dict:
    d, p_inc, p_cand = SCENARIOS[scenario]
    rng = np.random.default_rng(seed)
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    t0 = datetime(2026, 9, 1)
    inc_rows, cand_rows, gold_rows = [], [], []
    for i in range(n):
        cid, ts = f"c{i:06d}", (t0 + timedelta(seconds=30 * i)).isoformat()
        y = rng.choice(CLASSES)
        if rng.random() < d:
            u = rng.random()
            if u < p_inc:            # incumbent alone right
                pi, pc = y, _wrong(rng, y)
            elif u < p_inc + p_cand:  # candidate alone right
                pi, pc = _wrong(rng, y), y
            else:                    # both wrong, different answers
                w1 = _wrong(rng, y); pi, pc = w1, rng.choice([c for c in CLASSES if c not in (y, w1)])
        else:
            pi = pc = y if rng.random() < 0.9 else _wrong(rng, y)
        inc_rows.append((cid, ts, pi)); cand_rows.append((cid, ts, pc)); gold_rows.append((cid, y))
    for name, rows, hdr in (("incumbent.csv", inc_rows, ["case_id", "ts", "prediction"]),
                            ("candidate.csv", cand_rows, ["case_id", "ts", "prediction"]),
                            ("gold.csv", gold_rows, ["case_id", "gold"])):
        with open(out / name, "w", newline="") as f:
            w = csv.writer(f); w.writerow(hdr); w.writerows(rows)
    return {"scenario": scenario, "true_delta": d * (p_inc - p_cand), "n": n}


def make_ops_data(out_dir, seed: int = 11):
    rng = np.random.default_rng(seed)
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    t0 = datetime(2026, 8, 1)
    models = [("acme", "llm-small", "1.0", 0.55), ("acme", "llm-large", "2.1", 0.30), ("zeta", "chat-pro", "5", 0.15)]
    with open(out / "decisions.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["case_id", "ts", "workflow", "provider", "model", "version"])
        for i in range(5000):
            m = models[rng.choice(len(models), p=[x[3] for x in models])]
            w.writerow([f"d{i:05d}", (t0 + timedelta(minutes=10 * i)).isoformat(),
                        rng.choice(["support_chat", "support_email"], p=[0.7, 0.3]), m[0], m[1], m[2]])
    json.dump([
        {"provider": "acme", "model": "llm-small", "version": "1.0", "retirement_date": "2026-12-15", "source": "fictional notice A"},
        {"provider": "acme", "model": "llm-large", "version": "2.1", "retirement_date": "2027-02-20", "source": "fictional notice B"},
        {"provider": "zeta", "model": "chat-pro", "version": "5", "retirement_date": "2027-09-30", "source": "fictional notice C"},
    ], open(out / "deprecations.json", "w"), indent=2)
    with open(out / "tickets.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["case_id", "case_class", "handled_by", "cost", "accepted", "reopened"])
        for i in range(3000):
            ai = rng.random() < 0.6
            w.writerow([f"t{i:05d}", rng.choice(CLASSES), "ai" if ai else "human",
                        round(float(rng.uniform(0.4, 0.9) if ai else rng.uniform(4, 9)), 2),
                        int(rng.random() < (0.72 if ai else 0.95)), int(rng.random() < (0.09 if ai else 0.03))])
    (out / "transcripts.txt").write_text(
        "Hi, my email is jane.doe@example.com and my card 4111 1111 1111 1111 was charged twice.\n"
        "Call me on +1 415 555 0132 or write to ops@example.org. SSN 123-45-6789 is on the form.\n"
        "Please refund to IBAN DE89 3704 0044 0532 0130 00. My IP is 192.168.1.20.\n"
        "No personal data in this line, just a question about shipping times.\n")
    json.dump({"trains_on_data": False, "retention_days": 0, "region": "eu"}, open(out / "provider_terms_ok.json", "w"))
    json.dump({"trains_on_data": True, "retention_days": 30, "region": "us"}, open(out / "provider_terms_bad.json", "w"))
    json.dump({"allow_training": False, "max_retention_days": 0, "allowed_regions": ["eu"]}, open(out / "provider_policy.json", "w"))
