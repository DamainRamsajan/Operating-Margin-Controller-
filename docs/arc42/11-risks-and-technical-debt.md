# 11. Risks and technical debt

## 11.1 Risks

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Competitive convergence: suites, labs and process-intelligence vendors add ROI and decision features | High | High | Independence; certified audits; open evidence; ingest rather than rebuild mining |
| R2 | Estimator validity: poor overlap or positivity | Medium | High | Exploration floors, power analysis, grades |
| R3 | Label scarcity and delay | High | Medium | Active and prediction-powered sampling, override labels, disagreement-only labeling, fast-outcome beachhead |
| R4 | Interference from congested human queues biases estimates | Medium | Medium | Queue-aware estimators, BB8 |
| R5 | Regulatory classification (employment use case) and Omnibus timing | Medium | High | ADR-007, counsel review, track publication |
| R6 | Method maturity: conformal policy control, prediction-powered causal inference and anytime-valid audits are recent; the paired-audit paper is a single-author preprint validated on classification | Medium | High | Feasibility spikes, synthetic validation, simpler guarded rollouts as fallback |
| R7 | Integration cost and drift into consulting | High | High | Pilot kit, connector library, strict scope, paid integration |
| R8 | Small-team capacity | High | High | Modular monolith, staged roadmap, early statistics and proof engineer |
| R9 | Goodhart effects and metric gaming | Medium | High | Guardrail metrics, permanent reference lane, several outcome definitions |
| R10 | Ownership conflict between IT and finance | Medium | Medium | Finance co-owner from day one; replay tooling |
| R11 | Provider opacity: silent model changes, no attestation | High | Medium | Behavior-based regime detection; certified audits on unplanned shifts |
| R12 | Cross-tenant benchmarks raise legal and competitive sensitivities | Medium | Medium | Opt-in; aggregates only; Phase 3 |
| R13 | Pricing conflict of interest | Medium | High | ADR-009, ADR-010, ADR-016, ADR-020 |
| R14 | Telemetry and protocol standards churn | High | Low | Adapters (ADR-001) |
| R15 | Suite bundling (ServiceNow, Salesforce) | High | High | Certified connectors; independence; evidence grades |
| R16 | Lab-owned context and evaluation layers | Medium | High | Lab-agnostic evidence; auditor-style independence |
| R17 | Crowded context-graph category | High | Medium | Causal, graded traces; do not compete on mapping |
| R18 | Judge failure and reward hacking in label pipelines | Medium | High | Judge rule (8.14); gold audits; judge-drift monitoring |
| R19 | Simulation validity | Medium | Medium | Input to inference only (ADR-014) |
| R20 | Open-spec strategy gives away the format | Low | Medium | Keep reference implementation, data asset and integrations proprietary; align to SCITT so the format is a profile, not a fork |
| R21 | Dependence on customer logs with outcomes | Medium | Medium | Grade E1 where labels are missing; ingest first |
| R22 | Vendor data-sharing terms block shadow scoring or exports | Medium | High | Contract templates; export-based audits; start with customer-owned models and gateways |
| R23 | Free-text agents fall outside the certified-audit theory | High | Medium | Action-level disagreement (ADR-021); residual text quality graded E2 |
| R24 | Standards in draft: SCITT profile for agent receipts is an individual draft; COSE post-quantum algorithm support unverified | Medium | Low | Pin versions; schema isolates the payload; re-profile when drafts mature |
| R25 | Billing audit strains vendor relationships and customer contracts | Medium | Medium | Customer-initiated only; definitions side by side; fixed fees; legal template for dispute packs |
| R26 | Assurance incumbents extend live agent testing to outcomes and change safety [S31][V] | Medium | High | Partner posture, open verifier, control mappings, published methodology |
| R27 | Trust damage from low-quality automated assurance (an alleged certificate-mill case in 2026) [S34][V] | Medium | Medium | Reproducible evidence, no sale of certificates, replication studies |
| R28 | Partner arrangements compromise independence | Low | High | No referral fees contingent on findings; disclose relationships (ADR-026) |
| R29 | Dependence on customer experts' availability for gold labels | Medium | Medium | Disagreement-only and prediction-powered sampling; QA-tool labels; time-boxed budgets |
| R30 | Authority rules are undocumented or inconsistent | High | Medium | Rule registry; elicit with owners; grade E1 where rules are inferred |
| R31 | Compliance evidence is mistaken for legal advice, or rule interpretation is wrong [S37][V] | Medium | High | Rule sets entered by counsel; statements avoid legal conclusions (8.20); counsel-reviewed templates |
| R32 | Developer tools commoditize the migration wedge; open-source gates are free [S39][V] | High | High | Interoperate (ADR-028); differentiate on certified verdicts, business parity, independence, signed evidence |
| R33 | Residual privacy leakage in replay sets, or provider retention of customer data [S40][V] | Medium | High | Replay Privacy Gate; measured leakage bounds; local-first scoring; provider terms checks |
| R34 | Marketplace dependence and fee pressure; bundling by marketplace owners [S41][V] | Medium | Medium | Several marketplaces; direct sales for entry tiers; independence rules for incentives (ADR-030) |
| R35 | Scope creep across four modules for a small team | High | High | Shared machinery; strict phase gates; compliance module limited to measurement |
| R36 | Rapidly changing state and national chatbot laws [S37][V] | High | Medium | Rule sets as versioned data; counsel owns mappings; no hard-coded thresholds |

## 11.2 Technical debt to track from day one

Adapter backlog per source version; estimator versions requiring re-runs; schema migrations; policy-table precompute; signature-algorithm agility; material-difference classifier versions; assumption register upkeep.
