import pytest

from omc.audit.paired import AuditConfig
from omc.audit.simulate import World, run_campaign

CFG = AuditConfig(epsilon=0.01, alpha=0.05, label_rate=0.5)


@pytest.mark.slow
def test_false_certificate_rate_below_alpha_when_regression_exceeds_tolerance():
    r = run_campaign(World(0.05, 0.625, 0.375), CFG, runs=150, n=30000, seed=11)   # true delta 0.0125 > 0.01
    assert r["certified_rate"] <= CFG.alpha


@pytest.mark.slow
def test_equivalent_models_are_usually_certified():
    r = run_campaign(World(0.004, 0.4, 0.4), CFG, runs=100, n=30000, seed=12)
    assert r["certified_rate"] >= 0.9


@pytest.mark.slow
def test_clear_regression_is_rejected_in_simulation():
    r = run_campaign(World(0.06, 0.70, 0.15), CFG, runs=100, n=30000, seed=13)
    assert r["rejected_rate"] >= 0.9
