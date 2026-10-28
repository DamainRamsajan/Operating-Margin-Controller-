# ADR-032: Evidence Statement v0 encoding

- **Status:** Proposed (spike S-d pending)
- **Context:** Statements must verify offline, years later, and must not depend on float formatting.
- **Decision:** COSE_Sign1 with Ed25519 for v0, canonical JSON payload with integers and decimal strings only, hash-chained log. Post-quantum or hybrid signatures and transparency-service registration follow the S-d spike without changing the payload schema (see docs/spec/evidence-statement-v0.md).
- **Consequences:** Deterministic, auditable encoding; v0 signatures are not post-quantum safe.
