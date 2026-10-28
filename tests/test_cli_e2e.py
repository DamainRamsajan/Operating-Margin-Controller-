import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args):
    r = subprocess.run([sys.executable, "-m", "omc.cli", *map(str, args)], capture_output=True, text=True, cwd=ROOT)
    return r.returncode, r.stdout


def test_gate_end_to_end(tmp_path):
    run("keygen", "--out-dir", tmp_path / "k")
    run("sample", "--out-dir", tmp_path / "d", "--n", 16000)
    expect = {"benign": 0, "regression": 20}
    for sc, code_expected in expect.items():
        d = tmp_path / "d" / sc
        code, out = run("gate", "--incumbent", d / "incumbent.csv", "--candidate", d / "candidate.csv",
                        "--labels", d / "gold.csv", "--key", tmp_path / "k" / "omc-key.pem", "--out-dir", tmp_path / "o" / sc)
        assert code == code_expected, (sc, out)
        vcode, vout = run("verify", "statement", tmp_path / "o" / sc / "verdict.cose", "--pubkey", tmp_path / "k" / "omc-key.pub.pem")
        assert vcode == 0 and json.loads(vout)["valid"] is True
        ccode, _ = run("verify", "chain", tmp_path / "o" / sc / "chain.jsonl", "--pubkey", tmp_path / "k" / "omc-key.pub.pem")
        assert ccode == 0


def test_hold_returns_label_requests(tmp_path):
    run("keygen", "--out-dir", tmp_path / "k")
    run("sample", "--out-dir", tmp_path / "d", "--n", 6000)
    d = tmp_path / "d" / "unclear"
    code, _ = run("gate", "--incumbent", d / "incumbent.csv", "--candidate", d / "candidate.csv",
                  "--key", tmp_path / "k" / "omc-key.pem", "--out-dir", tmp_path / "o")
    assert code == 10 and (tmp_path / "o" / "label_requests.txt").read_text().strip()


def test_check_data_and_pseudonymize(tmp_path):
    run("sample", "--out-dir", tmp_path / "d", "--n", 3000)
    d = tmp_path / "d" / "benign"
    code, out = run("check-data", "--incumbent", d / "incumbent.csv", "--candidate", d / "candidate.csv", "--labels", d / "gold.csv")
    info = json.loads(out)
    assert code == 0 and info["cases_in_both"] == 3000 and 0 <= info["disagreement_rate"] < 0.05
    assert info["gold_coverage_all"] == 1.0
    (tmp_path / "secret.txt").write_text("keep-me-private")
    code, _ = run("pseudonymize", "--in", d / "gold.csv", "--out", tmp_path / "gold_p.csv", "--column", "case_id",
                  "--secret-file", tmp_path / "secret.txt")
    assert code == 0
    first = (tmp_path / "gold_p.csv").read_text().splitlines()[1].split(",")[0]
    assert len(first) == 16 and not first.startswith("c0")


def test_check_data_flags_problems(tmp_path):
    (tmp_path / "a.csv").write_text("case_id,prediction\nx,a\nx,b\n")
    (tmp_path / "b.csv").write_text("case_id,prediction\nx,a\n")
    code, out = run("check-data", "--incumbent", tmp_path / "a.csv", "--candidate", tmp_path / "b.csv")
    assert code == 20 and any("duplicate" in i for i in json.loads(out)["issues"])
