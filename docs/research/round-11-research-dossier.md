# Round 11 research dossier: compliance deadlines, developer-tool crowding, replay privacy, channels, valuation reality

Date: 27 October 2026. Builds on Rounds 8 to 10. Claims marked [V] rest on vendor, press or secondary sources. Items marked **hypothesis** are analysis.

## 1. Findings

1. **Chatbot laws now create measurable obligations with near-term deadlines.** California AB 1609 was signed on 28 September 2026 and applies from 1 January 2027 to businesses above $500 million revenue: no representing a customer-service chatbot as human, a clear disclosure when a reasonable person could be misled, a simple way to request a human during regular hours, and a good-faith effort to connect within 15 minutes or schedule a callback within one business day, with limits on hold and cumulative wait times. Spain's Law 10/2025 gives customers the right to reach a live human and sets answer-time standards, with a compliance deadline of 28 December 2026. EU AI Act Article 50 has applied since 2 August 2026, and the EU has no general right to a human yet but several sector rules do. Commentary names the failure mode chatbot purgatory [S37][V]. These are measurable (timestamps, request recognition, loops), which makes them a good fit for OMC's evidence machinery.
2. **The migration wedge is crowded at the developer-tool layer.** Open-source and commercial tools already import production traces, replay them against a candidate model, run shadow reports, open upgrade pull requests and gate CI. Examples: Kitaru, llmshift ("Dependabot for AI models", with lifecycle data compiled from provider deprecation pages), gatelane, Braintrust, LangSmith backtesting, Langfuse sliced-trace experiments, Datadog single-trace replay. One project's own comparison notes that none signs a promotion report [S39][V]. Replay mechanics are therefore commoditizing; the defensible layer is the certified verdict, business-metric parity, independence and evidence.
3. **Replay sets are a privacy boundary.** Evaluation sets are usually real customer transcripts. A 2026 preprint finds no single privacy technique dominates; local routing plus redaction plus rephrasing left 0.6 percent residual PII leakage in its test. Redactor models trained on real data can themselves leak [S40][V]. Support teams will not run replay without a privacy answer.
4. **Marketplaces are the procurement shortcut.** Salesforce unified its marketplace in April 2026 with a $50M builders initiative; ServiceNow launched a build partner program and an AI agents category in January 2026; Microsoft's marketplace ties co-sell to committed cloud spend and reports more than $22 billion of co-sold partner revenue. The same companies are building competing control planes [S41][V].
5. **Regulatory update.** One source reports the Digital Omnibus on AI was adopted by the Council on 29 June, signed on 8 July, published on 24 July and in force on 27 July 2026, fixing 2 December 2027 for Annex III and 2 August 2028 for Annex I [S38][V]. This removes a verification item once confirmed on EUR-Lex.
6. **Valuation reality.** Vanta was valued at $4.15B in July 2025 on estimated ARR near $220M (about 19 times) and was near $300M ARR by April 2026 [S42][V]. A $7B outcome implies several hundred million ARR at comparable multiples or a strategic premium. The earlier pre-revenue $6B+ precedents were frontier-lab teams.

## 2. What this changes

| Area | Change |
|---|---|
| Value for customers | New compliance module: human-access and disclosure audit (ADR-027); Replay Privacy Gate (ADR-029) |
| Moat | Interoperability (import adapters, CI gate) so OMC is the verdict layer others call (ADR-028); certified verdicts and independence stay the differentiators |
| Functionality | CI promotion gate; leakage-bounded replay; compliance statements |
| Profitability | Marketplace channels to shorten procurement (ADR-030); compliance module with dated triggers; E.7 and E.8 in Appendix E |
| Distance from competitors | Do not compete on runners, replay or dashboards; compete where nobody signs, certifies or stays independent |

## 3. Opportunities ranked (customer value, deadline, reuse)

| Rank | Opportunity | Why now | Reuse |
|---|---|---|---|
| 1 | Certified model qualification with CI gate | Retirements plus crowded tooling needs a verdict layer | Very high |
| 2 | Human-access and disclosure audit | Deadlines 28 December 2026 and 1 January 2027 | High |
| 3 | Outcome billing audit | Vendor-defined outcomes | High |
| 4 | Action authority audit | Unauthorized credits and liability caps | High |
| 5 | Replay Privacy Gate (enabler and product) | Unblocks legal review | Medium |
| 6 | Marketplace distribution | Procurement shortcut | Not a product |

## 4. Honest limits

- Statute summaries come from law-firm and trade pages; counsel must confirm applicability, thresholds and dates.
- AB 1609 applies to large businesses, so the first compliance pilots target large customers; smaller companies serving Spain may still be in scope under Spanish law.
- The compliance module is only worth building small: deterministic checks plus sampled review.
- Developer-tool claims come from project pages; several are early versions.
- Channel economics are hypotheses; fees change.

## 5. Decisions needed

D10 adopt the compliance module and ADR-027 to ADR-030 (recommended yes); D11 first marketplace; D12 engage compliance counsel before the first compliance pilot; D5, D6, D8 and D9 remain open.
