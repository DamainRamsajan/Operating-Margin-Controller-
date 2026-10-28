# 2. Architecture constraints

| ID | Constraint | Consequence |
|---|---|---|
| TC1 | Customer-tenant data plane | Raw case data never leaves the tenant by default; the control plane receives metadata and aggregates only |
| TC2 | Read-only through Phase 1 | Value is shown before any production change is requested |
| TC3 | No hard dependency on any model provider or agent platform | Decision layer works on abstract options; vendors sit behind adapters |
| TC4 | OpenTelemetry GenAI conventions were still in Development status with no stable release as of August 2026 [S6] | Ingestion uses an anti-corruption layer into an internal canonical model |
| TC5 | Propensity logging from the first actuated decision | Without it, logged data is confounded and causal claims fail |
| TC6 | Small team | Modular monolith in the data plane first; split services only on proven need |
| TC7 | Helpdesk and vendor APIs have rate limits, data-use terms and uneven export coverage | Connectors budget calls, cache incrementally and degrade to file exports |
| TC8 | Routing for label requests must never read the outcome label | Routing rules are pre-label functions only; enforced in the Label Service (ADR-019) |
| OC1 | Staged delivery (Appendix B) | Each phase must stand alone commercially |
| OC2 | Pricing may be tied to audited savings | Estimators must be reproducible by the customer's finance team (ADR-009) |
| OC3 | Independence charter (ADR-016) | No fees contingent on a specific vendor's results; no sale of agents or models |
| RC1 | EU AI Act: Annex III high-risk obligations moved to 2 December 2027 under the Digital Omnibus; Article 12 requires automatic logs kept at least six months, Article 18 ten-year documentation retention, Article 14 human oversight, Article 26 deployer duties including worker information [S5][S7][S38]; the Omnibus is reported published on 24 July 2026 and in force from 27 July 2026 (one secondary source; confirm on EUR-Lex [V]) | Evidence Vault, oversight design and retention defaults |
| RC2 | Allocating tasks based on individual behavior or traits, or monitoring individual worker performance, is an Annex III employment use case [V: counsel review] | No individual-level inputs or outputs by default (ADR-007); QA scores are ingested only in aggregate or as case-level labels |
| RC3 | GDPR and national works-council rules | Pseudonymization, purpose limitation, aggregate reporting units |
| RC4 | Sector overlays (financial model-risk management, operational-resilience rules) [V] | Estimator governance and change control must be auditable |
| RC5 | Customer-facing chatbots carry AI-disclosure duties (Article 50 transparency, in force since August 2026) [S7] | Evidence packs record disclosure configuration as context; duty stays with the deployer |
| OC4 | Gold labels come from customer experts and partner QA tools, not OMC staff | Cost-of-goods control and independence; Review Workbench required (ADR-024) |
| RC6 | Assurance frameworks (AIUC-1, ISO/IEC 42001, SOC 2, NIST AI RMF) are the language buyers, auditors and insurers use [S31][S32][V] | Statements carry control mappings; OMC issues evidence, never certificates (ADR-022) |
| RC7 | Chatbot disclosure and human-access laws: California AB 1609 (signed 28 September 2026, applies from 1 January 2027 to businesses above $500 million revenue), Spain Law 10/2025 (compliance deadline 28 December 2026), EU AI Act Article 50 (since 2 August 2026), and state laws in Utah, Maine and Colorado [S37][V] | OMC produces measurement evidence only; counsel interprets applicability; evidence packs avoid legal conclusions |
| TC9 | Provider data-use terms govern whether replay or shadow data may reach a candidate model | Replay Privacy Gate checks retention and training terms before any provider call (ADR-029) |
| CV1 | Conventions | arc42, C4-style views, ADRs in `docs/adr/`, semantic versions for schemas and estimators |
