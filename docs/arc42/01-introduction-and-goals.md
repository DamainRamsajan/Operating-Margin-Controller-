# 1. Introduction and goals

## 1.1 Purpose

OMC is a closed-loop system that raises and proves the financial value of work shared between people, AI models and agents. For repeatable, high-volume workflows it runs four loops:

1. **Sense.** Reconstruct how the work really runs and where margin leaks, in currency.
2. **Price.** Estimate the calibrated risk and full cost of every step, including human review, tool calls and rework.
3. **Decide.** Choose which executor (human, model class, agent configuration, vendor agent or tool pipeline) handles each case, inside a declared risk budget, with the current process as the safe fallback.
4. **Prove.** Estimate the causal profit-and-loss effect with confidence intervals and an evidence grade, backed by signed, transparency-registered records that the customer's finance team and auditors can re-run without the vendor.

Verification of output correctness is an input to the risk term, not the product.

**Entry products.** OMC enters through three budgeted pains, plus one deadline-driven compliance module, that exercise the same machinery as the full controller:

- **Certified model migration qualification.** When a provider retires or silently changes a model, OMC certifies whether the replacement is no worse, at low labeling cost.
- **Outcome billing audit and vendor bake-off.** When vendors bill per outcome under their own definitions, OMC independently estimates the true accepted-outcome rate and compares vendors on identical traffic.
- **Action authority audit.** When AI agents issue refunds, credits or discounts, OMC independently estimates how much money moved outside policy authority and what guardrail ceilings the data supports.
- **Human access and disclosure compliance audit (module).** New chatbot laws require disclosure and timely access to a human (California AB 1609 from 1 January 2027, Spain Law 10/2025 by 28 December 2026, EU AI Act Article 50). OMC measures compliance with intervals and signed evidence; it does not give legal advice.

## 1.2 Problem statement

- Organizations report individual productivity gains but struggle to show enterprise-level financial impact [S1][V].
- AI spend overruns are common and tracking is near universal, yet tracking does not control cost; model tokens can be a minority of true per-case cost [S2][V].
- Agents fail on missing process context more often than on reasoning [S3][V].
- Human oversight is required by regulation and by practice, and attention-based oversight does not survive volume [S4][S5].
- Model versions retire on published calendars and change silently; re-qualifying production workflows is a recurring "re-qualification tax" that many enterprises delay [S22][V].
- Outcome-priced vendors define the billed outcome themselves; one leading vendor counts silence after an answer as a billable resolution, and vendor-claimed resolution rates run well above independent test results [S27][V].
- The assurance ecosystem (SOC 2, ISO/IEC 42001, AIUC-1 and insurers) certifies controls and agent behavior, but nobody certifies that billed outcomes are real, that a model change is safe, or that money moved within authority [S31][V].
- AI agents issue refunds and credits that finance cannot trace to a policy; vendor liability caps often limit recourse to a refund of fees [S35][V].
- New chatbot laws turn disclosure and timely human access into measurable obligations with deadlines inside two months, and most support teams cannot show compliance statistically [S37][V].
- Developer tools (open source and commercial) already replay production traffic, shadow and gate model changes, so replay mechanics are commoditizing; what they do not ship is a certified, signed promotion verdict [S39][V].
- Evaluation sets built from production transcripts are a privacy boundary: redaction is imperfect and sending replay data to a candidate provider exports customer data [S40][V].
- Suites and labs now ship ROI, cost and evaluation views (Appendix A), so the durable advantage is statistical rigor, safe actuation, independence and customer-verifiable evidence, not dashboards or process maps.

## 1.3 Functional requirements

| ID | Requirement | Phase |
|---|---|---|
| FR1 | Ingest events read-only from systems of record, agent platforms, model gateways, vendor billing exports and billing data | 0 |
| FR2 | Reconstruct the workflow graph and rank value leaks in currency | 0 |
| FR3 | Compute cost per accepted outcome and net value per workflow and step, including human, run, tool, review and infrastructure cost | 0 |
| FR4 | Define outcomes and collect labels, including delayed, sampled, surrogate and third-party QA labels | 1 |
| FR5 | Estimate calibrated risk (probability and severity of error) per step, case class and executor option | 1 |
| FR6 | Evaluate candidate policies offline in shadow mode and state the evidence grade of every estimate | 1 |
| FR7 | Actuate policy changes through a gated, risk-bounded, propensity-logged loop with instant fallback to the baseline | 2 |
| FR8 | Produce causal value statements (realized vs projected) with confidence intervals and evidence grades | 1 to 2 |
| FR9 | Preserve tamper-evident evidence and allow any statement to be reproduced by the customer | 0 to 2 |
| FR10 | Generate logging and human-oversight evidence packs aligned with EU AI Act Articles 12, 14 and 26 | 2 |
| FR11 | Model human review capacity and congestion and schedule experiments accordingly | 2 |
| FR12 | Detect regime shifts (model, provider, rule or data changes) and respond automatically | 1 to 2 |
| FR13 | Provide role-based views for IT, finance, workflow owners and auditors | 0 to 2 |
| FR14 | Maintain a model-exposure inventory and retirement calendar from logged model identity and provider deprecation feeds | 0 |
| FR15 | Qualify a candidate model with a certified, anytime-valid paired audit: a zero-label tier for benign updates and a label-efficient tier that labels only material disagreements | 0 to 1 |
| FR16 | Publish Evidence Statements as signed statements registrable in a transparency service, using an open, versioned schema | 1 |
| FR17 | Retrieve precedent decision traces filtered by evidence grade and provenance (Proposed, ADR-012) | 2 |
| FR18 | Audit outcome-based vendor billing: estimate the true accepted-outcome rate with intervals and compare it with billed outcomes | 1 |
| FR19 | Run continuous, randomized, propensity-logged vendor and model bake-offs on identical traffic under the risk gate | 2 |
| FR20 | Ingest third-party QA and judge scores as labels or surrogates without producing individual-worker scores | 1 |
| FR21 | Audit consequential AI actions (refunds, credits, discounts, account changes, data access) against policy authority; estimate the outside-authority rate and currency amount with intervals; calibrate guardrail ceilings | 1 |
| FR22 | Compare measured outcomes, service levels, deprecation notices and definitions with contract terms (Proposed) | 2 |
| FR23 | Provide a Review Workbench through which customer experts label sampled cases under pre-label routing, with blinded comparisons | 1 |
| FR24 | Provide a public verifier, schema, test vectors and a partner interface so auditors, certifiers and insurers can verify statements offline and map them to control frameworks | 1 |
| FR25 | Audit human-access and disclosure compliance: disclosure presence and accuracy, availability of a human-request feature, time to a human, escalation success and trapped-loop rate, with intervals and signed evidence | 1 |
| FR26 | Import traces and datasets from developer tools and expose a CI/CD promotion gate that returns a signed verdict | 0 to 1 |
| FR27 | Gate every replay or shadow set through a Replay Privacy Gate: local-first scoring, redaction and rephrasing, measured residual leakage, provider data-use checks | 0 to 1 |

## 1.4 Quality goals

| Priority | Goal | Meaning |
|---|---|---|
| 1 | Causal credibility and reproducibility | Every reported number can be re-derived by the customer from signed inputs and a pinned, versioned estimator, with valid uncertainty |
| 2 | Bounded risk | Actuation never exceeds the declared risk tolerance; the default is the baseline process |
| 3 | Time to first value | Read-only insight within one week of access; shadow estimates within 30 days; first migration verdict on a typical workflow within 10 business days of a notice |
| 4 | Change tolerance | Models, providers, agent platforms and telemetry standards can change without touching decision logic |
| 5 | Sovereignty and privacy by design | Customer data stays in the customer tenant; no individual-level worker scoring |

Secondary goals: evidence longevity (10 years or more, post-quantum safe), interoperability through open standards (MCP, A2A, SCITT, COSE), operability by a small team, and low cost of running OMC itself.

## 1.5 Stakeholders

| Stakeholder | Concern |
|---|---|
| IT manager or CIO office (champion) | Justify spend; roll out without disrupting production; survive model retirements |
| CFO and finance controller (co-owner of the number) | Numbers they can audit and re-run; vendor invoices that match reality |
| Support and operations leaders (COO, workflow owners) | Throughput, quality, unit cost, vendor choice |
| Frontline reviewers and agents | Sustainable review load; not scored as individuals |
| Compliance, DPO, legal, works council | EU AI Act Articles 12, 14, 26 and 50, chatbot disclosure and human-access laws, worker information, GDPR, replay-set privacy |
| CISO and security | Tenant isolation, least privilege, read-only default, decision-API attack surface |
| Internal and external auditors | Replay, evidence integrity, retention |
| Assurance partners (CPA firms, certification bodies, insurers) | Evidence they can verify offline and map to AIUC-1, ISO/IEC 42001, SOC 2 and underwriting frameworks |
| Platform and AI-vendor owners (helpdesk, CRM, agent vendors) | Stable integration contracts; fair measurement |
| Intellica engineering and operations | Buildable and operable by a small team |

## 1.6 Assumptions

| ID | Assumption |
|---|---|
| A1 | **Beachhead (decided, ADR-017):** customer-support ticket resolution across chat and email, AI-handled and AI-assisted, with IT service desk second. Accounts-payable exceptions and regulated workflows come later. The architecture stays workflow-agnostic. |
| A2 | Target workflows carry at least 100,000 cases per year, enough volume for causal power. |
| A3 | Phases 0 and 1 have no write access to systems of record. |
| A4 | Planning scale per tenant: up to 5 million decision records per day; in-line decision latency p99 of 250 ms or less. |
| A5 | Buyers accept a customer-tenant data plane with a hosted control plane. |
| A6 | The team is small, so delivery is staged and the data plane starts as a modular monolith. |
| A7 | Initial exploration defaults (reference lane of 5 to 10 percent of cases, minimum action-probability floor) are starting values to be tuned per workflow. |
| A8 | Reference lane and risk budgets are set with the customer's risk owner, not by OMC. |
| A9 | Target customers run at least one AI-handled support workflow, ideally on an outcome-priced vendor or a model that has a published retirement date. |
| A10 | Customers can provide read access to the helpdesk and the vendor's billing and resolution exports. |
| A11 | Model-update audits rely on shadow-scoring traffic with both models, which the customer or the vendor integration must permit. |
| A12 | Customer experts supply gold labels through the Review Workbench, and partner QA tools supply surrogates; OMC employs no labeling staff. |
| A13 | Policy authority rules (refund ceilings, eligibility windows, credit and discount limits, data-access scope) exist as documents or system configuration that owners can confirm. |
| A14 | Target customers serve users in California, Spain or the EU and therefore face chatbot disclosure and human-access obligations; counsel, not OMC, interprets the statutes. |
| A15 | Customers document processing of production transcripts for evaluation as a stated purpose and permit local or in-tenant scoring first. |
