# ADR-010: Outcome-linked pricing with a cap and ramp

- **Status:** Proposed (constrained by ADR-016 and ADR-020)
- **Context:** Fees tied to measured savings align incentives and fund themselves.
- **Decision:** For the full controller, fees are capped and ramp only after two consecutive statements are independently re-run by the customer's finance team. Entry products (migration qualification, billing audit) use fixed fees and never contingent fees.
- **Consequences:** Variable revenue only in later phases; a defensible answer to the conflict-of-interest objection.
