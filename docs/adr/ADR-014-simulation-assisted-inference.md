# ADR-014: Simulation only as an input to inference

- **Status:** Proposed
- **Context:** LLM-based and agent-based twins can be calibrated against observed data, but sim-to-real gaps remain [S24].
- **Decision:** Simulator outputs may enter estimators only as predictions corrected by real randomized outcomes and are graded no higher than E2. Stand-alone simulation is E0.
- **Consequences:** Shorter experiments if the hypothesis holds; simulation never becomes a source of billable claims by itself.
