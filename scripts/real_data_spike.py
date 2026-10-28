"""Spike S-a-lite: run the certified paired audit on REAL public customer-support text.

Data: Banking77 (PolyAI), 13,083 real banking customer-support queries with gold intent labels.
Two model versions are trained here (classical text classifiers), with 5-fold out-of-fold predictions,
so every case is predicted by models that never saw it. The empirical population is the full set;
each audit run draws a random permutation (sampling without replacement), so the true regression is
known exactly and the audit's verdicts can be checked against it.

This is NOT a test on LLM support agents or on live tickets. It tests the statistical machinery on
real text and real disagreement structure. Run: python scripts/real_data_spike.py [--runs 200]
"""
import argparse
import csv
import json
import time
import urllib.request
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import FeatureUnion, make_pipeline
from sklearn.svm import LinearSVC

from omc.audit.paired import AuditConfig, monitor_vectorized

BASE = "https://raw.githubusercontent.com/PolyAI-LDN/task-specific-datasets/master/banking_data/"


def load(cache: Path):
    cache.mkdir(parents=True, exist_ok=True)
    rows = []
    for name in ("train", "test"):
        p = cache / f"banking_{name}.csv"
        if not p.exists():
            urllib.request.urlretrieve(BASE + f"{name}.csv", p)
        rows += list(csv.DictReader(open(p, newline="", encoding="utf-8")))
    return [r["text"] for r in rows], np.array([r["category"] for r in rows])


def oof_predictions(make_model, X, y, train_frac=1.0, seed=0):
    pred = np.empty(len(y), dtype=object)
    rng = np.random.default_rng(seed)
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=seed).split(X, y):
        if train_frac < 1.0:
            tr = rng.choice(tr, int(len(tr) * train_frac), replace=False)
        m = make_model()
        m.fit([X[i] for i in tr], y[tr])
        pred[te] = m.predict([X[i] for i in te])
    return pred


def word_svc(c=0.5):
    return lambda: make_pipeline(TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True), LinearSVC(C=c))


def word_char_svc():
    return lambda: make_pipeline(FeatureUnion([
        ("w", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)),
        ("c", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), sublinear_tf=True))]), LinearSVC(C=0.5))


def unigram_small():
    return lambda: make_pipeline(TfidfVectorizer(max_features=2000), LinearSVC(C=0.5))


def audit_runs(inc, cand, y, eps, runs, seed, alpha=0.05, label_rate=0.5):
    cfg = AuditConfig(epsilon=eps, alpha=alpha, label_rate=label_rate)
    L_i = (inc != y).astype(int)
    L_c = (cand != y).astype(int)
    dis = (inc != cand).astype(int)
    d_val = L_c - L_i
    rng = np.random.default_rng(seed)
    cert = rej = 0
    ns, labs = [], []
    for _ in range(runs):
        perm = rng.permutation(len(y))
        mask = (rng.random(len(y)) < label_rate).astype(int)
        ci, ri = monitor_vectorized(dis[perm], d_val[perm], mask, cfg, check_every=50)
        if ci is not None and (ri is None or ci <= ri):
            cert += 1
            ns.append(ci)
            labs.append(int((dis[perm][:ci] * mask[:ci]).sum()))
        elif ri is not None:
            rej += 1
    return {"epsilon": eps, "certified_rate": cert / runs, "rejected_rate": rej / runs,
            "median_cases_to_certify": float(np.median(ns)) if ns else None,
            "median_labels_to_certify": float(np.median(labs)) if labs else None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=200)
    ap.add_argument("--cache", default="data/public")
    ap.add_argument("--out", default="out/real_data_spike.json")
    a = ap.parse_args()
    t0 = time.time()
    X, y = load(Path(a.cache))
    print(f"loaded {len(y)} real support queries, {len(set(y))} intents  ({time.time()-t0:.0f}s)")
    inc = oof_predictions(word_svc(0.5), X, y, seed=1)
    cands = {
        "near-equivalent (C 0.5 -> 0.6)": oof_predictions(word_svc(0.6), X, y, seed=1),
        "improved (word + char n-grams)": oof_predictions(word_char_svc(), X, y, seed=1),
        "regressed (2000 unigrams, 30% of training data)": oof_predictions(unigram_small(), X, y, train_frac=0.3, seed=1),
    }
    print(f"models trained ({time.time()-t0:.0f}s); incumbent accuracy {np.mean(inc == y):.4f}")
    results = []
    for name, cand in cands.items():
        delta = float(np.mean(cand != y) - np.mean(inc != y))
        rho = float(np.mean(inc != cand))
        row = {"candidate": name, "n": len(y), "incumbent_accuracy": float(np.mean(inc == y)),
               "candidate_accuracy": float(np.mean(cand == y)), "disagreement_rate": rho,
               "true_delta_error": delta, "audits": []}
        for eps in (0.01, 0.02, 0.03):
            row["audits"].append(audit_runs(inc, cand, y, eps, a.runs, seed=7))
        results.append(row)
        print(f"{name}: acc {row['candidate_accuracy']:.4f}  disagreement {rho:.4f}  true delta {delta:+.4f}")
        for au in row["audits"]:
            fc = " <- would be a FALSE certificate" if (au["certified_rate"] > 0 and delta > au["epsilon"]) else ""
            print(f"   eps {au['epsilon']:.2f}: certified {au['certified_rate']:.1%}  rejected {au['rejected_rate']:.1%}  "
                  f"median cases {au['median_cases_to_certify']}  median labels {au['median_labels_to_certify']}{fc}")
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(results, open(a.out, "w"), indent=1)
    print(f"done in {time.time()-t0:.0f}s -> {a.out}")


if __name__ == "__main__":
    main()
