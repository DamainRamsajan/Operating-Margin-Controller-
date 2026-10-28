"""Synthetic worlds with planted ground truth for testing audits (arc42 8.8, Q15, Q17)."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from omc.audit.paired import AuditConfig, monitor_vectorized


@dataclass
class World:
    """Disagreement rate d. On disagreement, the incumbent alone is right with prob p_inc_only,
    the candidate alone with p_cand_only, otherwise both are wrong with different answers.
    True regression Delta = d * (p_inc_only - p_cand_only)."""
    d: float
    p_inc_only: float
    p_cand_only: float

    @property
    def delta(self) -> float:
        return self.d * (self.p_inc_only - self.p_cand_only)


def draw(world: World, n: int, label_rate: float, rng: np.random.Generator):
    dis = (rng.random(n) < world.d).astype(int)
    u = rng.random(n)
    d_val = np.where(u < world.p_inc_only, 1,            # candidate wrong, incumbent right
             np.where(u < world.p_inc_only + world.p_cand_only, -1, 0))
    label_mask = (rng.random(n) < label_rate).astype(int)
    return dis, d_val, label_mask


def run_campaign(world: World, cfg: AuditConfig, runs: int, n: int, seed: int,
                 check_every: int = 50):
    rng = np.random.default_rng(seed)
    cert, rej, cert_n, labels = 0, 0, [], []
    for _ in range(runs):
        dis, d_val, mask = draw(world, n, cfg.label_rate, rng)
        ci, ri = monitor_vectorized(dis, d_val, mask, cfg, check_every)
        if ci is not None and (ri is None or ci <= ri):
            cert += 1
            cert_n.append(ci)
            labels.append(int((dis[:ci] * mask[:ci]).sum()))
        elif ri is not None:
            rej += 1
    return {
        "runs": runs, "certified": cert, "rejected": rej,
        "certified_rate": cert / runs, "rejected_rate": rej / runs,
        "median_cases_to_certify": float(np.median(cert_n)) if cert_n else None,
        "median_labels_to_certify": float(np.median(labels)) if labels else None,
        "true_delta": world.delta,
    }
