# OMC architecture documentation (arc42) v0.4

Version 0.4, 27 October 2026. Supersedes v0.3. Merges Round 11 research: human-access compliance deadlines, developer-tool crowding, replay privacy, channel economics.

| File | arc42 section |
|---|---|
| 01-introduction-and-goals.md | 1 |
| 02-constraints.md | 2 |
| 03-context-and-scope.md | 3 |
| 04-solution-strategy.md | 4 |
| 05-building-blocks.md | 5 |
| 06-runtime-view.md | 6 |
| 07-deployment-view.md | 7 |
| 08-crosscutting-concepts.md | 8 |
| 09-architecture-decisions.md | 9 (index; records live in `docs/adr/`) |
| 10-quality-requirements.md | 10 |
| 11-risks-and-technical-debt.md | 11 |
| 12-glossary.md | 12 |
| appendix-a-competitive-position.md | Appendix A |
| appendix-b-roadmap.md | Appendix B |
| appendix-c-evidence.md | Appendix C |
| appendix-d-open-items.md | Appendix D |
| appendix-e-business-model.md | Appendix E |

Conventions: source tags `[S#]` resolve in Appendix C; `[V]` marks vendor or secondary sources to verify before external use; assumptions are `A#`; every product number carries an evidence grade E0 to E3.

## What changed from v0.3

- **Human access and disclosure compliance audit** (ADR-027): measures disclosure, time to a human, escalation success and trapped-loop rate against new chatbot laws (California AB 1609 from 1 January 2027, Spain Law 10/2025 by 28 December 2026, EU AI Act Article 50), with intervals and signed evidence.
- **Interoperate with developer tools** (ADR-028): import adapters for Langfuse, LangSmith, Braintrust, Kitaru and similar exports, and a CI/CD promotion gate that returns a signed verdict. OMC does not build replay or evaluation runners.
- **Replay Privacy Gate** (ADR-029): local-first scoring, redaction and rephrasing, and measured residual leakage before any provider call.
- **Channel strategy** (ADR-030): marketplace listings and co-sell where they shorten procurement, under the independence rules.
- Decision D7 approved: ADR-022 to ADR-026 are Accepted. EU Digital Omnibus on AI reported published (July 2026), removing one verification item.
- New building blocks BB21 and BB22; runtime scenarios R16 to R18; risks R31 to R36; quality scenarios Q22 to Q25; requirements FR25 to FR27; Appendix E gains channel economics and a valuation reality check.

## What changed from v0.2

- Third entry product: **action authority audit** (refunds, credits, discounts and data access checked against policy authority, with leakage estimated in currency).
- **Assurance-ecosystem alignment** (ADR-022): statements mapped to AIUC-1, ISO/IEC 42001, SOC 2 and NIST AI RMF controls; partner interface for CPA firms, certifiers and insurers; OMC issues evidence, never certificates.
- **Public verifier, schema and test vectors** (ADR-025) and **Review Workbench** with customer-supplied gold labels (ADR-024).
- **Packaging and pricing principles** (ADR-026) and Appendix E (business model, hypotheses only).
- Building blocks BB19 and BB20; runtime scenarios R13 to R15; risks R26 to R30; quality scenarios Q18 to Q21; requirements FR21 to FR24.

## What changed from v0.1 (v0.2 summary)

- Beachhead chosen: customer-support ticket resolution (AI-handled and AI-assisted), IT service desk second (ADR-017).
- Entry products: certified model migration qualification (ADR-011, ADR-019) and outcome billing audit with continuous vendor bake-off (ADR-020).
- Evidence Statements become SCITT signed statements (COSE_Sign1 over a canonical payload) registrable in a transparency service (ADR-018, ADR-015).
- Independence charter accepted (ADR-016), including a no-contingent-fee rule.
- New action-level disagreement concept for generative agents (ADR-021).
- Building blocks BB15 to BB18 added; runtime scenarios R9 to R12; risks R15 to R24; quality scenarios Q12 to Q17.
