# Appendix A. Competitive position and differentiation

## A.1 Landscape (as publicly described; methodology unverified [V])

| Player or class | What is publicly claimed | Implication for OMC |
|---|---|---|
| ServiceNow AI Control Tower | Discover, observe, govern, secure and measure AI across systems; cost tracking and ROI views; process mining bundled in platform tiers [S17] | Measure views are bundled; compete on evidence grade and independence |
| Salesforce AI control plane | Announced 10 September 2026: discovery, identity, policy, lifecycle, evaluation and cost control; rollout reported from February 2027 [S18][V]. Intercom's Fin is reported to be part of Salesforce [V] | Window before bundling; vendor consolidation raises the value of independent outcome audits |
| Microsoft Agent 365 with Celonis | Preview since 1 May 2026: agent business impact and ROI [S14] | Largest distribution channel |
| Celonis | Context Model with decision intelligence, Transformation Hub with audit-ready ROI and value attribution, MCP server [S14] | Closest convergence; do not compete on maps |
| Make Process Intelligence | Launched 20 October 2026; claims to prove whether a change worked [S14] | Claim becoming table stakes |
| UiPath Maestro Flow | August 2026 orchestration [S18] | Orchestration plus observability |
| OpenAI Frontier | February 2026: shared business context, agent identity, evaluation and optimization tooling [S20] | Labs build context and evaluation layers |
| Outcome-priced support vendors (Fin, Sierra, Decagon, Zendesk, Agentforce, others) | Per-resolution or outcome pricing; vendor-defined outcomes; published rates for some (for example about $0.99 per resolution) [S27][V] | Their incentive is to count more resolutions; independent audit and bake-off are structurally unavailable to them |
| AI QA tools | Score 100 percent of interactions against rubrics; calibrate to human reviewers; agreement metrics [S30][V] | Partner: ingest scores as labels; add valid intervals; avoid per-worker scoring |
| Context-graph startups | Interloom, Trace, Skan, Glean positioning [S21] | Crowded; differentiate with causal, graded traces |
| Evaluation and observability tools | Fixed test suites, benchmarks, regression suites [S22] | Certified, label-efficient audits are a step beyond |
| Process-mining research | Agenda notes the gap between mined evidence and permitted action [S13] | Open space for governed action |
| Assurance ecosystem (AICPA with AIUC, KPMG, ISO/IEC 42001 certifiers, CSA STAR for AI) | Joint SOC 2 plus AIUC-1 certification announced 19 October 2026; KPMG first Big Four firm with AIUC-1 certification (27 August 2026); AIUC-1 includes live testing of agent behavior; several support vendors, reportedly including Fin, certified [S31][V] | They certify controls and agent behavior; they do not measure outcome truth, change safety or action authority. Partner, map to their controls, supply the evidence |
| AI liability insurers (for example Munich Re aiSure) | Underwriting converges on NIST AI RMF, ISO/IEC 42001 and AIUC-1; third-party validation shortens underwriting [S33][V] | Evidence feed in Phase 3; statements must map to those frameworks |
| Action monitors (for example Isara) | Detect unauthorized refunds and credits in conversations [S35][V] | Niche competitors; differentiate with statistical leakage estimates, cross-vendor view and signed evidence |
| Developer tools for replay and gating (Langfuse, LangSmith, Braintrust, Datadog, Kitaru, llmshift, gatelane) | Backtesting on production traces, shadow reports, upgrade pull requests and CI gates, many free or open source; none reported to sign promotion verdicts or give anytime-valid certified results [S39][V] | Do not compete on runners; import and interoperate; differentiate on certified verdicts, business parity and independence |
| Chatbot-law compliance advisers and transcript auditors | Manual or tool-assisted audits of disclosure and escalation against state and EU rules [S37][V] | Statistical, continuous, signed evidence; partner with counsel |
| Marketplaces and co-sell programs (Salesforce AgentExchange, ServiceNow Store, Microsoft marketplace) | Unified marketplaces, new partner programs, co-sell tied to committed cloud spend [S41][V] | Distribution channels and bundling risk at once |
| Compliance automation (Vanta, Drata) | Subscription priced by size, frameworks and modules, audits engaged separately; Vanta ARR estimated near $300M in April 2026; direct switching rare [S34][V] | Business-model analogue; OMC's advantage is daily operational use |

## A.2 Where OMC aims to lead

1. **Independence.** Not selling agents or models, no contingent fees, definitions shown side by side (ADR-016).
2. **Certified, label-efficient audits.** Zero-label certificates for benign updates, labels only on material disagreements, anytime-valid verdicts, error budget across a lifetime of updates [S29].
3. **Evidence-graded value.** Every number labeled E0 to E3 with intervals.
4. **Risk-bounded actuation.** Conformal safe-policy control anchored on the baseline [S8].
5. **Customer-rerunnable, third-party-verifiable proof.** Pre-registered plans, pinned estimators, signed statements registered in a transparency service [S28].
6. **Outcome audit and bake-off.** Independent truth about vendor-claimed outcomes and vendor performance.
7. **Label-efficient causality** through prediction-powered inference [S9].
8. **Congestion-aware oversight.** Human review as a modeled, constrained resource [S10].
9. **Privacy by construction.** Workflow-level units only (ADR-007).
10. **Regime awareness.** Model identity is data; unplanned shifts trigger certified audits.
11. **Compounding asset.** Propensity-logged decision history per tenant; opt-in aggregate priors later.
12. **Assurance-ecosystem fit.** Control mappings and a partner interface make OMC the evidence substrate for certifiers, CPA firms and insurers (ADR-022).
13. **Action authority audit.** Currency-denominated leakage estimates with intervals, independent of the vendor (ADR-023).
14. **Public verifier.** Open-source verification and test vectors make claims checkable by anyone (ADR-025).
15. **Compliance measurement with deadlines.** Human-access and disclosure evidence for rules that apply within weeks (ADR-027).
16. **Interoperability.** Imports from developer tools and a CI gate make OMC a verdict layer on top of what teams already use (ADR-028).
17. **Privacy-gated replay.** Measured leakage bounds before any provider call (ADR-029).

## A.3 Honest limits

The assurance incumbents are well-funded and moving fast (a Series A and a Big Four certification within weeks of each other in 2026 [V]). OMC's position depends on staying complementary and on the evidence being better than what they can assemble from live testing alone. The rigor gap versus competitors is inferred from public descriptions and has not been tested hands-on. The lead is on rigor, independence and evidence, not features, and the window narrows as incumbents add ROI and decision modules. The certified-audit theory covers prediction-determined losses; generative agents depend on the action-level reduction and on a material-difference classifier that must be validated (ADR-021). The core audit paper is a single-author preprint validated on classification tasks and small language models; a replication on support-workflow data is Phase 0 spike S-a.
