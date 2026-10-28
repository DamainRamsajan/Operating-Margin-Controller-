# ADR-029: Replay Privacy Gate

- **Status:** Proposed (pending spike S-k)
- **Context:** Evaluation sets built from production transcripts are personal data; redaction leaves residual leakage (one preprint reports 0.6 percent residual PII leakage for local routing plus redaction plus rephrasing) and sending replay data to a candidate provider exports it [S40][V].
- **Decision:** Add BB21: local-first scoring, redaction and rephrasing, an audited residual-leakage bound that blocks sets above the policy limit, provider data-use checks, and provenance for every set.
- **Consequences:** Unblocks legal and privacy review; adds latency and sampling cost; leakage is measured and reported, never assumed zero.
