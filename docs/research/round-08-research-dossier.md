# Round 8 research dossier: academic map, competitive scan, three-year protection

Date: 23 October 2026. Status: findings for founder review. Claims marked [V] rest on vendor or secondary sources.

## 1. Executive findings

1. **Dashboards are now table stakes.** ServiceNow, Salesforce, Microsoft with Celonis, UiPath, Make and OpenAI Frontier all ship or announce ROI, cost or evaluation views. A single ROI number is no longer a differentiator.
2. **The category vocabulary is converging on our language.** Buyer guidance now says ROI means accepted completed work, a credible baseline, full operating cost and stated attribution limits. That is the opening for evidence grades and customer-rerunnable proof.
3. **The context-graph land grab is crowded and funded.** Celonis Context Model, Skan, Glean, Interloom and Trace all target decision traces. Competing on process maps is a losing frame. Making decision traces *causal* (propensity-logged, evidence-graded) is not yet claimed by anyone I found.
4. **There is a forced-deadline pain we can serve first.** Model deprecations and silent updates create a "re-qualification tax". Providers give roughly 60 days notice, many enterprises delay migrations because switching looks too costly, and a large share expect migrations to take four months or more. OMC's shadow replay, canary lane, risk gate and evidence vault are exactly the machinery a migration needs.
5. **The academic frontier just moved toward our design.** An October 2026 paper treats deferral to congested human experts as a queue-control problem with regret bounds. Conformal methods now offer risk and budget guarantees for model cascades. Prediction-powered methods reach causal estimands. The pieces exist; the integrated, audited system does not (absence caveat applies).
6. **Standards are consolidating.** MCP and A2A now sit under the Linux Foundation's Agentic AI Foundation, and A2A reached v1.0 in March 2026. OpenTelemetry GenAI conventions remain unstable. OMC should treat MCP and A2A as first-class surfaces and keep an anti-corruption layer for telemetry.
7. **Independence is a structural moat.** Every suite and every lab sells agents or models. A vendor cannot credibly audit its own value claims. Positioning OMC as the independent measurement authority that plugs into all of them is the one position none of them can occupy.

## 2. Academic domain map

Freshness: **N** = new research this round, **P** = prior rounds, **Q** = in the research queue only.

| # | Domain | Frontier signals (2026) | OMC component | Fresh |
|---|---|---|---|---|
| 1 | Causal inference and off-policy evaluation | Causal methods for LLM development and evaluation (arXiv 2605.25998); doubly robust and sequential estimators | Causal Ledger | P |
| 2 | Prediction-powered inference | Causal variants (2502.06343), LLM-judge calibration (2601.05420), active sampling (2604.18569), multi-task (2605.29249), power analysis (2603.16041) | Label Service, Ledger | N |
| 3 | Conformal risk control and safe policy control | Conformal policy control (2603.02196); calibrate-then-delegate with risk and budget guarantees (2604.14251); conformal arbitrage (2506.00911) | Risk Gate | N |
| 4 | Learning to defer and human-AI complementarity | To Defer or Not to Defer? congested experts (2610.15128); cost-sensitive deferral with workload constraints; doubly robust deferral policy learning (2302.02944); amplified oversight (2510.26518) | Capacity Model, Optimizer | N |
| 5 | Experiments under interference | Stochastic congestion estimators (ACM 2024, 2302.12093); Little's-law mixed differences-in-Q (2605.29641); clustered and random-duration switchbacks | Ledger, Scheduler | N |
| 6 | Constrained online learning, routing, cascades | AgentRouter (2609.22951); UCCI (2605.18796); CascadeDebate (2604.12262); Bayesian self-escalation (2608.24087) | Optimizer | P |
| 7 | Process mining, agentic and object-centric | Agentic process mining agenda (2609.07984); OCEL 2.0 | Work Twin | P |
| 8 | Decision traces and context graphs | Foundation Capital thesis; Forrester caution that traces need provenance, versioning and access control | Precedent Store (proposed) | N |
| 9 | LLM-as-judge and evaluation science | Noisy-judge inference (2601.05420); simplex perspective for no-gold settings (2505.21972) | Label Service | N |
| 10 | Calibrated simulation and digital twins | SYN-DIGITS synthetic-control calibration (2604.07513); LLM-augmented twins (2603.11333, 2601.06111) | Simulation Twin (Phase 3) | N |
| 11 | Queueing theory and operations research | Little's law estimators; staffing and capacity | Capacity Model | P |
| 12 | Applied cryptography and trust | NIST FIPS 203, 204, 205; transparency logs; attestation | Evidence Vault | P |
| 13 | Privacy-enhancing technologies | Differential privacy, secure aggregation, federated analytics | Cross-tenant priors (Phase 3) | Q |
| 14 | Regulation and governance | EU AI Act Articles 12, 14, 26; Digital Omnibus dates; ISO/IEC 42001; NIST AI RMF | Evidence packs | P |
| 15 | Organizational and labor economics of AI | Task-based models; principal-agent delegation | Value model, change management | Q |
| 16 | Software lifecycle for models | Deprecation calendars, canary, shadow, rollback | Migration Gate | N |
| 17 | Agent security | Human-centric security backbone in production systems (2605.24309) | Decision API threat model | P |
| 18 | Human factors | Oversight fatigue, automation bias | Structural oversight design | Q |
| 19 | Incentives and mechanism design | Goodhart, outcome-linked pricing conflicts | ADR-009, ADR-010 | P |

## 3. Competitive scan (dated)

| Player | Latest public move | Why it matters |
|---|---|---|
| ServiceNow AI Control Tower | Knowledge 2026 (May): discover, observe, govern, secure, measure; Traceloop acquired; cost tracking and ROI dashboards; GA expected August 2026. April 2026 tiering bundles process mining and the control tower | Measure and ROI views are bundled into the platform |
| Salesforce Trusted Enterprise AI Harness | Announced 10 September 2026: AI Control Plane with discovery, identity, policy, lifecycle, evaluation and cost control across Salesforce and third-party systems; coverage places rollout in fiscal 2028 starting February 2027 [V] | Window before bundling lands is roughly 12 to 18 months |
| Microsoft Agent 365 with Celonis | Private preview 1 May 2026: agent business impact and ROI, identify which agent paths perform better | Distribution through the largest enterprise channel |
| Celonis | Context Model (May 2026) with decision intelligence (anticipate and simulate change), Transformation Hub with audit-ready ROI and value attribution, MCP server, AgentC | Closest convergence. Rigor of attribution unverified |
| UiPath Maestro Flow | August 2026 orchestration surface for agents, automations and people | Orchestration plus observability |
| Make Process Intelligence | Launched 20 October 2026; claims to prove whether a change worked | Claim is becoming table stakes |
| OpenAI Frontier | Launched 5 February 2026: shared business context, agent identity, evaluation and optimization tooling, usage analytics; supports third-party agents including those built on other labs' models | Labs are building context and evaluation layers |
| Context-graph startups | Interloom $16.5M (March 2026), Trace $3M seed (February 2026), Skan, Glean positioning | Funded land grab on decision traces |

**Reading the scan.**
- Suites are ecosystem-anchored. Buyer guides rate Salesforce and ServiceNow low on independence. Labs claim multi-vendor reach but sell their own agents.
- I found no public product combining pre-registered measurement plans, customer-rerunnable estimators, evidence grades and risk-bounded actuation. Absence caveat: I have not tested competitors hands-on.
- Price anchors in the category run roughly $60K to $350K per year for production platforms [V].

## 4. Value opportunities for the customer base

Scored on deadline pressure, reuse of components already in the architecture, and strength of evidence.

| Rank | Opportunity | Evidence | Reuse | Verdict |
|---|---|---|---|---|
| 1 | **Safe model migration and qualification** | Providers publish roughly 60-day notices; a survey of 520 technical leaders found over 80% delayed, scaled back or restructured a migration over switching cost, and 57% expect four months or more; 81% of CIOs run three or more model families [V] | Very high: shadow replay, canary lane, risk gate, vault | **Entry wedge** |
| 2 | Compliance evidence packs (Articles 12, 14, 26) | Annex III obligations from 2 December 2027; deployers must keep logs and assign oversight | High: vault and oversight design | Paid module, ready by mid-2027 |
| 3 | Cost per accepted outcome and AI-spend leak finder | Overruns common; token cost can be a minority of per-case cost [V] | High | Part of Phase 0 report |
| 4 | Override mining into playbooks and decision traces | Overrides are free labels; context-graph demand | Medium | Phase 2, aggregate only |
| 5 | Review-capacity and staffing forecasts | Congested-expert theory; queue models already in the Capacity Model | High | Ops-leader upsell |
| 6 | Contract leverage: measured switching cost for vendor negotiation | Buyers now ask for 12-month deprecation notice and stability terms [V] | Medium | Report by-product |
| 7 | Underwriting evidence feed | Insurers certify agents, capacity is small | Medium | Phase 3 option |

### 4.1 The migration wedge in detail

1. **Exposure inventory.** Model identity logs show which workflows depend on which model versions, volume, spend and retirement dates.
2. **Qualification set.** Stratified historical cases by case class, plus hard cases and recent drift.
3. **Offline replay** of the candidate model on that set; gold labels where they exist, judge scores corrected by prediction-powered inference elsewhere.
4. **Shadow run** on a live copy of traffic with no action.
5. **Statistical decision.** Non-inferiority or equivalence testing (two one-sided tests) on business metrics: accepted-outcome rate, error rate, cycle time, cost per accepted outcome. The margin is set by the workflow owner. Sequential designs allow early stopping. Intervals, not point estimates.
6. **Canary lane** behind the risk gate with automatic rollback until the retirement date.
7. **Promotion** and a signed evidence pack: parity statement, cost delta, residual risk, rollback record.
8. **Calendar.** Retirement tracking and alerts, so the next migration starts at the notice, not at the shutdown reminder.

Why it is the right wedge: hard deadline, existing engineering and QA budget, short sales cycle, no actuation authority needed at first, and every artifact it produces (baseline, replay set, propensity-logged canary) is the seed of the full controller. Risks: eval-tool vendors adding parity reports, labs shipping their own migration tooling, customers lacking outcome-labeled history (these cases grade E1).

## 5. Innovations to break new ground

Each is a **hypothesis from this analysis**, not a published result. Each has a validation test.

| ID | Innovation | Hypothesis | Test |
|---|---|---|---|
| I1 | Evidence-weighted decision traces | Precedent retrieval filtered by evidence grade and provenance beats unfiltered precedent | Synthetic or partner workflow, outcome comparison |
| I2 | Simulation-assisted inference | A calibrated twin used as the prediction in prediction-powered inference gives valid intervals with shorter real experiments | Synthetic worlds with planted truth |
| I3 | Congestion-aware deferral under a conformal gate | Joint deferral and queue control beats threshold deferral at equal risk | Simulated review queue |
| I4 | Open Evidence Statement format | An open, signed schema for causal value claims becomes the format auditors and insurers accept | Draft spec; test with a finance advisor |
| I5 | Regime-aware calibration | Adaptive conformal recalibration at model-identity changes preserves coverage after swaps | Planted model flips |
| I6 | Causal parity tests for model swaps | Equivalence testing on business metrics with reduced labels gives faster, safer qualification than benchmark scores | Replay on partner data |
| I7 | Privacy-preserving cross-tenant priors | Differentially private aggregates speed calibration for new tenants | Legal review first, then simulation |
| I8 | Independence charter | A written no-conflict policy (no agents or models sold, no outcome grading by interested parties) is itself a buying criterion | Customer interviews |

## 6. Three-year threat model and protection (2026 to 2029)

| Threat | Timing | OMC response |
|---|---|---|
| Suites bundle ROI and optimization (Salesforce Harness, ServiceNow Measure) | 2027 | Be the measurement authority inside them: certified connectors and marketplace listings; independence and evidence grades as the differentiator |
| Labs own business context and evaluation, and sell outcome-priced agents | 2027 to 2028 | Lab-agnostic evidence layer; auditor-style independence |
| A process-intelligence leader adds rigorous causal methods | 2027 to 2028 | Ship first with the open Evidence Statement; ingest rather than rebuild mining; stay ahead on safe actuation |
| Judging and simulation commoditize evaluation | 2027 onward | Judges and simulators are inputs to inference; the asset is calibration and causal design |
| Agents become reliable enough to remove humans from target workflows | 2028 onward | Option abstraction; the risk gate and economics remain; shift to process redesign decisions |
| Regulation loosens or tightens | Continuous | Finance and board reporting value remains; evidence packs are a module |
| Standards settle (MCP, A2A, OpenTelemetry) | Continuous | First-class MCP and A2A surfaces; adapters for telemetry |
| Quantum threat to signatures | 2029 to 2035 | Hybrid post-quantum signing and re-anchoring from day one |
| Model price collapse | Continuous | Value sits in risk and process terms, not token cost |
| Open-source clones of the ledger | 2028 onward | Standard, per-tenant data asset, integration depth, evidence independence |

**Moat stack:** independence, open evidence format, propensity-logged history, per-workflow calibration, certified suite connectors, compliance packs, customer-owned evidence (low switching fear).

## 7. Profitability levers

- **Fast first sale:** fixed-price migration qualification, then subscription, then outcome-linked fees after two re-run statements (ADR-010).
- **Land and expand:** migration qualification, shadow evaluation, gated actuation, compliance module.
- **Cost structure:** estimators and ledgers are compute-light compared with model serving. The main cost is integration, so productize the pilot kit and use partner channels.
- **Avoid consulting drift:** fixed scopes, connector library, refuse bespoke work not on the roadmap.
- **Compounding asset:** propensity-logged decision history lowers marginal onboarding cost.
- **Unknowns to model:** sales-cycle length, integration hours per tenant, evidence-pack attach rate, gross margin at 10 and 50 tenants.

## 8. Effect on arc42

See `docs/arc42/amendments/v0.2-proposed-amendments.md`.

## 9. Evidence register

| Tag | Source | Flag |
|---|---|---|
| S17 | ServiceNow Knowledge 2026 press release (newsroom.servicenow.com); MarkTechPost 19 May 2026 | Vendor [V] |
| S18 | Lyzr, onereach.ai platform roundups (Salesforce Harness, UiPath Maestro Flow) | Secondary [V] |
| S19 | Kai Waehner Process Intelligence Landscape 2026; Celonis:NEXT 2026 announcement | Analyst blog and vendor [V] |
| S20 | OpenAI Frontier coverage: Futurum, nxcode.io | Secondary [V] |
| S21 | Interloom (Fortune, 23 March 2026); Trace (TechCrunch, 26 February 2026); Foundation Capital; Forrester | Press and analyst |
| S22 | Model deprecation: ud.hk (31 July 2026), Stack Overflow blog on a 520-leader survey (21 October 2026), dev.to migration-gate article, Kai Waehner trusted agentic AI landscape Q3 2026 | Mixed; survey is vendor-run [V] |
| S23 | To Defer or Not to Defer? (arXiv 2610.15128); Gao et al. (arXiv 2302.02944); calibrate-then-delegate (arXiv 2604.14251) | Preprints |
| S24 | SYN-DIGITS (arXiv 2604.07513); LLM-augmented digital twin (arXiv 2603.11333) | Preprints |
| S25 | AAIF, MCP and A2A status: flowhunt.io, devopsdigest.com (A2A v1.0 March 2026; joined AAIF mid-August 2026, sources differ on the exact date) | Secondary [V] |
| S26 | Platform price anchors: agentic-ai.readthedocs.io | Secondary [V] |

Earlier-round sources S1 to S16 remain in arc42 Appendix C.

## 10. Decisions needed from the founder

- **D1.** Make Safe Model Migration and Qualification the Phase 0 entry wedge (alongside the read-only leak report). Recommended: yes.
- **D2.** Publish the Evidence Statement as an open specification. Recommended: yes, after one design-partner review.
- **D3.** Position OMC as the independent measurement authority that integrates with every suite (partner, do not compete). Recommended: yes.
- **D4.** Choose the beachhead workflow (still open from arc42 assumption A1).
