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
