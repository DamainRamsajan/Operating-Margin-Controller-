# Appendix E. Business model and packaging (hypotheses)

Nothing here is a price or a forecast. Anchors are from secondary sources [V] and are to be replaced by design-partner evidence.

## E.1 Analogue and lessons

| Observation | Source | Lesson for OMC |
|---|---|---|
| Compliance-automation leaders sell annual subscriptions priced by company size, number of frameworks and add-on modules; the audit itself is bought separately from partner auditors | [S34][V] | Platform subscription plus partner-delivered attestations; OMC never sells the certificate |
| Vanta's ARR is estimated near $300M (April 2026), growing about 69 percent a year; direct switching between leaders is rare | [S34][V] | Embedded evidence workflows create durable revenue |
| Low-frequency usage (twice-yearly audits) is cited as a churn risk, so leaders add continuous monitoring | [S34][V] | OMC's migration, billing and action audits are operational, so usage frequency is higher by design |
| An alleged case of near-identical certificates produced by an automated vendor in 2026 hurt trust in cheap, fast attestations | [S34][V] | Quality and reproducibility are the premium; publish methods and test vectors |

## E.2 Packaging

| Tier | Contents | Pricing shape | Trigger |
|---|---|---|---|
| Qualify | Exposure inventory, retirement calendar, certified qualification per migration | Fixed fee per qualification or annual retainer with a number of qualifications | A retirement notice |
| Audit | Outcome billing audit, action authority audit, contract evidence pack | Fixed fee per audit cycle, then subscription per workflow and vendor | An invoice dispute or a leakage concern |
| Control | Bake-off, gated actuation, capacity model | Subscription by workflow volume band | Evidence that a better configuration exists |
| Comply | Article 12 and 14 packs, control mappings, partner interface | Module on top of any tier | Annex III dates, a customer security review, an insurer request |

Reference anchors [V]: small-company compliance subscriptions start near $7,500 to $10,000 a year (not our segment); production agent platforms price roughly $60K to $350K a year; partner audits cost roughly $10K to $40K or more, billed separately. Entry products should price below platform anchors to shorten the sales cycle.

## E.3 Cost of goods and margin levers

| Cost item | Driver | Control |
|---|---|---|
| Shadow-scoring inference | Traffic share times the candidate model's price | Sampling, anytime-valid early stopping, capped customer-billed pass-through |
| Gold labels | Sample size | Customer experts, disagreement-only labeling, prediction-powered correction (ADR-024) |
| Estimator compute | Estimator mix and data size | Pinned images, batch scheduling |
| Integration engineering | Connectors per tenant | Pilot kit, connector library, suite marketplaces |
| Control-plane hosting | Tenants and feeds | Multi-tenant control plane, metadata only |
| Customer success | Workflows per tenant | Documentation, verifier, templates, partner delivery |

## E.4 Expansion path

Qualify, then Audit, then Control, then Comply, each triggered by a concrete event (a retirement notice, an invoice dispute, a leakage finding, a compliance date). Each step reuses the same ingestion, label service, ledger and vault.

## E.5 Metrics to track

Time to first verdict; labels per verdict; verified savings per tenant; attach rate by tier; gross margin per tenant; partner-sourced pipeline; net revenue retention; share of statements verified by third parties; number of independent replications of the methods.

## E.6 What we will not do

Contingent fees; selling certificates; referral fees that depend on findings; employing labeling staff; bespoke work off the roadmap.

## E.7 Channel economics (hypotheses) [S41][V]

| Channel | Mechanism | Why it matters | Caveat |
|---|---|---|---|
| Salesforce AgentExchange | Unified marketplace announced April 2026; revenue share by percentage of net revenue with a marginal model; a $50M builders initiative | Many support teams run Service Cloud | The same company is building a competing control plane and reportedly owns a leading support vendor |
| ServiceNow Store | AI agents category and a new Build Partner Program (January 2026) | Strong in IT service desk, our second workflow family | Bundled measure views |
| Microsoft commercial marketplace | Transactable offers, co-sell tied to committed cloud spend; historically a low transaction fee | Purchases can draw down existing cloud commitments, shortening procurement | Fee levels and terms change; confirm before modeling |
| Helpdesk marketplaces (Zendesk, Intercom) | Not researched | Closest to the data | Unknown |

Principles: list where the buyer's helpdesk or cloud commitment is; sell entry products directly; never let a co-sell incentive influence findings (ADR-016, ADR-030).

## E.8 Valuation reality check [S42][V]

Vanta was valued at $4.15B in July 2025 when its ARR was estimated near $220M, roughly 19 times ARR on those estimates, and its ARR was estimated near $300M by April 2026. Category leaders therefore earn high-teens ARR multiples at best, so a $7B outcome implies several hundred million dollars of ARR at comparable multiples, or a strategic premium. Pre-revenue deals of that size in 2026 involved frontier-lab teams (Round 1 research). The honest reading is that OMC is a revenue business with strategic upside: standard position, data asset, distribution and an evidence layer others need. Independence is a moat and also limits the buyer set, because an acquirer from the assessed set would erode it. Treat $7B as a guideline for ambition and track milestones instead: ARR, partner-delivered attestations, third-party verification share, marketplace distribution and standard adoption.
