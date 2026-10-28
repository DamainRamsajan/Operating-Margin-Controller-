# Limitations of M0 (read before relying on any result)

1. **Synthetic data only.** Every result comes from planted-ground-truth simulations. Nothing here has been validated on real tickets (spike S-a).
2. **Stationarity assumption.** The confidence bounds assume cases are i.i.d. from a fixed distribution over the audit window. Drift, seasonality or changing traffic mix can invalidate a certificate. Windowed variants and drift detection are not built.
3. **Loss class.** The theory covers losses determined by the decision (0-1 against a gold label). Free-text quality is out of scope until the material-difference classifier exists (ADR-021).
4. **Conservative by design.** The union bound over sample sizes gives valid but wide bounds. The `unclear` scenario (true regression 0.003, tolerance 0.01) is still on hold after 30,000 cases. Tighter sequences (empirical-Bernstein or mixture methods) are future work.
5. **Uniform label sampling only.** Disagreements are labeled at a fixed rate. Judge-guided routing and importance weighting are not implemented.
6. **Gold labels are assumed correct.** Label noise is not modeled.
7. **Signatures.** Ed25519 only; no post-quantum or hybrid signing, no transparency-service registration, no timestamp anchoring, no key management beyond PEM files.
8. **Redaction is rule-based.** `omc redact` catches common patterns only; the leakage audit measures what it misses on a reviewed sample and must be run on real data. Provider-terms checks compare declared terms and cannot verify provider behavior.
9. **Leak report is descriptive** (evidence grade E0): it does not estimate causal effects.
10. **The statistics are my own implementation from first principles**, not a port of any published code. They are tested by simulation, not independently audited. Have a statistician review `omc/stats/cs.py` and `omc/audit/paired.py` before any customer-facing claim.
