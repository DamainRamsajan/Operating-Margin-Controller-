# 8. Cross-cutting concepts

## 8.1 Unit-economics model

Net value per case = P(accept) x V - (C_exec + C_tool + C_review + C_infra) - P(error) x L - C_delay x T

where V is the value of an accepted outcome, L the loss when an error escapes, T the cycle time. Cost per accepted outcome = total cost / accepted outcomes. The same formula serves discovery, risk pricing, optimization, vendor comparison and reporting, so the numbers reconcile. For outcome-priced vendors, cost per accepted outcome uses the audited true-outcome rate, not the billed count.

## 8.2 Identity and propensity logging

Every decision has a stable identifier, the full candidate and feasible sets, and the probability of the chosen option. Never skipped.

## 8.3 Evidence grades

Section 4.4 applies to statements, dashboards, exports and billing.

## 8.4 Privacy and the no-individual-scoring rule

Aggregation units are workflow, step, case class and queue. Person identifiers are pseudonymized at ingestion and are not features, outputs or filters. Reports cannot be sliced to an individual. Third-party QA scores are ingested at case level as labels, never published per worker. This guards against employment-related high-risk classification and is a trust feature for works councils [RC2][V].

## 8.5 Security

Tenant isolation; least-privilege read-only connectors; secrets in KMS; signed images; sandboxed estimators; signed policy and plan changes; audit of OMC administrators. The decision API and any MCP surface are attack surfaces and carry a threat model covering prompt injection, tool abuse and authorization (ADR-013, Proposed).

## 8.6 Human oversight by design

Mandatory-human steps are hard constraints; reviewers can override and each override is logged as a label; high-risk actions can be held for review without a live-queue watcher; the vault provides a queryable record [S4][S5]. Review workload is modeled in BB8 so oversight does not silently degrade under volume.

## 8.7 Versioning

Semantic versions for schemas, adapters, estimators, policies and the Evidence Statement schema; every statement records the versions used; breaking changes require a new estimator major version and re-runs of affected statements.

## 8.8 Testing

- Synthetic worlds with planted ground truth for estimator coverage and bias, including planted model flips for audits.
- A/A tests for false discoveries.
- Coverage tests for conformal, prediction-powered and anytime-valid intervals under drift.
- Replay tests: every release reproduces archived statements.
- Chaos tests: connector loss, delayed labels, model-version flips, queue surges, vendor export gaps.

## 8.9 Observability of OMC itself

OMC emits traces and metrics in the canonical model; its decisions are auditable through the same vault.

## 8.10 Cost governance of OMC

OMC tracks its own compute and inference (including shadow scoring) as cost lines and compares them with the savings it measures.

## 8.11 Fail-safe behavior

Every failure resolves to the baseline: timeouts, missing features, unhealthy dependencies, breached budgets, regime changes.

## 8.12 Currency and localization

Multi-currency cost lines with dated conversion; locale-aware reporting; time zones recorded per source.

## 8.13 Action-level disagreement for generative agents

Certified audits need an observable disagreement signal and a loss determined by the prediction. Free text is neither. OMC therefore defines disagreement at the level of consequential decisions: resolve or escalate, intent and category, tool calls made, refund or credit issued, policy-compliance flags, handoff reason. Two answers that differ only in wording do not disagree. A material-difference classifier (versioned, audited against gold) decides when two free-text answers are materially different; its errors affect label efficiency and are reported, not hidden. Residual free-text quality is measured with prediction-powered inference and graded E2 (ADR-021).

## 8.14 Judge rule

Judges, QA models and classifiers may route labeling effort and supply surrogate scores. They never stand alone as evidence in a certificate, and label routing never reads the outcome. Validity then does not depend on judge quality; only cost does. Judge drift is monitored separately (section 6.4) [S29].

## 8.15 Standards alignment

Statements use COSE and SCITT structures; telemetry arrives through adapters; MCP and A2A are first-class surfaces; OCEL is the process-log format; FOCUS is used for cost exports where available. Where a standard is draft or individual-submission, OMC pins the version and records the dependency.

## 8.16 Vendor-neutral measurement

Outcome definitions are data. OMC never adopts a vendor's definition as its own; it reports results under the vendor's definition and under the customer's definition side by side.

## 8.17 Own your evidence, rent our engine

Customers hold their statements, inputs references and verifier, and can verify any claim without OMC services. Stickiness is meant to come from embedded workflows and accumulated calibration, not from holding evidence hostage.

## 8.18 Control mapping

Each statement type declares which controls in AIUC-1, ISO/IEC 42001, SOC 2 and NIST AI RMF it can support and what evidence it provides. Mappings are versioned and signed, and OMC claims support for a control, never certification [V].

## 8.19 Money-at-risk thresholds

Every action type with currency impact carries an authority rule, a ceiling and an escalation threshold. Audits state leakage in currency with intervals, and guardrail changes go through the risk gate.

## 8.20 Compliance evidence stance

OMC measures; counsel interprets. Rule sets are versioned data entered by the customer's counsel, statements state measured results against a named rule-set version, and no statement asserts that a law is or is not satisfied.

## 8.21 Replay privacy by design

Production transcripts are treated as personal data. Scoring is local-first, external calls need passed provider-terms checks and an audited residual-leakage bound, and every set carries provenance. Leakage is measured and reported, never assumed zero.

## 8.22 Interoperate before building

Replay, tracing and evaluation running are commoditizing in developer tools. OMC imports their datasets and traces and returns signed verdicts, and builds only the layers they lack: certified statistics, business-metric parity, independence, evidence and compliance.
