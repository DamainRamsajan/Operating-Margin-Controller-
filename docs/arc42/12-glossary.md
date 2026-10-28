# 12. Glossary

| Term | Meaning |
|---|---|
| Action-level disagreement | Two executors differ in a consequential decision (resolve or escalate, tool call, refund, category), not merely in wording |
| AIPW | Augmented inverse-propensity weighting: a doubly robust effect estimator |
| Anytime-valid | Statistical guarantee that stays valid under continuous monitoring and any stopping time |
| Assumed resolution | A vendor-billed resolution inferred from customer silence or departure, not confirmed by the customer |
| Baseline | The current process, always an available option and the safe fallback |
| Bake-off | Randomized comparison of vendors, models or configurations on identical live traffic |
| Case class | Group of similar cases used for aggregation and calibration |
| Confidence sequence | Interval sequence that covers the true value at all times simultaneously |
| Confirmed resolution | A resolution the customer affirmed |
| Conformal calibration | Finite-sample risk guarantee from calibration data |
| COSE, COSE_Sign1 | CBOR object signing format used for signed statements |
| Decision point, enforcement point | OMC decides; customer systems enforce |
| Disagreement rate | Fraction of traffic where incumbent and candidate differ at the chosen decision level; observable without labels |
| Equivalence or non-inferiority test | Test that a replacement is no worse than the incumbent by a stated margin |
| Evidence grade | E0 to E3 label stating how an estimate was obtained |
| Gold label | Verified ground-truth outcome from expert review or audit |
| OCEL | Object-centric event log standard |
| Overlap (positivity) | Every compared option had a nonzero chance of being chosen |
| PPI | Prediction-powered inference: combines abundant predicted labels with few gold labels while keeping valid intervals |
| Propensity | Probability that the logged option was selected |
| Qualification set | Cases used to certify a replacement model |
| Realization rate | Realized causal value divided by projected value |
| Re-qualification tax | Recurring cost of proving a replacement model is safe for production workflows |
| Reference lane | Slice of cases always run on the baseline for guardrails and drift detection |
| Regime shift | Change in model, provider, rule or data that breaks earlier calibration |
| SCITT | IETF architecture for transparent, signed statements registered with a transparency service |
| Switchback | Experiment design that toggles an intervention over time windows |
| Transparency service | Service that registers signed statements and issues receipts proving registration |
| Work twin | Process graph with currency annotations of how work really runs |
| AIUC-1 | Certification standard for AI agents maintained by the Artificial Intelligence Underwriting Company; includes live behavior testing [S31][V] |
| Authority rule | Versioned limit or eligibility condition that defines what an action may do without escalation |
| Control mapping | Declared link between a statement type and the controls of a framework it can support |
| Leakage | Currency moved by actions outside policy authority |
| Review Workbench | Expert labeling interface with blinded comparisons and visible sampling plans |
| SCRAPI | SCITT reference HTTP API for transparency services |
| Verifier CLI | Open-source tool that verifies statements, signatures and receipts offline |
| Chatbot purgatory | An interaction loop in which a customer cannot reach a human despite asking |
| Human-access compliance | Measured disclosure, availability of a human-request feature, time to a human and escalation success against a named rule set |
| Promotion gate | A CI/CD step that returns a signed promote, hold or reject verdict for a model or prompt change |
| Replay Privacy Gate | Control that screens replay and shadow sets for residual personal data and provider terms before any external call |
| Residual leakage | Estimated fraction of sensitive content that survives redaction |