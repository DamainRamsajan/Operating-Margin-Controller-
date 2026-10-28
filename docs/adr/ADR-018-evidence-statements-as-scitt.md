# ADR-018: Evidence Statements as SCITT signed statements

- **Status:** Proposed
- **Context:** RFC 9943 defines the SCITT architecture and RFC 9942 COSE receipts; an individual draft already profiles AI-agent action receipts as COSE_Sign1 statements over a canonical payload [S28].
- **Decision:** OMC Evidence Statements are COSE_Sign1 signed statements over a canonical payload, registrable in any SCITT transparency service to obtain receipts and non-equivocation. The OMC schema is a payload profile, not a new envelope. Hash chain and RFC 3161 anchoring remain as fallback.
- **Consequences:** Standards-based verification by third parties; dependency on draft profiles and on post-quantum COSE support, both pinned and tracked (R24).
