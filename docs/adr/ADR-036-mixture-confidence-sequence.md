# ADR-036: Beta-binomial mixture confidence sequence for the disagreement rate

- **Status:** Proposed (implemented in `omc/stats/cs.py`; simulation-validated)
- **Context:** The stitched union bound was valid but wide. The disagreement indicator is exactly Bernoulli, so a mixture likelihood ratio gives a confidence sequence valid at all sample sizes (Ville's inequality) without the union-bound penalty.
- **Decision:** Use the mixture bound for the disagreement rate (default `rho_method="mixture"`); keep the union bound as an option and for non-Bernoulli quantities. Disagreement and label sequences still split alpha equally.
- **Consequences:** In simulation, equivalent models with rare disagreement certify with about 3 times fewer cases and a regression twice the tolerance is flagged more often, with no false certificates in the simulated worlds. The bound is still an own implementation: have it reviewed.
