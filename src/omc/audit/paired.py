"""Certified paired audit for a model update (ADR-019, arc42 5.7 and 6.9).

Setting: an incumbent and a candidate each make a discrete decision per case (class label,
resolve or escalate, tool choice). The loss is 0-1 against a gold label, so the loss is
determined by the prediction: when the two decisions agree, the losses are equal.
Let D = L_candidate - L_incumbent in {-1, 0, 1}. Then
    Delta = E[D] = rho * mu,   rho = P(disagree),   mu = E[D | disagree].
No-regression certificate: Delta <= epsilon with confidence 1 - alpha, valid under
continuous monitoring (see omc.stats.cs).

Tier 0: no labels. rho is observable from traffic. Since |mu| <= 1, Delta <= rho, so
        UB(rho) <= epsilon certifies.
Tier 1: label a random subset of disagreements (selection independent of outcome).
        mu is estimated from them. Delta <= UB(rho) * max(UB(mu), 0).
The two confidence sequences each use alpha / 2 (union bound).

Assumptions: cases are i.i.d. from a stationary stream over the audit window; label selection
never reads the gold label (TC8). Open-ended text is out of scope: use action-level decisions
(ADR-021).
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

import numpy as np

from omc.stats import cs


def selected_for_label(case_id: str, salt: str, q: float) -> bool:
    """Outcome-independent, reproducible selection of a disagreement for labeling."""
    h = hashlib.sha256(f"{salt}:{case_id}".encode()).digest()
    u = int.from_bytes(h[:8], "big") / 2**64
    return u < q


@dataclass
class AuditConfig:
    epsilon: float = 0.01      # tolerated regression in error rate
    alpha: float = 0.05        # total error probability
    label_rate: float = 0.5    # share of disagreements sent for labeling
    salt: str = "omc-audit-v0"
    min_cases: int = 1
    check_every: int = 100     # evaluate bounds at checkpoints; validity is unaffected
    min_labels: int = 30       # operational guardrail for Tier 1 (not needed for validity)


@dataclass
class AuditResult:
    verdict: str               # promote | hold | reject
    tier: str                  # tier0 | tier1 | none
    n_cases: int
    n_disagree: int
    n_labeled: int
    stopping_index: int | None
    rho_ub: float
    rho_lb: float
    mu_ub: float | None
    mu_lb: float | None
    delta_ub: float
    delta_lb: float
    labels_requested: list[str] = field(default_factory=list)
    reason: str = ""


def _bounds(n, d, m, s, alpha):
    """Bounds on rho (from n cases, d disagreements) and on mu (from m labels with sum s of
    D' = (D + 1) / 2 in [0, 1])."""
    a = alpha / 2
    rho_ub = cs.ub_scalar(d, n, a)
    rho_lb = cs.lb_scalar(d, n, a)
    if m > 0:
        mu_ub = 2 * cs.ub_scalar(s, m, a) - 1
        mu_lb = 2 * cs.lb_scalar(s, m, a) - 1
    else:
        mu_ub, mu_lb = 1.0, -1.0
    delta_ub = rho_ub * max(mu_ub, 0.0)
    delta_lb = rho_lb * max(mu_lb, 0.0)
    return rho_ub, rho_lb, mu_ub, mu_lb, delta_ub, delta_lb


def run_audit(case_ids, incumbent, candidate, gold: dict[str, str] | None, cfg: AuditConfig):
    """Process cases in order. Stops at the first certification or regression alarm.

    gold: case_id -> gold label, for cases where a label is available. Disagreements that are
    selected for labeling but have no label yet are returned in labels_requested.
    """
    gold = gold or {}
    n = d = m = 0
    s = 0.0
    requested: list[str] = []
    last = None
    for i, cid in enumerate(case_ids):
        n += 1
        pi, pc = incumbent[cid], candidate[cid]
        if pi != pc:
            d += 1
            if selected_for_label(cid, cfg.salt, cfg.label_rate):
                if cid in gold:
                    y = gold[cid]
                    dd = (1 if pc != y else 0) - (1 if pi != y else 0)  # L_c - L_i
                    m += 1
                    s += (dd + 1) / 2
                else:
                    requested.append(cid)
        if n < cfg.min_cases or (n % cfg.check_every != 0):
            continue
        last = _bounds(n, d, m, s, cfg.alpha)
        rho_ub, rho_lb, mu_ub, mu_lb, delta_ub, delta_lb = last
        if rho_ub <= cfg.epsilon:
            return AuditResult("promote", "tier0", n, d, m, i, rho_ub, rho_lb, mu_ub, mu_lb,
                               delta_ub, delta_lb, requested, "disagreement rate bound below tolerance")
        if m >= cfg.min_labels and delta_ub <= cfg.epsilon:
            return AuditResult("promote", "tier1", n, d, m, i, rho_ub, rho_lb, mu_ub, mu_lb,
                               delta_ub, delta_lb, requested, "regression bound below tolerance")
        if m >= cfg.min_labels and delta_lb > cfg.epsilon:
            return AuditResult("reject", "tier1", n, d, m, i, rho_ub, rho_lb, mu_ub, mu_lb,
                               delta_ub, delta_lb, requested, "regression bound above tolerance")
    if n > 0 and (last is None or n % cfg.check_every != 0):
        last = _bounds(n, d, m, s, cfg.alpha)
    if last is None:
        return AuditResult("hold", "none", n, d, m, None, 1.0, 0.0, None, None, 1.0, 0.0,
                           requested, "no data")
    rho_ub, rho_lb, mu_ub, mu_lb, delta_ub, delta_lb = last
    why = "more traffic needed" if not requested else "labels needed for selected disagreements"
    return AuditResult("hold", "none", n, d, m, None, rho_ub, rho_lb, mu_ub, mu_lb,
                       delta_ub, delta_lb, requested, why)


def monitor_vectorized(agree_flags: np.ndarray, d_values: np.ndarray, label_mask: np.ndarray,
                       cfg: AuditConfig, check_every: int = 50):
    """Fast version for simulation. Inputs are per-case arrays:
    agree_flags (1 = disagree), d_values (L_c - L_i, only used where disagree and labeled),
    label_mask (1 = this disagreement is selected for labeling).
    Returns (certified_index or None, rejected_index or None)."""
    n_total = len(agree_flags)
    idx = np.arange(check_every, n_total + 1, check_every)
    cum_d = np.cumsum(agree_flags)
    lab = (agree_flags * label_mask).astype(float)
    cum_m = np.cumsum(lab)
    cum_s = np.cumsum(lab * (d_values + 1) / 2)
    n = idx.astype(float)
    d = cum_d[idx - 1].astype(float)
    m = cum_m[idx - 1]
    s = cum_s[idx - 1]
    a = cfg.alpha / 2
    rho_ub = cs.upper_bound(d, n, a)
    rho_lb = cs.lower_bound(d, n, a)
    mu_ub = np.where(m > 0, 2 * cs.upper_bound(s, m, a) - 1, 1.0)
    mu_lb = np.where(m > 0, 2 * cs.lower_bound(s, m, a) - 1, -1.0)
    delta_ub = rho_ub * np.maximum(mu_ub, 0.0)
    delta_lb = rho_lb * np.maximum(mu_lb, 0.0)
    cert = (rho_ub <= cfg.epsilon) | ((m >= cfg.min_labels) & (delta_ub <= cfg.epsilon))
    rej = (m >= cfg.min_labels) & (delta_lb > cfg.epsilon)
    ci = int(idx[np.argmax(cert)]) if cert.any() else None
    ri = int(idx[np.argmax(rej)]) if rej.any() else None
    return ci, ri
