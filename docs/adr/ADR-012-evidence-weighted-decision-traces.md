# ADR-012: Evidence-weighted decision traces (Precedent Store)

- **Status:** Proposed
- **Context:** The context-graph category treats decision traces as a compounding asset, but traces are observational, can be stale, and need provenance, versioning and access control [S21].
- **Decision:** Store traces with evidence grade, propensity, policy and model version, access scope and expiry. Retrieval filters by minimum grade and unexpired provenance. Phase 2.
- **Consequences:** Differentiates from graph vendors; adds storage and governance work; the retrieval benefit is a hypothesis to test.
