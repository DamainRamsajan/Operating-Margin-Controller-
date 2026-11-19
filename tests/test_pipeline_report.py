import importlib.util
from datetime import date
from pathlib import Path

spec = importlib.util.spec_from_file_location("pipeline_report", Path(__file__).resolve().parents[1] / "scripts" / "pipeline_report.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_pipeline_report(tmp_path):
    p = tmp_path / "p.csv"
    p.write_text("org,contact_role,tier,source,stage,last_touch,next_step,next_date,notes\n"
                 "A,ops,1,job,contacted,2026-11-01,follow up,2026-11-05,\n"
                 "B,ops,1,job,replied,2026-11-01,call,2026-11-20,\n"
                 "C,ops,2,post,design_partner,2026-11-01,sign,2026-11-03,\n"
                 "D,ops,1,job,lost,2026-11-01,,,\n")
    r = mod.report(p, date(2026, 11, 10))
    assert r["reached"]["contacted"] == 3 and r["reached"]["replied"] == 2
    assert r["reply_rate"] == round(2 / 3, 3) and sorted(r["overdue_next_steps"]) == ["A", "C"]
