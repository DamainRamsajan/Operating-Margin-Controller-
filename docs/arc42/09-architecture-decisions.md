# 9. Architecture decisions

Records live in `docs/adr/`. Status as of 27 October 2026. Accepted: ADR-011, 015, 016, 017 and 022 to 026 (founder decisions D1 to D3 and D7, and the delegated beachhead).

| ADR | Title | Status |
|---|---|---|
| 001 | Canonical object-centric event model behind anti-corruption adapters | Proposed |
| 002 | Log propensity, candidate set and feasible set for every decision | Proposed |
| 003 | Safe-policy-first actuation | Proposed |
| 004 | Customer-tenant data plane with a hosted control plane | Proposed |
| 005 | Decision layer over abstract options | Proposed |
| 006 | Estimator isolation and registry | Proposed |
| 007 | No individual-level worker scoring | Proposed |
| 008 | Evidence Vault with hybrid post-quantum signatures and re-anchoring | Proposed (extended by 018) |
| 009 | Pre-registered measurement plans and customer-rerunnable estimators | Proposed |
| 010 | Outcome-linked pricing with a cap and ramp | Proposed (constrained by 016, 020) |
| 011 | Safe model migration and qualification as the entry wedge | **Accepted** |
| 012 | Evidence-weighted decision traces (Precedent Store) | Proposed |
| 013 | MCP and A2A as first-class surfaces | Proposed |
| 014 | Simulation only as an input to inference | Proposed |
| 015 | Open Evidence Statement specification | **Accepted** (design-partner review before publication) |
| 016 | Independence charter | **Accepted** |
| 017 | Beachhead: customer-support ticket resolution | **Accepted** (delegated decision) |
| 018 | Evidence Statements as SCITT signed statements | Proposed |
| 019 | Disagreement-supported certified migration audits | Proposed |
| 020 | Outcome billing audit and vendor bake-off | Proposed |
| 021 | Action-level disagreement for generative agents | Proposed |
| 022 | Assurance-ecosystem alignment and partner channel | **Accepted** (D7) |
| 023 | Action authority audit | **Accepted** (D7) |
| 024 | Customer-labeled gold and Review Workbench | **Accepted** (D7) |
| 025 | Public verifier, schema and test vectors | **Accepted** (D7) |
| 026 | Packaging and pricing principles | **Accepted** (D7) |
| 027 | Human access and disclosure compliance audit | Proposed (spike S-j) |
| 028 | Interoperate with developer tools: import adapters and CI promotion gate | Proposed |
| 029 | Replay Privacy Gate | Proposed (spike S-k) |
| 030 | Channel strategy: marketplaces and co-sell under independence rules | Proposed |

ADRs 001 to 010 move to Accepted as the Phase 0 spikes in Appendix D complete.
