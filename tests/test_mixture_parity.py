import numpy as np
import pytest

from omc.audit.parity import ParityConfig, run_parity
from omc.audit.stationarity import check
from omc.stats import cs


def test_mixture_bounds_bracket_and_are_tighter_than_union():
    for s, n in ((4, 1000), (40, 5000), (0, 800), (300, 3000)):
        ub_m, ub_u = cs.mix_ub_scalar(s, n, 0.025), cs.ub_scalar(s, n, 0.025)
        lb_m, lb_u = cs.mix_lb_scalar(s, n, 0.025), cs.lb_scalar(s, n, 0.025)
        assert lb_m <= s / n <= ub_m
        assert ub_m <= ub_u + 1e-9 and lb_m >= lb_u - 1e-9
    assert cs.mix_ub_scalar(0, 0, 0.05) == 1.0 and cs.mix_lb_scalar(5, 5, 0.05) <= 1.0


def test_mixture_anytime_coverage():
    rng = np.random.default_rng(3)
    alpha, p, n_max, runs = 0.05, 0.02, 4000, 200
    n = np.arange(1, n_max + 1)
    bad = 0
    for _ in range(runs):
        cum = np.cumsum(rng.random(n_max) < p)
        if (cs.bern_mix_upper(cum, n, alpha) < p).any() or (cs.bern_mix_lower(cum, n, alpha) > p).any():
            bad += 1
    assert bad / runs <= 2 * alpha


def _stream(rng, n, p_inc, p_cand):
    ids = [f"c{i}" for i in range(n)]
    inc = {c: float(rng.random() < p_inc) for c in ids}
    cand = {c: float(rng.random() < p_cand) for c in ids}
    return ids, inc, cand


def test_parity_promotes_equal_metric():
    ids, inc, cand = _stream(np.random.default_rng(1), 30000, 0.80, 0.80)
    r = run_parity(ids, inc, cand, ParityConfig(margin=0.05))
    assert r.verdict == "promote" and r.diff_lb >= -0.05


def test_parity_rejects_clear_worsening():
    ids, inc, cand = _stream(np.random.default_rng(2), 30000, 0.80, 0.70)
    assert run_parity(ids, inc, cand, ParityConfig(margin=0.02)).verdict == "reject"


def test_parity_holds_with_little_data_and_handles_lower_is_better():
    ids, inc, cand = _stream(np.random.default_rng(4), 300, 0.8, 0.8)
    assert run_parity(ids, inc, cand, ParityConfig(margin=0.01)).verdict == "hold"
    big = [f"k{i}" for i in range(5000)]
    cost_inc = {c: 5.0 for c in big}
    cost_cand = {c: 4.0 for c in big}                      # candidate is cheaper: better when lower is better
    r = run_parity(big, cost_inc, cost_cand, ParityConfig(lo=0, hi=10, margin=0.5, higher_is_better=False))
    assert r.verdict == "promote" and r.diff_ub <= 0.5   # cost increase bound within the 0.5 margin


@pytest.mark.slow
def test_parity_false_promotion_rate_below_alpha():
    rng = np.random.default_rng(9)
    false = 0
    for _ in range(80):
        ids, inc, cand = _stream(rng, 6000, 0.80, 0.74)     # true worsening 0.06 > margin 0.05
        false += run_parity(ids, inc, cand, ParityConfig(margin=0.05)).verdict == "promote"
    assert false / 80 <= 0.05


def test_stationarity_warns_on_shift_only():
    steady = ([0] * 95 + [1] * 5) * 20
    shifted = [0] * 1000 + ([0] * 70 + [1] * 30) * 10
    assert check(steady)["warning"] is False
    assert check(shifted)["warning"] is True
