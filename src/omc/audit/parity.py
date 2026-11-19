"""Business-metric parity (non-inferiority) audit (arc42 5.7 Equivalence Tester, FR15).
For a bounded per-case metric (accepted outcome 0/1, cost, handle time with a cap), paired by case.
Claim: the candidate is not worse than the incumbent by more than a margin, with confidence 1 - alpha,
valid under continuous monitoring (same confidence-sequence machinery as the paired audit).
All cases need the metric, so this costs more labels than the disagreement-supported audit when the metric
is human-labeled; use it for metrics that are logged automatically (cost, time, reopen)."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from omc.stats import cs


@dataclass
class ParityConfig:
    lo: float = 0.0               # smallest possible metric value
    hi: float = 1.0               # largest possible metric value
    margin: float = 0.01          # tolerated worsening, in metric units
    higher_is_better: bool = True
    alpha: float = 0.05
    check_every: int = 100


@dataclass
class ParityResult:
    verdict: str                  # promote (non-inferior) | reject (inferior) | hold
    n_cases: int
    stopping_index: int | None
    diff_lb: float                # bounds on mean(candidate - incumbent) in metric units
    diff_ub: float
    reason: str


def run_parity(case_ids, incumbent: dict, candidate: dict, cfg: ParityConfig) -> ParityResult:
    width = cfg.hi - cfg.lo
    sign = 1.0 if cfg.higher_is_better else -1.0
    # normalized "goodness" difference in [-1, 1]: positive means the candidate is better
    d = np.array([sign * (candidate[c] - incumbent[c]) / width for c in case_ids], dtype=float)
    x = (np.clip(d, -1, 1) + 1) / 2
    n_total = len(x)
    cum = np.cumsum(x)
    idx = np.arange(cfg.check_every, n_total + 1, cfg.check_every)
    if len(idx) == 0 or idx[-1] != n_total:
        idx = np.append(idx, n_total)
    n = idx.astype(float)
    s = cum[idx - 1]
    a = cfg.alpha
    lb = 2 * cs.lower_bound(s, n, a) - 1      # lower bound on mean goodness difference (normalized)
    ub = 2 * cs.upper_bound(s, n, a) - 1
    m = cfg.margin / width
    ok = lb >= -m
    bad = ub < -m
    def conv(v):  # back to metric units, in "candidate minus incumbent" orientation
        return float(sign * v * width)
    if ok.any() and (not bad.any() or np.argmax(ok) <= np.argmax(bad)):
        i = int(np.argmax(ok))
        lo_u, hi_u = sorted((conv(lb[i]), conv(ub[i])))
        return ParityResult("promote", int(n[i]), int(idx[i]), lo_u, hi_u, "worsening bound within margin")
    if bad.any():
        i = int(np.argmax(bad))
        lo_u, hi_u = sorted((conv(lb[i]), conv(ub[i])))
        return ParityResult("reject", int(n[i]), int(idx[i]), lo_u, hi_u, "worsening exceeds margin")
    lo_u, hi_u = sorted((conv(lb[-1]), conv(ub[-1])))
    return ParityResult("hold", int(n[-1]), None, lo_u, hi_u, "more cases needed")
