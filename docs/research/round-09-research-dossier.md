# Round 9 research dossier: beachhead, new customer value, certified audits, standards

Date: 23 October 2026. Builds on Round 8. Claims marked [V] rest on vendor or secondary sources. Items marked **hypothesis** are analysis, not published results.

## 1. Findings

1. **Beachhead: customer-support ticket resolution** (ADR-017). Per-resolution pricing is mainstream and published rates are public for several vendors; reopen, recontact and CSAT give fast outcome labels; model churn is high; Annex III exposure stays low if OMC never scores individual workers.
2. **A new, strong value-add: outcome billing audit.** Vendors define the billed outcome. One leading vendor counts an assumed resolution when a customer leaves or stays silent for 24 hours, and critics dispute that billing. Vendor-claimed resolution rates (reported 66 to 76 percent fleet-wide) sit well above results from independent tests and case studies (reported 38 to 53 percent) [V]. Review sites advise buyers to "model the definition carefully" because the definition moves the money. Only an independent party can audit this; the vendor cannot.
3. **Vendors are consolidating.** Two sources report that Intercom's Fin is now part of Salesforce after a transaction completed on 10 September 2026 [V]. When the leading outcome-priced vendor is owned by a suite, independent measurement matters more.
4. **The statistical core for the migration wedge now exists in the literature.** A 2026 preprint shows that the risk difference between an incumbent and a candidate model lives on the inputs where they disagree, which is observable without labels. It certifies benign updates with zero labels, labels only sampled disagreements through an anytime-valid sequence, stays valid under any label-routing rule (even an adversarial judge), and composes across a lifetime of updates. Reported results: 56 percent of benign updates certify with zero labels, and the audited band needed a median of 327 labels against 2,906 for uniform labeling [S29]. **Limits:** single author; validated on classification and small language-model fine-tunes; open-ended judged text is explicitly outside the theory.
5. **Standards give us a better evidence format than inventing one.** RFC 9943 defines the SCITT architecture (signed statements registered with a transparency service, with receipts), and an individual draft already profiles AI-agent action receipts as COSE_Sign1 statements over a canonical payload [S28]. OMC's Evidence Statement should be a SCITT profile (ADR-018).
6. **QA tooling is crowded but statistically thin.** Vendors sell scoring of 100 percent of interactions against rubrics, versus typical manual coverage of 1 to 5 percent, and track human agreement [S30][V]. They do not provide valid intervals for aggregate quality, and per-agent scoring raises employment issues. OMC should ingest their scores as labels and add intervals.
7. **The statistical machinery for gating changes is converging.** Related 2026 work covers anytime-valid acceptance tests for self-evolving agents, adaptive auditing with anytime-valid guarantees, and attribution of drift between the system and the judge [S29]. This validates the approach and also shortens the lead time for others.

## 2. Beachhead evaluation

Confidence: support is scored from this round's evidence; the others rest on earlier rounds and general knowledge.

| Workflow | Volume | Label speed | Vendor and model churn, outcome pricing | Regulatory exposure | Data access | Sales cycle | Verdict |
|---|---|---|---|---|---|---|---|
| Support tickets (chat, email) | High | Fast (reopen, recontact, CSAT) | Very high | Low to medium | Mature helpdesk APIs | Short to medium | **Chosen** |
| IT service desk | High | Fast | High | Low | Mature | Medium | Second |
| Payables exceptions | Medium to high | Slow (audit, recovery) | Medium | Low to medium | ERP-dependent | Medium to long | Later |
| Claims triage | Medium | Slow | Medium | High | Hard | Long | Later |
| KYC alert triage | Medium | Slow | Medium | High | Hard | Long | Later |

## 3. Value opportunities, ranked

| Rank | Opportunity | Evidence | Reuse of existing blocks | Notes |
|---|---|---|---|---|
| 1 | Certified model qualification | Retirement calendars; survey evidence of delayed migrations [V]; certified-audit literature | Very high | Entry product; fixed fee |
| 2 | Outcome billing audit | Vendor-defined outcomes, assumed resolutions, rate gaps [V] | High | Entry product; fixed fee; never contingent |
| 3 | Continuous vendor bake-off | Buyers compare vendors by proof of concept; one controlled comparison reported 73 versus 49 percent resolution between two vendors [V] | High | Needs two or more options or a build-versus-buy alternative |
| 4 | QA inference layer | Manual QA coverage 1 to 5 percent [V] | High | Partner with QA tools; case-level labels only |
| 5 | Compliance evidence packs | Annex III obligations from December 2027 | High | Paid module, ready mid-2027 |
| 6 | Contract leverage pack | Measured switching cost and deprecation exposure | Medium | By-product of 1 |
| 7 | Knowledge-gap detection from escalations and overrides | **Hypothesis**: overrides are free labels that point to missing content | Medium | Phase 2, aggregate only |

## 4. Design implications

- **Action-level disagreement** (ADR-021) lets certified audits cover support agents: compare resolve versus escalate, category, tool calls and refunds, not wording.
- **Judge rule:** judges may steer labeling effort and supply surrogates but never stand alone in a certificate.
- **Outcome definitions as data** (side by side, vendor and customer) is the core of the billing audit.
- **Fee rule:** no fee may depend on findings (ADR-016). A contingency fee on recovered overbilling would be profitable and would destroy independence, so it is excluded.
- **Worker monitoring:** QA scores stay case-level; no per-worker output exists anywhere in the product.

## 5. Competitive implications and moat

| Position | Why competitors cannot easily follow |
|---|---|
| Independent audit of vendor-defined outcomes | Vendors, suites and labs have a conflict of interest |
| Zero-label and label-efficient certified audits | Fixed test suites and benchmarks are the norm; the theory is new and needs engineering depth |
| Standards-based, third-party-verifiable evidence | Dashboards cannot be verified without trusting the vendor |
| Propensity-logged history per tenant | Compounds only after deployment |
| Certified suite connectors | Turns bundlers into channels |

**Threat updates.** Fastest threat: suites adding measure views (2027). Newest threat: evaluation vendors adding parity reports. Protection: speed to the first design partner, the independence charter, and a replicated, published methodology.

## 6. Profitability levers

- **Fast, fixed-price first sale** to a team facing a retirement date or an invoice dispute.
- **Low marginal cost:** the audit is compute-light and label-light by design; the main cost is integration, so productize the pilot kit and use suite marketplaces.
- **Recurring revenue** follows outcome-priced spend, which grows with agent volume.
- **Price anchors** for production platforms in the category run roughly $60K to $350K per year [V]; entry products can price below that to shorten the cycle.
- **Avoid:** contingent fees, bespoke integrations off the roadmap.
- **Unknowns to model:** sales cycle, integration hours per tenant, attach rate of billing audit and compliance packs, gross margin at 10 and 50 tenants.

## 7. Spikes before external claims

S-a replicate the paired audit on support data; S-b validate the material-difference classifier; S-c test outcome-audit interval coverage on planted truth; S-d prototype a SCITT-registered statement and test post-quantum COSE support; S-e map helpdesk export coverage; S-f test recalibration under model flips. Details in arc42 Appendix D.

## 8. Decisions

- Decided: ADR-017 beachhead.
- Accepted from Round 8: ADR-011, ADR-015, ADR-016.
- Open: D5 first design-partner profile; D6 entry-product pricing.
