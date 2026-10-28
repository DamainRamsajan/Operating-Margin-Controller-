# 10. Quality requirements

## 10.1 Quality tree

| Quality | Sub-attribute | Scenarios |
|---|---|---|
| Credibility | Reproducibility, valid uncertainty, certified verdicts | Q1, Q2, Q15 |
| Safety | Bounded risk, fail-safe | Q2, Q6, Q10 |
| Efficiency | Time to value, decision latency, label cost, cost of OMC | Q3, Q9, Q11, Q12 |
| Changeability | Provider swap, telemetry change, retirement response | Q4, Q5, Q13 |
| Privacy | No person-level outputs | Q7 |
| Durability | Evidence longevity, transparency | Q8, Q14 |
| Fairness of measurement | Independence, reproducible randomization | Q16, Q17 |

## 10.2 Quality scenarios

| ID | Scenario | Measure |
|---|---|---|
| Q1 | Finance re-runs a published statement without OMC services | Match within stated tolerance; 1 hour or less |
| Q2 | Explored decisions run for 30 days | Observed error rate at or below the declared budget with the agreed confidence; a breach triggers fallback |
| Q3 | Read-only access granted | Ranked leak report, cost-per-outcome baseline and exposure inventory in 5 business days or less |
| Q4 | A model provider is added or swapped | Configuration and one adapter; no policy-engine change; 1 day or less |
| Q5 | A telemetry schema version changes | New adapter in production within 2 weeks |
| Q6 | Kill switch tripped | Baseline decisions within 60 seconds |
| Q7 | Any export or API response | Rejected by schema check if it contains person-level identifiers or person-level performance metrics; zero tolerance |
| Q8 | A signature algorithm weakens | Chain re-anchored on schedule; offline verifier validates all history |
| Q9 | In-line decision request | p99 of 250 ms or less; timeout returns baseline |
| Q10 | Model identity changes | Learning frozen within 1 minute; baseline-only restriction until requalification |
| Q11 | Steady state | OMC run cost at or below 10 percent of measured savings (target to validate) |
| Q12 | Deprecation notice received | Exposure report in 2 business days; verdict on a typical workflow in 10 business days; rollback available until retirement. Label spend target set after spike S-a |
| Q13 | Retirement date within 60 days | Calendar alert at notice; no workflow reaches retirement unqualified without an explicit risk acceptance record |
| Q14 | Evidence Statement issued | Validates against the published schema, verifies offline, and carries a transparency receipt |
| Q15 | Outcome audit on planted-ground-truth tests | Interval coverage at or above nominal for the true-outcome rate; certified audits show zero false certificates in the test campaign |
| Q16 | Bake-off allocation | 100 percent of decisions carry logged propensities; randomization reproducible from the case-reference hash |
| Q17 | Label routing | Static check proves routing functions cannot read outcome fields; violations fail the build |
| Q18 | A partner verifies a shared statement | Offline, without contacting OMC; passes all published test vectors |
| Q19 | Action authority audit on planted-ground-truth tests | Leakage-rate interval coverage at or above nominal; deterministic checks have zero false negatives on rule violations in the test set |
| Q20 | Review Workbench batch | Experts complete a sampled batch within the agreed time budget; blinded comparisons expose no model or vendor identifiers |
| Q21 | Control mapping published | Each statement type lists supported controls and evidence provided; mapping versions are signed |
| Q22 | Human-access compliance audit on planted-ground-truth tests | Rate-interval coverage at or above nominal; time-to-human computation matches ground truth on every planted case |
| Q23 | Replay set released to an external provider | Provider terms check passed; residual-leakage upper bound below the policy limit; provenance recorded; no set leaves the tenant otherwise |
| Q24 | CI promotion gate call | Signed verdict returned within the agreed time on imported datasets; verdict registered in the transparency service |
| Q25 | Compliance statement issued | Names rule-set versions, states measurements only, and contains no legal conclusion; verified by a schema check |
