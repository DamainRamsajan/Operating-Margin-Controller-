# 4. Solution strategy

## 4.1 Strategy overview

| Quality goal | Approach | Detail |
|---|---|---|
| Causal credibility | Propensity-logged randomized policies inside safe sets; doubly robust estimators; prediction-powered inference when labels are scarce [S9]; queue-aware designs when review is congested [S10]; pre-registered plans | 5.3, ADR-002, ADR-006, ADR-009 |
| Bounded risk | Safe-policy-first actuation anchored on the baseline [S8]; hard constraints for mandatory human steps; kill switch | 5.2, 5.4, ADR-003 |
| Time to value and low labeling cost | Read-only connectors; certified paired audits that need zero labels for benign updates and label only material disagreements [S29] | 5.7, ADR-011, ADR-019 |
| Change tolerance | Anti-corruption ingestion; decision layer over abstract options; model identity as data; a model change is an intervention | 4.5, ADR-001, ADR-005 |
| Sovereignty and privacy | Customer-tenant data plane; workflow-level units; no individual scoring | 7, ADR-004, ADR-007 |
| Evidence longevity and verifiability | Statements as signed, transparency-registered records; hybrid post-quantum signing; re-anchoring | 5.5, ADR-008, ADR-018 |
| Independence and moat | Open schema, independence charter, no contingent fees, certified connectors | ADR-015, ADR-016 |
| Ecosystem fit and low switching friction | Import adapters and a CI gate for developer tools; marketplace listings; partner program | ADR-022, ADR-028, ADR-030 |
| Privacy of replay data | Replay Privacy Gate: local-first scoring, redaction and rephrasing, measured residual leakage | ADR-029 |

## 4.2 Two planes

The **data plane** runs inside the customer tenant: ingestion, event store, work twin, risk model, policy engine, actuation, migration gate, outcome audit, ledger computation and evidence vault. The **control plane** is hosted: estimator registry, model and price catalog, deprecation-feed aggregation, console API, update service and optional aggregate benchmarks. Control-plane access to the data plane is pull-based and limited to metadata and aggregates.

## 4.3 Decision-point and enforcement-point pattern

OMC is a policy decision point. Customer routers, agent platforms and workflow engines are enforcement points. This keeps OMC out of the execution path in advisory mode, makes in-line mode a thin API call, and lets the customer revoke authority by disabling a single integration.

## 4.4 Evidence grades

| Grade | Meaning | Typical source |
|---|---|---|
| E3 | Randomized or anytime-valid certified, audited, overlap verified | Propensity-logged exploration, switchbacks, certified paired audits with predictable label routing |
| E2 | Quasi-experimental or label-augmented | Natural variation with checked overlap; prediction-powered estimates |
| E1 | Observational with stated bounds | Shadow-mode estimates under partial identification |
| E0 | Projection or simulation | Work-twin what-if scenarios |

Savings used for billing or board reporting must be E2 or better (ADR-009). Migration certificates are E3 only when label routing is predictable (it never reads the outcome) and the loss class is within the audit's stated scope (ADR-019, ADR-021).

## 4.5 Designing for change

| Change | Effect on OMC | Design response |
|---|---|---|
| Agents become far more reliable | Fewer human steps; decisions shift to process redesign | Generic options catalog (executor, configuration, review policy) |
| Protocols and telemetry churn | Ingestion breaks | Anti-corruption layer; versioned adapters; canonical model |
| Inference prices fall | Run-cost term shrinks | Cost model is data-driven; risk and value terms dominate |
| Suites and labs bundle ROI features | Overlap with dashboards | Independence, evidence grades, certified audits, customer-rerunnable proof |
| Providers retire or silently update models | Policies drift | Exposure inventory, certified qualification, model identity per decision, regime shift handling |
| Regulation tightens or loosens | Logging and oversight duties change | Evidence vault and oversight packs built in; finance-grade value remains |
| Quantum threat to signatures | Historical records forgeable | Hybrid post-quantum signing and re-anchoring from day one |
| Vendors consolidate (for example, a helpdesk vendor acquired by a suite) | Vendor-defined outcomes harder to challenge | Independent outcome audit and bake-off |

## 4.6 Three-year resilience plan (2026 to 2029)

| Threat | Timing | Response |
|---|---|---|
| Suites bundle ROI and optimization (ServiceNow measure views, Salesforce AI control plane) | 2027 | Be the measurement authority inside them through certified connectors; independence and grades as the differentiator |
| Labs own business context and evaluation and sell outcome-priced agents | 2027 to 2028 | Lab-agnostic evidence; auditor-style independence |
| A process-intelligence leader adds rigorous causal methods | 2027 to 2028 | Ship first with an open, standards-based statement format; ingest rather than rebuild mining; lead on safe actuation |
| Judging and simulation commoditize evaluation | 2027 onward | Judges and simulators are inputs; validity never depends on them; the asset is calibration and causal design |
| Agents become reliable enough to remove humans | 2028 onward | Option abstraction; risk gate remains; shift to process redesign |
| Outcome-pricing definitions tighten after disputes | 2027 onward | Audit module becomes a dispute-evidence service |
| Standards settle (MCP, A2A, SCITT, OpenTelemetry) | Continuous | First-class surfaces and adapters |
| Quantum threat to signatures | 2029 to 2035 | Algorithm agility and re-anchoring |
| Assurance incumbents (certifiers, CPA firms, insurers) add outcome and change measurement to live-testing programs | 2027 to 2028 | Be their evidence substrate: control mappings, partner interface, open verifier |
| Quality scandals in automated assurance reduce trust in fast, cheap attestations [S34][V] | 2026 onward | Reproducible, human-verifiable evidence; replication studies; no sale of certificates |
| Open-source and developer tools commoditize replay, shadow and gating [S39][V] | Now | Do not compete there; import their output; differentiate with certified verdicts, business-metric parity, independence and signed statements |
| Marketplace and suite-controlled distribution, fee pressure [S41][V] | 2027 onward | List on several marketplaces; sell entry products directly; apply independence rules to any co-sell incentive |
| Chatbot-law changes (new states, amended thresholds) [S37][V] | Continuous | Compliance module is parameterized by rule sets; counsel maps statutes to measurements |
| Open-source clones of the ledger | 2028 onward | Standard, per-tenant data asset, integration depth, independence |

**Moat stack:** independence, open standards-based evidence, certified label-efficient audits, propensity-logged history, per-workflow calibration, certified suite connectors, compliance packs, customer-owned evidence.

## 4.7 Entry wedge

Three linked products and one compliance module land first in support workflows:

1. **Certified model qualification.** Exposure inventory, qualification set, shadow scoring with both models, a zero-label certificate when the models rarely disagree, and a label-efficient audit of material disagreements otherwise, followed by a canary lane and a signed pack (section 6.9).
2. **Outcome billing audit and bake-off.** Independent estimate of the true accepted-outcome rate against billed outcomes, then randomized comparison of vendors and models on identical traffic (sections 6.10 and 6.11).
3. **Action authority audit.** Independent estimate of money moved outside policy authority, with guardrail ceilings calibrated from the data and a liability evidence pack (section 6.13).
4. **Human access and disclosure compliance audit (module).** Statistical measurement of disclosure, time to a human, escalation success and trapped-loop rate against the rules the customer must meet, with signed evidence (section 6.16). Much of it is deterministic (timestamps), so it is cheap to build and has near-term deadlines.

Their artifacts (baseline, replay set, propensity-logged canary, outcome labels, signed statements) seed the full controller.

## 4.8 Moat architecture

| Moat element | What it is | Why it holds | Build step |
|---|---|---|---|
| Independence | Charter, no contingent fees, disclosed relationships | Vendors, suites, labs and some certifiers sell what they would assess | ADR-016 |
| Verifiable evidence | SCITT signed statements plus a public, open-source verifier and test vectors | Anyone can check a claim without trusting OMC; the format can become a reference | ADR-018, ADR-025 |
| Assurance-ecosystem fit | Statements mapped to AIUC-1, ISO/IEC 42001, SOC 2 and NIST AI RMF controls; partner interface | Certifiers verify controls and agent behavior but do not measure outcome truth, change safety or action authority; OMC supplies that evidence [S31][V] | ADR-022 |
| Certified, label-efficient methods | Disagreement-supported audits, prediction-powered estimation, anytime-valid verdicts, published methodology and replication | Hard to copy quickly; credibility compounds with each replication | ADR-019 |
| Operational embedding | Daily use for migrations, billing, action audits and bake-offs, not only at audit time | Compliance-automation vendors show very low direct switching once embedded in internal processes [S34][V] | Phases 0 to 2 |
| Own your evidence, rent our engine | Customers hold their evidence and can verify it without OMC | Lowers lock-in fear and speeds sales; stickiness comes from workflow integration and calibration history | 8.17 |
| Interoperability | Import adapters, CI promotion gate, MCP surface | Fits the tools teams already use, so OMC adds a verdict layer instead of replacing tooling | ADR-028 |
| Data asset | Propensity-logged history, per-workflow calibration, material-difference classifiers per domain | Compounds only after deployment | ADR-002 |

## 4.9 Business model principles

1. Fixed-fee entry products with a short sales cycle; subscription by workflow and module once embedded; partner-delivered attestations priced by the partner; nothing contingent on findings (ADR-016, ADR-026).
2. Gold labels come from customer experts and partner QA tools through the Review Workbench, so label labor never becomes OMC's cost of goods (ADR-024).
3. Compute-light estimators and disagreement-only labeling keep marginal cost low; shadow-scoring inference is a capped, customer-billed pass-through shown in the cost model (8.10).
4. Expand by module, not by custom work: Qualify, Audit, Control, Comply (Appendix E).
5. Distribute through marketplaces and co-sell where they shorten procurement, applying the independence rules to any partner incentive (ADR-030).
