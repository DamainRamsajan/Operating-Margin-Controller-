import importlib.util
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("usability_report", ROOT / "scripts" / "usability_report.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_sus_scoring_known_values():
    assert mod.sus_score([3] * 10) == 50.0
    assert mod.sus_score([5, 1] * 5) == 100.0
    assert mod.sus_score([1, 5] * 5) == 0.0


def test_wilson_bounds_match_documented_guarantees():
    assert abs(mod.wilson(12, 12)[0] - 0.757) < 0.005     # 12 of 12 guarantees about 76 percent
    assert abs(mod.wilson(30, 30)[0] - 0.886) < 0.005     # 30 of 30 guarantees about 89 percent


def test_mcnemar_counts_discordant_pairs():
    r = mod.mcnemar_exact({"p1": 1, "p2": 1, "p3": 0, "p4": 1}, {"p1": 0, "p2": 0, "p3": 0, "p4": 1})
    assert r["first_only_correct"] == 2 and r["second_only_correct"] == 0 and r["pairs"] == 4


def test_full_report_from_templates(tmp_path):
    src = ROOT / "docs" / "ux" / "usability" / "templates"
    for f in src.iterdir():
        shutil.copy(f, tmp_path / f.name)
    (tmp_path / "participants.csv").write_text((tmp_path / "participants.csv").read_text() + "P01,ops,Head of support,SaaS,8,2026-11-10,me,yes\nP02,fin,Controller,Retail,5,2026-11-11,me,yes\n")
    (tmp_path / "task_results.csv").write_text((tmp_path / "task_results.csv").read_text() + "P01,T1,1,40,0,0,\nP02,T1,0.5,70,1,1,\n")
    (tmp_path / "sus_results.csv").write_text((tmp_path / "sus_results.csv").read_text() + "P01,5,1,5,1,5,1,5,1,5,1\nP02,4,2,4,2,4,2,4,2,4,2\n")
    rows = ""
    for pid, ok in (("P01", (1, 1, 0)), ("P02", (1, 0, 0))):
        for t, (ph, o) in enumerate(zip("ABC", ok), start=1):
            rows += f"{pid},{t},benign,{ph},switch,{o},B,1,7.8,{o},4,,,30\n"
    (tmp_path / "comprehension_results.csv").write_text((tmp_path / "comprehension_results.csv").read_text() + rows)
    rep = mod.build(tmp_path)
    assert rep["sus"]["mean"] == 87.5 and rep["tasks"]["T1"]["n"] == 2
    assert rep["comprehension"]["A"]["q1"]["k"] == 2 and rep["paired"]["q1_correct:A vs B"]["first_only_correct"] == 1
    assert "Usability report (2 participants)" in mod.render(rep)
