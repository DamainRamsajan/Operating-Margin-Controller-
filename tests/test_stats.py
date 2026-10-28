import numpy as np

from omc.stats import cs


def test_bounds_bracket_sample_mean():
    ub = cs.ub_scalar(10, 100, 0.05)
    lb = cs.lb_scalar(10, 100, 0.05)
    assert lb < 0.1 < ub <= 1.0 and lb >= 0.0


def test_no_data_is_vacuous():
    assert cs.ub_scalar(0, 0, 0.05) == 1.0
    assert cs.lb_scalar(0, 0, 0.05) == 0.0


def test_bounds_tighten_with_n():
    assert cs.ub_scalar(100, 1000, 0.05) - 0.1 > cs.ub_scalar(1000, 10000, 0.05) - 0.1


def test_anytime_coverage_under_continuous_monitoring():
    rng = np.random.default_rng(1)
    alpha, p, n_max, runs = 0.05, 0.1, 3000, 200
    bad = 0
    n = np.arange(1, n_max + 1)
    for _ in range(runs):
        cum = np.cumsum(rng.random(n_max) < p)
        if (cs.upper_bound(cum, n, alpha) < p).any() or (cs.lower_bound(cum, n, alpha) > p).any():
            bad += 1
    assert bad / runs <= 2 * alpha
