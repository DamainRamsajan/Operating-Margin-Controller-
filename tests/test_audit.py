import inspect

from omc.audit import paired
from omc.audit.paired import AuditConfig, run_audit, selected_for_label


def _ids(n):
    return [f"c{i}" for i in range(n)]


def test_identical_models_get_tier0_certificate():
    ids = _ids(5000)
    pred = {c: "a" for c in ids}
    r = run_audit(ids, pred, dict(pred), {}, AuditConfig(epsilon=0.01))
    assert r.verdict == "promote" and r.tier == "tier0" and r.n_labeled == 0


def test_hold_and_label_requests_when_labels_missing():
    ids = _ids(3000)
    inc = {c: "a" for c in ids}
    cand = {c: ("b" if i % 10 == 0 else "a") for i, c in enumerate(ids)}   # 10 percent disagreement
    r = run_audit(ids, inc, cand, {}, AuditConfig(epsilon=0.01))
    assert r.verdict == "hold" and r.labels_requested


def test_clear_regression_is_rejected():
    ids = _ids(20000)
    inc = {c: "a" for c in ids}
    cand = {c: ("b" if i % 10 == 0 else "a") for i, c in enumerate(ids)}   # candidate wrong on disagreements
    gold = {c: "a" for c in ids}
    r = run_audit(ids, inc, cand, gold, AuditConfig(epsilon=0.01))
    assert r.verdict == "reject" and r.tier == "tier1"


def test_clear_improvement_is_certified_with_labels():
    ids = _ids(20000)
    inc = {c: ("b" if i % 10 == 0 else "a") for i, c in enumerate(ids)}
    cand = {c: "a" for c in ids}
    gold = {c: "a" for c in ids}
    r = run_audit(ids, inc, cand, gold, AuditConfig(epsilon=0.01))
    assert r.verdict == "promote"


def test_min_label_guardrail_blocks_tiny_label_certificates():
    ids = _ids(4000)
    inc = {c: "a" for c in ids}
    cand = {c: ("b" if i % 25 == 0 else "a") for i, c in enumerate(ids)}
    gold = {c: "b" for c in ids}   # incumbent wrong where they disagree, so candidate is better
    r = run_audit(ids, inc, cand, gold, AuditConfig(epsilon=0.01, min_labels=10**9))
    assert r.tier != "tier1"


def test_label_selection_never_sees_the_label():
    params = inspect.signature(selected_for_label).parameters
    assert list(params) == ["case_id", "salt", "q"]          # TC8 and Q17: no outcome argument
    assert selected_for_label("x", "s", 0.5) == selected_for_label("x", "s", 0.5)


def test_module_exposes_no_gold_dependent_router():
    src = inspect.getsource(paired.selected_for_label)
    assert "gold" not in src and "label" not in src.split('"""')[2]
