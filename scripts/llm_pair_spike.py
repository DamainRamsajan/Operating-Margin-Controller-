"""Spike S-a with real LLMs on public data (UNTESTED here: needs your API keys and network).

Classifies Banking77 queries with two model versions, writes incumbent.csv, candidate.csv and gold.csv,
then you run `omc gate`. Start with --n 20 to check the plumbing and cost.
  export ANTHROPIC_API_KEY=...   (or OPENAI_API_KEY=...)
  python scripts/llm_pair_spike.py --provider anthropic --incumbent-model MODEL_A --candidate-model MODEL_B --n 2000
Model names are whatever your account offers; nothing is hard-coded. Costs are yours: 2 calls per case.
"""
import argparse
import csv
import json
import os
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

BASE = "https://raw.githubusercontent.com/PolyAI-LDN/task-specific-datasets/master/banking_data/"


def load_rows(cache):
    cache.mkdir(parents=True, exist_ok=True)
    p = cache / "banking_test.csv"
    if not p.exists():
        urllib.request.urlretrieve(BASE + "test.csv", p)
    return list(csv.DictReader(open(p, newline="", encoding="utf-8")))


def normalize(answer: str, labels: list[str]) -> str:
    """Map a model answer to one of the allowed labels, else INVALID."""
    a = answer.strip().lower().replace(" ", "_").strip("`'\".,")
    return a if a in labels else "INVALID"


def prompt(text, labels):
    return ("Classify this customer message into exactly one intent. Answer with the intent name only.\n"
            f"Allowed intents: {', '.join(labels)}\n\nMessage: {text}\nIntent:")


def call(provider, model, content, retries=4):
    for k in range(retries):
        try:
            if provider == "anthropic":
                body = {"model": model, "max_tokens": 20, "messages": [{"role": "user", "content": content}]}
                req = urllib.request.Request("https://api.anthropic.com/v1/messages", json.dumps(body).encode(), {
                    "x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01", "content-type": "application/json"})
                return json.load(urllib.request.urlopen(req, timeout=60))["content"][0]["text"]
            body = {"model": model, "max_tokens": 20, "temperature": 0, "messages": [{"role": "user", "content": content}]}
            req = urllib.request.Request("https://api.openai.com/v1/chat/completions", json.dumps(body).encode(), {
                "Authorization": "Bearer " + os.environ["OPENAI_API_KEY"], "content-type": "application/json"})
            return json.load(urllib.request.urlopen(req, timeout=60))["choices"][0]["message"]["content"]
        except Exception:
            time.sleep(2 ** k)
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", choices=["anthropic", "openai"], required=True)
    ap.add_argument("--incumbent-model", required=True)
    ap.add_argument("--candidate-model", required=True)
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--out-dir", default="data/llm_pair")
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()
    rows = load_rows(Path("data/public"))[: a.n]
    labels = sorted({r["category"] for r in rows} | {r["category"] for r in load_rows(Path("data/public"))})
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    def one(r):
        c = prompt(r["text"], labels)
        return (normalize(call(a.provider, a.incumbent_model, c), labels), normalize(call(a.provider, a.candidate_model, c), labels))

    with ThreadPoolExecutor(a.workers) as ex:
        preds = list(ex.map(one, rows))
    for name, idx in (("incumbent.csv", 0), ("candidate.csv", 1)):
        with open(out / name, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["case_id", "ts", "prediction"])
            for i, p in enumerate(preds):
                w.writerow([f"b{i:05d}", f"2026-10-01T00:{i // 60 % 60:02d}:{i % 60:02d}", p[idx]])
    with open(out / "gold.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["case_id", "gold"])
        for i, r in enumerate(rows):
            w.writerow([f"b{i:05d}", r["category"]])
    invalid = sum(p[0] == "INVALID" or p[1] == "INVALID" for p in preds)
    print(f"wrote {len(preds)} cases to {out}; {invalid} cases had an unparseable answer (counted as errors)")


if __name__ == "__main__":
    main()
