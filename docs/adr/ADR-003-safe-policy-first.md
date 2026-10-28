# ADR-003: Safe-policy-first actuation

- **Status:** Proposed
- **Context:** Customers will not accept experiments that can exceed their risk tolerance.
- **Decision:** The baseline is always feasible; the risk gate uses conformal calibration anchored on baseline data; the policy moves only within the calibrated bound; the kill switch returns to baseline [S8].
- **Consequences:** Slower early gains and credible safety. Supporting methods are recent preprints; spike S-f confirms behavior before commitment.
