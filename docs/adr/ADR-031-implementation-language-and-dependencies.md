# ADR-031: Implementation language and dependency policy

- **Status:** Proposed
- **Context:** M0 needs fast iteration on statistics, a small auditable verifier and easy Codespaces setup.
- **Decision:** Python 3.12 for the engine, tests and CLI; numpy and scipy for statistics; cbor2 and cryptography for signed statements. The verifier (omc_verify) depends only on cbor2 and cryptography and does not import the engine, so auditors can review a very small code base. Revisit Rust or Go for the in-line policy service when latency requires it (A4).
- **Consequences:** Fast development; Python packaging in customer tenants; a later rewrite of the hot path is possible without changing statements or the verifier.
