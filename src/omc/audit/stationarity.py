"""Informational stationarity check. The audit's guarantee assumes a stable stream. Recent work shows
that guarantees calibrated on one distribution can fail badly after a shift, so every audit reports whether
the disagreement rate moved between the first and second half of the window. This check does not change
the guarantee; it warns when the assumption looks violated."""
from __future__ import annotations

import math


def two_proportion_p(k1: int, n1: int, k2: int, n2: int) -> float:
    if min(n1, n2) == 0:
        return 1.0
    p1, p2, p = k1 / n1, k2 / n2, (k1 + k2) / (n1 + n2)
    se = math.sqrt(max(p * (1 - p) * (1 / n1 + 1 / n2), 1e-18))
    z = abs(p1 - p2) / se
    return math.erfc(z / math.sqrt(2))


def check(disagree_flags: list[int], threshold: float = 0.01, min_events: int = 8) -> dict:
    n = len(disagree_flags)
    h = n // 2
    k1, k2 = sum(disagree_flags[:h]), sum(disagree_flags[h:])
    p = two_proportion_p(k1, h, k2, n - h)
    warn = bool(p < threshold and (k1 + k2) >= min_events)
    return {"first_half_rate": k1 / h if h else 0.0, "second_half_rate": k2 / (n - h) if n - h else 0.0,
            "p_value": p, "warning": warn}
