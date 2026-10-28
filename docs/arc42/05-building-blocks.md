# 5. Building block view

## 5.1 Level 1: overall system

```
DATA PLANE (customer tenant)
  Connectors -> Ingest and Normalize -> Canonical Event Store
                                              |
        +-------------+-------------+---------+---+-------------+
     Work Twin   Unit Economics   Outcome and   Risk Model   Capacity Model
        |             |           Label Service      |             |
        +-------------+-------------+--------------+-------------+
                              Policy Engine (decision point)       Migration Gate
                                   |              ^               Outcome Audit and Bake-off
                      Actuation Gateway ----> enforcement points (customer systems)
                                   |
                             Causal Ledger -> Evidence Vault -> Transparency service

CONTROL PLANE (hosted)
  Estimator Registry | Model and Price Catalog | Deprecation Feeds | Console API | Update Service | Aggregate Benchmarks (opt-in)
```

| ID | Building block | Responsibility | Key interfaces | Phase |
|---|---|---|---|---|
| BB1 | Connector Layer | Read-only adapters to helpdesks, agent platforms, gateways, vendor billing, QA tools; credentials; incremental sync | Source APIs in, raw events out | 0 |
| BB2 | Ingest and Normalize | Anti-corruption mapping to the canonical model; schema versioning; dedup; pseudonymization at the edge | Raw in, canonical out | 0 |
| BB3 | Canonical Event Store | Append-only object-centric events and decision records; columnar files plus metadata DB; time travel | Query API, export (OCEL, Parquet) | 0 |
| BB4 | Work Twin | Process graph, variants, exceptions, case classes, step catalog; currency annotations; leak ranking; what-if (E0) | Reads BB3, BB5 | 0 |
| BB5 | Unit Economics Engine | Cost lines to cases; cost per accepted outcome; net value per case and step | Cost and price catalog | 0 |
| BB6 | Outcome and Label Service | Outcome definitions; gold, override, judge, surrogate and QA labels; active gold sampling with pre-label routing only; latency tracking; hosts the Review Workbench (BB20) | Label queue, review tools | 1 |
| BB7 | Risk Model | Calibrated error probability and severity; conformal wrappers; adaptive recalibration; drift and regime detection | Feeds BB9, BB11, BB15 | 1 |
| BB8 | Capacity Model | Review queues, service rates, congestion; experiment windows | Feeds BB9, BB11 | 2 |
| BB9 | Policy Engine | Options, constraints, risk gate, optimizer, exploration, propensity logging, fallback | Decision API | 2 (shadow in 1) |
| BB10 | Actuation Gateway | Shadow, advisory, gated and canary modes; adapters; idempotency; kill switch | Decision API | 2 (canary in 1) |
| BB11 | Causal Ledger | Runs estimators; stores plans; assigns grades; composes statements; replays | Registry, vault | 1 to 2 |
| BB12 | Evidence Vault | Hash chain, hybrid signatures, SCITT registration, anchoring, retention, offline verifier | Append API, verifier CLI | 0 |
| BB13 | Console and Reporting | Role views; approvals; evidence packs; audit replay | Console API | 0 to 2 |
| BB14 | Governance and Tenancy | Identity, roles, policy-as-code, change approval, audit of OMC | OIDC, SAML, SCIM | 0 |
| BB15 | Migration Gate | Exposure inventory; qualification set; shadow comparator; certified paired audit; canary controller; retirement calendar; CI promotion gate and import adapters | BB3, BB6, BB7, BB9, BB10, BB11, BB12, BB21 | 0 to 1 |
| BB16 | Precedent Store (Proposed) | Decision traces with grade, provenance, versions, access scope, expiry | MCP, console | 2 |
| BB17 | Simulation Twin (Proposed) | Calibrated simulator used only as an input to inference | BB11 | 3 |
| BB18 | Outcome Audit and Bake-off | Vendor outcome definitions as data; true-outcome estimation; billing reconciliation; randomized vendor and model comparison; Contract Evidence Pack (Proposed) | BB1, BB6, BB9, BB11 | 1 to 2 |
| BB19 | Action Authority Audit | Authority rules as data; consequential-action extraction; authority checks; leakage estimation in currency; guardrail calibration; liability evidence pack | BB1, BB6, BB7, BB11, BB12 | 1 |
| BB20 | Review Workbench and Partner Interface | Expert labeling queue with blinded comparisons; public verifier, schema, test vectors; read-only partner API; control mappings | BB6, BB12, BB13 | 1 |
| BB21 | Replay Privacy Gate | Local-first scoring; redaction and rephrasing; residual-leakage audit; provider data-use checks; replay-set provenance | BB1, BB2, BB6, BB15 | 0 to 1 |
| BB22 | Compliance Evidence Module | Human-access and disclosure audit: rule sets as data, event extraction, deterministic timing checks, sampled review, trapped-loop detection, compliance statements | BB1, BB6, BB11, BB12 | 1 |

Control-plane blocks: CP1 Estimator Registry (signed, content-addressed images), CP2 Model and Price Catalog, CP3 Deprecation Feeds, CP4 Console API, CP5 Update Service, CP6 Aggregate Benchmarks (opt-in, aggregate only).

## 5.2 Level 2: Policy Engine (BB9)

| Component | Responsibility |
|---|---|
| Options Catalog | Executors per step: human, model class, agent configuration, vendor agent, tool pipeline, each with a review policy. Vendor specifics live in adapters |
| Constraint Compiler | Policy-as-code into hard constraints (mandatory human steps, residency, regulation) and soft constraints (cost, latency) |
| Risk Gate | Removes options whose calibrated risk bound exceeds the budget; baseline always retained |
| Optimizer | Scores feasible options by expected net value; learns online within the feasible set |
| Exploration Scheduler | Lane assignment by hash of case reference (reference, exploit, explore); action-probability floor; windows from BB8 |
| Propensity Logger | Selection probability, candidate and feasible sets |
| Fallback Controller | Baseline on timeout, error, breach or kill switch |

In-line latency target: p99 of 250 ms or less using precomputed policy tables (A4). A timeout returns the baseline.

**Decision record.**

| Field | Purpose |
|---|---|
| decision_id, case_ref (pseudonymous), workflow_id, step_id, case_class | Identity and aggregation keys; no person identifiers |
| context_ref | Hash of the feature snapshot in BB3 |
| candidate_set, feasible_set, chosen_option | What was possible, allowed, picked |
| propensity, lane | Selection probability; reference, exploit or explore |
| policy_version, plan_id | Policy build and measurement plan |
| risk_estimate | Calibrated probability with interval |
| constraints_active | Constraints applied |
| model_identity | Provider, model, version or hash, attestation reference if available |
| mode, timestamps | Shadow, advisory, gated or canary; request and decision times |

## 5.3 Level 2: Causal Ledger (BB11)

Components: Estimator Runner (isolated, no egress, pinned digests), Measurement Plan Store (signed before data collection), Evidence Grader, Statement Composer, Replay Verifier.

| Estimator family | Use | Grade | Needs |
|---|---|---|---|
| IPW and doubly robust (AIPW) | Randomized or logged-propensity decisions | E3 | Propensities, verified overlap |
| Prediction-powered causal inference and active PPI | Scarce or delayed labels, abundant judge or surrogate labels | E2 to E3 | Small gold sample, calibrated outcome model [S9] |
| Queue-aware and switchback estimators | Congested review so units interfere | E3 under congestion | Queue model or random-duration windows [S10] |
| Certified paired audit (disagreement-supported, anytime-valid) | Model updates with prediction-determined or action-level losses | E3 | Both models shadow-scored; pre-label routing [S29] |
| Equivalence and non-inferiority tests | Business-metric parity of a swap | E2 to E3 | Margin set by owner; sequential design |
| Sequential OPE with mediators | Multi-step workflows | E2 | Step-level logging [S11] |
| Observational with partial identification | Shadow mode with a deterministic baseline | E1 | Sensitivity analysis |
| Simulation and projection | What-if | E0 | None; labeled as projection |

Outputs: estimate, interval, grade, assumptions, sample sizes (power analysis that accounts for prediction-powered gains), replay references.

## 5.4 Level 2: Risk Model (BB7)

- Granularity: workflow, step, case class and option. Never a person.
- Outputs: error probability, severity distribution, upper bound per option.
- Calibration: conformal wrappers; where exchangeability fails, wrappers widen and the gate tightens [S8]. After model-identity changes, adaptive recalibration restarts windows.
- Labels: gold audits, human overrides (a cheap structural label), judge scores corrected by prediction-powered inference, QA scores as case-level surrogates, downstream outcomes.
- Judge rule: judges may steer where labels are spent but never replace gold evidence in a certificate (section 8.14).
- Regime detection: model identity changes, provider notices, residual drift tests, rule-change flags.

## 5.5 Level 2: Evidence Vault (BB12)

| Concern | Design |
|---|---|
| Statement format | Evidence Statements are SCITT signed statements: COSE_Sign1 over a canonical (JCS) payload; the schema is open and versioned (ADR-015, ADR-018) [S28] |
| Integrity | Per-tenant hash chain with Merkle batches; registration in a transparency service gives receipts and non-equivocation that a self-signed chain cannot provide alone |
| Authenticity | Hybrid signatures: classical plus ML-DSA (FIPS 204); SLH-DSA (FIPS 205) for long-lived anchor roots [S16]; COSE support for post-quantum algorithms to be verified [V] |
| Time | Transparency receipts plus periodic RFC 3161 anchoring; old heads re-anchored before algorithms weaken |
| Storage | Immutable object storage with retention locks; keys in HSM or KMS |
| Retention | Logs at least 6 months (Article 12), documentation 10 years (Article 18); customer may extend [S5] |
| Verification | Offline verifier CLI usable by auditors without OMC services |

## 5.6 Level 3: canonical entities

| Entity | Key attributes |
|---|---|
| Case | case_ref, workflow_id, case_class, opened and closed times, value drivers |
| Step | step_id, type, expected duration, mandatory-human flag |
| Decision | See 5.2 |
| Execution | Executor type, configuration reference, model identity, tokens or minutes, tool calls |
| CostLine | Source, amount, currency, attribution tags |
| Outcome | Definition id, value, observed time, accepted flag |
| VendorOutcomeClaim | Vendor, vendor definition id (confirmed, assumed), billed amount, case_ref |
| Label | Source (gold, override, judge, surrogate, QA), value, confidence, latency |
| ModelIdentity | Provider, model, version, hash or attestation reference, first-seen time, announced retirement date |
| PolicyVersion | Options, constraints, risk budget, approvals |
| MeasurementPlan | Hypothesis, estimator and version, outcome definitions, exclusions, signed time |
| Audit | Tolerance, confidence, tiers, verdict, stopping time, labels spent, per-slice table |
| Statement | Estimate, interval, grade, assumptions, evidence references, signatures |
| AuthorityRule | Rule id, action type, limits, eligibility, source document, version, effective dates |
| ConsequentialAction | Action type, amount, currency, case_ref, executor, authority rule matched, authorized flag, review label |
| ControlMapping | Statement type, framework, control id, evidence requirement, mapping version |
| HumanRequestEvent | case_ref, channel, request time, human-connect time or scheduled time, queue time, outcome |
| DisclosureEvent | case_ref, channel, disclosure text reference, presence flag, timing in the interaction |
| EscalationOutcome | case_ref, attempts to reach a human, loop indicator, resolution path |
| ReplaySetProvenance | Source window, sampling plan, redaction pipeline version, residual-leakage estimate, provider terms checked |

## 5.7 Level 2: Migration Gate (BB15)

| Component | Responsibility |
|---|---|
| Exposure Inventory | From ModelIdentity logs and deprecation feeds: workflows, volume, spend and retirement date per model version |
| Qualification Set Builder | Stratified historical cases by case class plus hard cases and recent drift |
| Shadow Comparator | Scores traffic with incumbent and candidate; computes the observable disagreement indicator at decision or action level (section 8.13) |
| Certified Auditor | Tier 0: zero-label certificate when the disagreement-rate upper bound is below tolerance. Tier 1: label only sampled material disagreements through an anytime-valid confidence sequence; per-slice verdicts; sequence-level error budget across promotions [S29] |
| Equivalence Tester | Business-metric parity with owner-set margins (accepted-outcome rate, cost per accepted outcome, cycle time) |
| Canary Controller | Randomized lane behind the risk gate with automatic rollback until retirement |
| Retirement Calendar | Alerts at notice, not at the shutdown reminder |

Scope note: the certified audit's theory covers losses determined by the prediction (classification, routing, action choice, exact-match). Open-ended judged text is outside it; section 8.13 reduces generative agents to action-level decisions and treats residual free-text quality as E2 prediction-powered evidence (ADR-021).

## 5.8 Level 2: Outcome Audit and Bake-off (BB18)

| Component | Responsibility |
|---|---|
| Definition Registry | Each vendor's outcome definition (for example confirmed versus assumed resolution) as versioned data |
| True-Outcome Estimator | Estimates the accepted-outcome rate with intervals from a gold-labeled sample, reopen and recontact signals and third-party QA or judge scores, using prediction-powered inference [S9] |
| Billing Reconciler | Compares billed outcomes with estimated true outcomes per vendor, definition and period; flags disputed segments |
| Bake-off Allocator | Randomized, propensity-logged allocation of live cases across vendors, models and the human baseline under the risk gate |
| Comparison Tester | Anytime-valid comparisons of vendors on identical traffic with per-slice verdicts |
| Dispute Evidence Pack | Signed statement with definitions, sample design and intervals, suitable for vendor negotiation |

Independence rules (ADR-016, ADR-020): fixed fees only, no contingency on findings, vendor relationships disclosed.

## 5.9 Level 2: Action Authority Audit (BB19)

| Component | Responsibility |
|---|---|
| Authority Rule Registry | Refund ceilings, eligibility windows, credit and discount limits, data-access scope and escalation thresholds as versioned data, sourced from policy documents and system configuration and confirmed by owners |
| Action Extractor | Consequential actions with amounts from helpdesk, billing and agent traces |
| Authority Checker | Deterministic checks where a rule is machine-checkable (amount above ceiling, outside window, duplicate with a chargeback credit); sampled expert review with prediction-powered correction where authority depends on context |
| Leakage Estimator | Rate and currency amount of actions outside authority, with intervals, by vendor, action type and case class |
| Guardrail Calibrator | Proposes ceilings and escalation thresholds from the loss distribution through the risk gate, with the review-load tradeoff from BB8 |
| Liability Evidence Pack | Signed statement for vendor disputes, insurers and auditors |

## 5.10 Level 2: Review Workbench and Partner Interface (BB20)

- **Review Workbench.** Queue for customer experts; blinded presentation when comparing vendors or models; visible sampling plan; time-boxed budgets; adjudication of disagreements; overrides recorded; label export with provenance.
- **Partner interface.** Public verifier CLI, schema and test vectors; read-only API for statements the customer chooses to share; control-mapping files that link statement types to AIUC-1, ISO/IEC 42001, SOC 2 and NIST AI RMF controls (mappings to be validated with a certifier [V]).

## 5.11 Level 2: Replay Privacy Gate (BB21)

| Component | Responsibility |
|---|---|
| Local-First Router | Scores with in-tenant or customer-controlled models where possible; sends only what passes the gate to external providers |
| Redactor | Pattern and context-aware redaction with placeholder restoration where needed |
| Rephraser | Semantic rephrasing of residual sensitive content for external scoring |
| Leakage Auditor | Estimates the residual leakage rate with intervals from a gold-reviewed sample, using prediction-powered correction [S9]; blocks a set whose upper bound exceeds the policy limit |
| Provider Terms Checker | Verifies retention, training and region terms for each external provider before any call (TC9) |
| Provenance Recorder | Writes ReplaySetProvenance for every set and links it to statements |

Published evidence shows that no single technique dominates and that residual leakage is nonzero (for example 0.6 percent residual PII leakage for local routing plus redaction plus rephrasing in one preprint [S40][V]), so OMC measures leakage instead of assuming it is zero.

## 5.12 Level 2: Compliance Evidence Module (BB22)

| Component | Responsibility |
|---|---|
| Rule Set Registry | Disclosure, human-request availability and time-to-human thresholds as versioned data per jurisdiction, entered and confirmed by counsel (for example California AB 1609 thresholds, Spain Law 10/2025 answer-time standards, EU Article 50 disclosure) |
| Event Extractor | Disclosure, human-request and escalation events from helpdesk, telephony and chat traces |
| Deterministic Checker | Timestamp-based checks: time to a human, queue time, scheduled-callback windows, availability during required hours |
| Sampled Reviewer | Expert review of disclosure wording, whether the request was recognized and trapped-loop indicators; prediction-powered correction for the rest [S9] |
| Compliance Estimator | Rates with intervals by channel, jurisdiction and period |
| Compliance Statement | Signed statement of measured results against the rule set, without legal conclusions |
