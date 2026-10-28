# ADR-008: Evidence Vault with hybrid post-quantum signatures and re-anchoring

- **Status:** Proposed (extended by ADR-018)
- **Context:** Records must remain credible for 10 years or more; classical signatures may be forgeable by then.
- **Decision:** Hash chain with Merkle batches; classical plus ML-DSA signatures; SLH-DSA for anchor roots; periodic re-anchoring [S16].
- **Consequences:** Larger signatures and key-management effort; durable evidence.
