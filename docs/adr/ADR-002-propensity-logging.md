# ADR-002: Log propensity, candidate set and feasible set for every decision

- **Status:** Proposed
- **Context:** Without selection probabilities, logged data is confounded.
- **Decision:** Mandatory for gated and canary modes; a deployment that cannot log them cannot actuate.
- **Consequences:** Extra storage; enables E3 evidence and off-policy evaluation.
