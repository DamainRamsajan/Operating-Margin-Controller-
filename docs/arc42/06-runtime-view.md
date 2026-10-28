# 6. Runtime view

## 6.1 R1: week-one discovery (read-only)

1. Customer grants read-only access; no production change requested.
2. Connectors sync history; BB2 normalizes into the canonical model.
3. BB4 builds the work twin: variants, exceptions, rework loops, reopen and recontact patterns.
4. BB5 joins cost lines (payroll rate cards, model and tool usage, vendor invoices, infrastructure) and computes cost per accepted outcome for current work.
5. BB15 builds the model-exposure inventory and retirement calendar.
6. Output: ranked leaks in currency, an AI-spend baseline per outcome, and the exposure report, labeled E0 or E1. The vault starts the chain.

## 6.2 R2: shadow policy evaluation

1. A candidate policy is declared with its measurement plan, signed before analysis.
2. BB11 evaluates it on logged data, checking overlap first: where the baseline never chose an option, the estimate cannot be identified without assumptions.
3. Results carry E1 or E2 with bounds; a power analysis states the exploration needed for E3.
4. Workflow owners decide whether to approve exploration on a bounded slice.

## 6.3 R3: gated decision loop

1. An enforcement point calls decide(case context, mode).
2. The gateway authenticates, checks mode and kill switch, assigns the lane by case-reference hash.
3. The Constraint Compiler removes options violating hard constraints.
4. The Risk Gate removes options whose risk bound exceeds the budget; the baseline remains.
5. The Optimizer scores feasible options; the Exploration Scheduler samples with probabilities at or above the floor (baseline only for the reference lane).
6. The Propensity Logger writes the decision record; the vault queues its hash.
7. The gateway returns the decision; on timeout or error it returns the baseline.
8. Execution and outcome events return; costs are attributed; the Label Service schedules gold sampling by pre-label routing rules only.
9. BB11 updates estimates and publishes weekly statements; BB7 recalibrates; policy changes go through approval.

## 6.4 R4: regime shift

1. Triggers: model identity change, provider incident notice, drift breach, rule or data change flag.
2. BB3 records a regime boundary, tagged **planned** (a qualified migration) or **unplanned** (a silent provider change); the optimizer freezes learning across it.
3. Decisions restrict to the baseline and last-qualified options; intervals widen and calibration windows restart.
4. For unplanned shifts, BB15 runs a certified audit between the previous and current behavior using the shadow comparator before normal operation resumes.
5. Statements split at the boundary.

## 6.5 R5: finance audit replay

1. Finance selects a published statement.
2. The vault verifies the chain, signatures and transparency receipts.
3. The signed plan and estimator image digest are retrieved.
4. Inputs are fetched by reference and recomputed in an isolated runner.
5. The result is compared with the published figure within tolerance; a verification report is produced.
6. Any mismatch opens an incident and flags the statement unverified.

## 6.6 R6: congestion-aware experiment

1. BB8 forecasts review-queue load and service rates.
2. The scheduler places random-duration switchback windows away from peaks.
3. The queue-aware estimator corrects for interference between waiting cases [S10].
4. A window aborts automatically if review-queue service levels breach their threshold.

## 6.7 R7: kill switch and fallback

1. An operator or automated breach rule (risk violation rate, service-level breach, cost spike) trips the switch.
2. Within 60 seconds the gateway returns baseline decisions and adapters revert enforcement points to baseline configurations.
3. An incident record is written to the vault; review precedes any restart.

## 6.8 R8: label acquisition

1. The Label Service ranks unlabeled cases for gold review by expected variance reduction or, for audits, by a routing rule that never reads the outcome.
2. Selected cases go to human gold review within a weekly budget; overrides captured in normal work are added at no extra cost.
3. Judge, QA and surrogate scores are recalibrated against the gold sample and enter estimators as prediction-powered inputs [S9].

## 6.9 R9: model migration qualification

1. A deprecation notice arrives (feed or manual) or the vault detects a new model identity.
2. BB15 computes exposure: workflows, volume, spend and days to retirement.
3. The Qualification Set Builder assembles historical cases by case class, hard cases and recent drift; every set passes the Replay Privacy Gate (section 6.17) before any provider call.
4. Shadow Comparator scores a live copy of traffic (and the replay set) with incumbent and candidate and computes the disagreement indicator at decision or action level.
5. **Tier 0.** If the confidence-sequence upper bound on the disagreement rate, scaled by the loss bound, falls below the tolerance, a no-regression certificate is issued with zero labels.
6. **Tier 1.** Otherwise sampled material disagreements go to gold review, routed by rules that never read the outcome, and an anytime-valid sequence issues a no-regression verdict or a regression alarm, with per-slice verdicts [S29].
7. The Equivalence Tester checks business-metric parity against the owner's margins.
8. A canary lane runs behind the risk gate with automatic rollback until the retirement date.
9. Promotion produces a signed Evidence Statement (tolerance, confidence, verdict, stopping time, labels spent, slice table), registered in the transparency service; the calendar updates; the sequence-level error budget is debited.

## 6.10 R10: outcome billing audit

1. The Definition Registry records the vendor's outcome definitions (for example confirmed and assumed resolutions).
2. BB1 ingests the vendor's resolution and billing export and the helpdesk's reopen, recontact and CSAT events.
3. The Label Service draws a gold sample stratified by vendor definition and case class; QA or judge scores add prediction-powered inputs [S9].
4. The True-Outcome Estimator produces the accepted-outcome rate per vendor, definition and period with intervals.
5. The Billing Reconciler compares billed outcomes with estimated true outcomes and flags disputed segments.
6. A Dispute Evidence Pack is issued as a signed statement; no fee depends on the finding (ADR-020).

## 6.11 R11: vendor bake-off

1. The customer approves a risk budget and a traffic share for comparison.
2. The Bake-off Allocator assigns live cases at random across vendors, models and the human baseline, logging propensities.
3. The risk gate removes any option breaching the budget; the baseline is always available.
4. The Comparison Tester runs anytime-valid comparisons on accepted-outcome rate, cost per accepted outcome and cycle time, with per-slice verdicts.
5. A decision memo (signed statement) states which vendor or configuration wins on which slices and with what grade.

## 6.12 R12: precedent retrieval (Proposed)

1. An agent requests precedents through the MCP surface with a minimum evidence grade.
2. The Precedent Store returns only entries meeting the grade, with unexpired provenance and permitted scope.

## 6.13 R13: action authority audit

1. The Authority Rule Registry loads policy rules and system limits as versioned data; owners confirm them.
2. BB1 ingests consequential actions with amounts from the helpdesk, billing and agent traces.
3. Deterministic checks classify machine-checkable actions (above ceiling, outside window, duplicate with a chargeback credit).
4. A stratified sample of context-dependent actions goes to expert review in the Review Workbench; judge scores add prediction-powered inputs [S9].
5. The Leakage Estimator reports the outside-authority rate and currency amount with intervals per vendor, action type and case class.
6. The Guardrail Calibrator proposes ceilings and escalation thresholds with the expected leakage and review-load tradeoff.
7. A Liability Evidence Pack is issued as a signed statement; no fee depends on the finding (ADR-016).

## 6.14 R14: partner attestation

1. The customer authorizes a partner (CPA firm, certifier or insurer) to receive selected statements.
2. The partner verifies statements offline with the public verifier and checks transparency receipts.
3. Control mappings show which framework controls each statement supports.
4. The partner issues its own attestation or underwriting view. OMC issues no certificates and takes no fee that depends on the outcome (ADR-022, ADR-026).

## 6.15 R15: contract evidence pack (Proposed)

1. Contract terms (service levels, outcome definitions, deprecation notice, liability caps, audit and export rights) are entered as versioned data.
2. OMC compares measured performance with the terms and flags breaches and unmet notice periods.
3. Output: breach evidence for credits and negotiation positions for renewal (shadow-scoring and export rights, definitions, notice periods).

## 6.16 R16: human access and disclosure compliance audit

1. Counsel enters and confirms the jurisdiction rule sets in the Rule Set Registry.
2. BB1 ingests helpdesk, chat, telephony and escalation events; the Event Extractor builds HumanRequestEvent, DisclosureEvent and EscalationOutcome records.
3. The Deterministic Checker computes time to a human, queue times and availability during required hours for every request.
4. A stratified sample goes to expert review in the Review Workbench: was a request recognized, was disclosure accurate, was the customer trapped in a loop; judge scores add prediction-powered inputs [S9].
5. The Compliance Estimator reports rates with intervals by channel, jurisdiction and period.
6. A signed Compliance Statement is issued, with assumptions and rule-set versions; it states measurements, not legal conclusions.

## 6.17 R17: replay privacy gate

1. A replay or shadow set is requested by the Migration Gate or an audit.
2. The Provider Terms Checker verifies retention, training and region terms for each external provider.
3. The Local-First Router scores locally where possible; remaining content passes the Redactor and Rephraser.
4. The Leakage Auditor reviews a sample and estimates residual leakage with an interval; a set above the policy limit is blocked.
5. The Provenance Recorder writes ReplaySetProvenance and links it to the resulting statements.

## 6.18 R18: CI promotion gate

1. A pipeline step calls the OMC gate with a candidate model or prompt change and a dataset reference imported from a developer tool.
2. OMC runs the certified audit and equivalence tests (section 6.9) on the qualification set and shadow traffic.
3. The gate returns a signed verdict (promote, hold or reject) with grade, tolerance and labels spent; the verdict is registered in the transparency service.
4. A held or rejected verdict blocks the pipeline; a promoted verdict starts the canary lane.
