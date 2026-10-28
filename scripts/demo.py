"""End-to-end demo: sample data -> gate on three scenarios -> verify -> exposure -> leaks -> privacy.
Run: python scripts/demo.py   (creates out/demo)"""
import json
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
out = root / "out" / "demo"
out.mkdir(parents=True, exist_ok=True)


def run(*args):
    r = subprocess.run([sys.executable, "-m", "omc.cli", *map(str, args)], capture_output=True, text=True, cwd=root)
    return r.returncode, r.stdout.strip()


print("== keygen / sample")
print(run("keygen", "--out-dir", out / "keys")[1])
run("sample", "--out-dir", out / "data", "--n", 30000)
for sc in ("benign", "regression", "unclear"):
    d = out / "data" / sc
    code, txt = run("gate", "--incumbent", d / "incumbent.csv", "--candidate", d / "candidate.csv", "--labels", d / "gold.csv",
                    "--key", out / "keys" / "omc-key.pem", "--out-dir", out / "gate" / sc,
                    "--incumbent-name", "model-a", "--candidate-name", f"model-b-{sc}")
    p = json.loads(txt)
    print(f"== gate {sc}: exit {code} verdict={p['verdict']} tier={p['tier']} cases={p['n_cases']} labels={p['n_labeled']} delta_ub={p['delta_ub']}")
    c, v = run("verify", "statement", out / "gate" / sc / "verdict.cose", "--pubkey", out / "keys" / "omc-key.pub.pem")
    print(f"   verify statement: {'valid' if json.loads(v)['valid'] else 'INVALID'}")
    c, v = run("verify", "chain", out / "gate" / sc / "chain.jsonl", "--pubkey", out / "keys" / "omc-key.pub.pem")
    print(f"   verify chain: {json.loads(v)}")
ops = out / "data" / "ops"
print("== exposure (as of 2026-10-27)")
print(run("exposure", "--decisions", ops / "decisions.csv", "--deprecations", ops / "deprecations.json", "--as-of", "2026-10-27")[1])
rep = json.loads(run("leaks", "--tickets", ops / "tickets.csv")[1])
print("== leaks: overall cost/accepted", rep["overall"]["cost_per_accepted"], "top leak class", rep["ranked_leaks"][0][0])
print("== privacy: redact", run("redact", "--in", ops / "transcripts.txt", "--out", out / "redacted.txt")[1])
print((out / "redacted.txt").read_text())
print("== leakage audit 0/300 reviewed, limit 2%:", json.loads(run("leakage-audit", "--reviewed", 300, "--leaks", 0, "--limit", 0.02)[1])["decision"])
print("== provider terms ok:", run("provider-terms", "--terms", ops / "provider_terms_ok.json", "--policy", ops / "provider_policy.json")[1])
print("== provider terms bad:", run("provider-terms", "--terms", ops / "provider_terms_bad.json", "--policy", ops / "provider_policy.json")[1])
