"""Anytime-valid confidence bounds for means of [0, 1]-valued variables.

Method: Chernoff-Hoeffding KL bound at each sample size n, with a union bound over n
(alpha_n = 6 * alpha / (pi^2 * n^2), so the sum over n is at most alpha).
For X in [0, 1] and t > 0, Hoeffding (1963, Thm 1) gives
    P(mean_n >= mu + t) <= exp(-n * KL(mu + t || mu)),
the same bound as for Bernoulli variables. Inverting it gives an upper bound
    UB_n = max { p >= phat : n * KL(phat || p) <= log(1 / alpha_n) }
and symmetrically a lower bound. Because of the union bound, the bounds hold
simultaneously for all n with probability at least 1 - alpha (one-sided), so they
remain valid under continuous monitoring and optional stopping.

Assumption: the observations are independent draws from a fixed distribution (stationary).
"""
from __future__ import annotations

import math

import numpy as np

_EPS = 1e-12


def _kl(p: np.ndarray, q: np.ndarray) -> np.ndarray:
    """Bernoulli KL(p || q), vectorized, with 0 log 0 = 0."""
    p = np.clip(p, 0.0, 1.0)
    q = np.clip(q, _EPS, 1.0 - _EPS)
    with np.errstate(divide="ignore", invalid="ignore"):
        a = np.where(p > 0, p * np.log(p / q), 0.0)
        b = np.where(p < 1, (1 - p) * np.log((1 - p) / (1 - q)), 0.0)
    return a + b


def log_inv_alpha_n(n: np.ndarray, alpha: float) -> np.ndarray:
    """log(1 / alpha_n) with alpha_n = 6 alpha / (pi^2 n^2)."""
    n = np.asarray(n, dtype=float)
    return np.log((math.pi**2) * n**2 / (6.0 * alpha))


def upper_bound(sum_x: np.ndarray, n: np.ndarray, alpha: float) -> np.ndarray:
    """Anytime-valid one-sided upper bound on the mean. n == 0 returns 1."""
    sum_x = np.asarray(sum_x, dtype=float)
    n = np.asarray(n, dtype=float)
    out = np.ones_like(sum_x, dtype=float)
    ok = n > 0
    if not np.any(ok):
        return out
    phat = np.where(ok, sum_x / np.maximum(n, 1), 0.0)
    c = np.where(ok, log_inv_alpha_n(np.maximum(n, 1), alpha) / np.maximum(n, 1), 0.0)
    lo, hi = phat.copy(), np.ones_like(phat)
    for _ in range(60):
        mid = (lo + hi) / 2
        too_far = _kl(phat, mid) > c
        hi = np.where(too_far, mid, hi)
        lo = np.where(too_far, lo, mid)
    out = np.where(ok, hi, 1.0)
    return out


def lower_bound(sum_x: np.ndarray, n: np.ndarray, alpha: float) -> np.ndarray:
    """Anytime-valid one-sided lower bound on the mean. n == 0 returns 0."""
    sum_x = np.asarray(sum_x, dtype=float)
    n = np.asarray(n, dtype=float)
    # lower bound on mean of X equals 1 - upper bound on mean of (1 - X)
    return 1.0 - upper_bound(n - sum_x, n, alpha)


def ub_scalar(sum_x: float, n: int, alpha: float) -> float:
    return float(upper_bound(np.array([sum_x]), np.array([n]), alpha)[0])


def lb_scalar(sum_x: float, n: int, alpha: float) -> float:
    return float(lower_bound(np.array([sum_x]), np.array([n]), alpha)[0])


# ---------------------------------------------------------------------------------------------
# Beta-binomial mixture confidence sequence for Bernoulli means (tighter than the union bound).
# For a fixed p0 the mixture likelihood ratio
#     M_n(p0) = [B(S + a, n - S + b) / B(a, b)] / [p0^S (1 - p0)^(n - S)]
# is a nonnegative martingale under p0, so by Ville's inequality P(sup_n M_n(p0) >= 1/alpha) <= alpha.
# The confidence sequence {p0 : M_n(p0) < 1/alpha} therefore covers the true p at all n at once.
# It applies to Bernoulli data only (for example the disagreement indicator).
# ---------------------------------------------------------------------------------------------
from scipy.special import betaln  # noqa: E402


def _log_mix(s, n, p0, a, b):
    p0 = np.clip(p0, 1e-12, 1 - 1e-12)
    return betaln(s + a, n - s + b) - betaln(a, b) - s * np.log(p0) - (n - s) * np.log1p(-p0)


def bern_mix_upper(sum_x, n, alpha, a=0.5, b=0.5):
    s = np.asarray(sum_x, dtype=float)
    n = np.asarray(n, dtype=float)
    phat = np.where(n > 0, s / np.maximum(n, 1), 0.0)
    thr = np.log(1.0 / alpha)
    lo, hi = phat.copy(), np.ones_like(phat)
    for _ in range(60):
        mid = (lo + hi) / 2
        inside = _log_mix(s, n, mid, a, b) < thr
        lo = np.where(inside, mid, lo)
        hi = np.where(inside, hi, mid)
    return np.where(n > 0, np.where(s >= n, 1.0, hi), 1.0)


def bern_mix_lower(sum_x, n, alpha, a=0.5, b=0.5):
    s = np.asarray(sum_x, dtype=float)
    n = np.asarray(n, dtype=float)
    phat = np.where(n > 0, s / np.maximum(n, 1), 0.0)
    thr = np.log(1.0 / alpha)
    lo, hi = np.zeros_like(phat), phat.copy()
    for _ in range(60):
        mid = (lo + hi) / 2
        inside = _log_mix(s, n, mid, a, b) < thr
        hi = np.where(inside, mid, hi)
        lo = np.where(inside, lo, mid)
    return np.where(n > 0, np.where(s <= 0, 0.0, lo), 0.0)


def mix_ub_scalar(sum_x, n, alpha):
    return float(bern_mix_upper(np.array([sum_x]), np.array([n]), alpha)[0])


def mix_lb_scalar(sum_x, n, alpha):
    return float(bern_mix_lower(np.array([sum_x]), np.array([n]), alpha)[0])
