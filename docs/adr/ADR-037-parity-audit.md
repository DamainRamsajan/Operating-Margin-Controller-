# ADR-037: Business-metric parity audit for logged metrics

- **Status:** Proposed (implemented in `omc/audit/parity.py`; simulation-validated)
- **Context:** The architecture promises business-metric parity (accepted outcome, cost, handle time) for model swaps, but the audit had only the decision-level test.
- **Decision:** Add a paired non-inferiority audit for bounded per-case metrics with anytime-valid bounds and an owner-set margin. Use it for metrics logged automatically; use the disagreement-supported audit when the metric needs human labels.
- **Consequences:** Parity evidence that finance can read; needs the metric for every case; bounds are conservative, so margins below about one percentage point need many cases.
