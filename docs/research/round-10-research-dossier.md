# Round 10 research dossier: assurance ecosystem, business model, action authority, moat

Date: 26 October 2026. Builds on Rounds 8 and 9. Claims marked [V] rest on vendor, press or secondary sources. Items marked **hypothesis** are analysis, not published results.

## 1. Findings

1. **The assurance ecosystem consolidated around controls and agent behavior in the last eight weeks.** KPMG became the first Big Four firm with AIUC-1 certification (27 August 2026). The AICPA and AIUC announced a joint SOC 2 plus AIUC-1 offering delivered as one CPA-led engagement (19 October 2026). Reports say AIUC raised a $40M Series A in September, and that support vendors including Fin have certified products [S31][V]. ISO/IEC 42001 is moving into national accreditation, and a CSA note observes that the system for assuring the assurers lags behind [S32]. Insurers converge on NIST AI RMF, ISO/IEC 42001 and AIUC-1, and third-party validation shortens underwriting [S33][V].
2. **None of that measures outcome truth, change safety or action authority.** AIUC-1 tests agent behavior live; SOC 2 and ISO 42001 certify controls. A customer still cannot get an independent answer to: did the vendor bill for real resolutions, is the replacement model no worse, and did the agent move money within policy? That is OMC's space, and the certifiers are potential channel partners, not only competitors.
3. **The compliance-automation analogue gives a business model.** Vanta is estimated near $300M ARR (April 2026), growing about 69 percent, valued at $4.15B in July 2025. It sells subscriptions priced by size, frameworks and modules; audits are bought separately from partner auditors; direct switching between leaders is rare; low-frequency usage is its churn risk [S34][V]. OMC's workflows are operational, which addresses the usage-frequency weakness.
4. **Trust is the premium.** An alleged certificate-mill case in March 2026 (near-identical SOC 2 reports from an automated vendor) pushed the market back toward established players [S34][V]. For OMC this argues for reproducible evidence, published methods and no sale of certificates.
5. **Action authority is a real, unowned money problem.** Practitioner accounts describe an agent issuing an unapproved credit with no log explaining the trigger or the authority; refund guides warn of double-refunds when a chargeback also credits the customer; analysts note vendor liability may be capped at trailing fees while the deploying business bears the loss; regulators say responsibility stays with the business [S35][V]. Small vendors detect unauthorized actions in conversations, but I found no independent, statistical, cross-vendor leakage estimate with signed evidence.
6. **Standards progress.** SCRAPI, the SCITT reference API, reached draft 11 (26 June 2026) with intended status Proposed Standard and sits in the RFC Editor queue [S36][V]. Post-quantum signature support in COSE remains unconfirmed.

## 2. Moat, strengthened

See arc42 section 4.8. Additions this round: assurance-ecosystem fit (control mappings, partner interface), a public open-source verifier with test vectors, a published methodology with replication, and "own your evidence, rent our engine". The principle: let customers and partners verify us without trusting us, and become the evidence substrate the certifiers and insurers lack.

## 3. Profitability, strengthened

| Lever | Mechanism | Evidence or reasoning |
|---|---|---|
| Land with fixed fees tied to a trigger event | Retirement notice, invoice dispute, leakage concern | Short cycle, existing budget |
| Expand by module | Qualify, Audit, Control, Comply | Same ingestion, labels, ledger and vault; analogue in compliance automation [S34][V] |
| Keep cost of goods low | Customer-supplied gold labels, disagreement-only labeling, capped inference pass-through | ADR-024, Appendix E |
| Use partners for delivery | CPA firms and certifiers deliver attestations; OMC sells the platform | Analogue; no contingent fees (ADR-026) |
| Raise usage frequency | Operational audits and bake-offs, not annual audits | Avoids the churn risk of low-frequency compliance tools |
| Build a data asset | Propensity-logged history, calibration, classifiers | Compounds only after deployment |

## 4. Low-hanging value for the customer demographic, ranked

| Rank | Opportunity | Evidence | Reuse | Status |
|---|---|---|---|---|
| 1 | Certified model qualification | Retirement calendars; certified-audit literature | Very high | Entry product (ADR-011) |
| 2 | Outcome billing audit | Vendor-defined outcomes [V] | High | Entry product (ADR-020) |
| 3 | **Action authority audit** | Unauthorized credits and refunds, double-payment, liability caps [S35][V] | High | New entry product (ADR-023) |
| 4 | Vendor bake-off | Proof-of-concept comparisons | High | Phase 2 |
| 5 | Contract Evidence Pack | Liability caps, deprecation notice, audit rights, SLA credits [V]; **hypothesis** that measured breaches support credit claims | Medium | Proposed (FR22) |
| 6 | Partner-delivered attestations | Joint SOC 2 plus AIUC-1 offering [S31][V] | Medium | Phase 2 partner program |
| 7 | Compliance packs | Annex III dates | High | Phase 2 |
| 8 | Insurer evidence feed | Underwriting convergence [S33][V] | Medium | Phase 3 |

## 5. Competitive implications

- AIUC-1 live testing and CPA-led engagements move toward behavior and controls; OMC should stay complementary and supply outcome, change and authority evidence.
- Compliance-automation vendors (Vanta, Drata) are adding AI governance modules and could add monitoring; they lack causal and statistical measurement of business outcomes.
- Action monitors exist at small scale; differentiate on statistical estimates, cross-vendor scope and signed evidence.
- Suites remain the main bundling threat (Round 8).

## 6. Risks added

R26 assurance incumbents extend live testing; R27 trust damage from low-quality automated assurance; R28 partner arrangements compromise independence; R29 dependence on customer experts for gold labels; R30 undocumented authority rules.

## 7. Verification items

Whether certification claims for named support vendors are accurate; scope of the AICPA and AIUC offering; whether control mappings are accepted by certifiers (spike S-h); SCRAPI RFC status; post-quantum COSE support; legal framing of liability evidence packs.

## 8. Decisions needed

D7 adopt the third entry product and ADR-022 to ADR-026 (recommended yes); D8 verifier licence; D9 first assurance partner to approach; D5 and D6 remain open.
