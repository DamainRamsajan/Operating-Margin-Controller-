# Round 12 research dossier: competitor gaps, method spread, shift, and distance for two years

Date: 29 October 2026. Claims marked [V] rest on vendor or secondary sources.

## Findings
1. **Consolidation continues.** Dynatrace completed its Arize acquisition on 1 October 2026; Cisco bought Galileo (May), ClickHouse bought Langfuse (January), Mintlify bought Helicone (March) [S44][V]. Independent evaluation vendors are becoming rare, and their buyers are observability suites. For OMC this raises the value of independence and also shows who the plausible acquirers are (Appendix E.9).
2. **Some competitors now enforce at runtime** (scoring every production run and holding or stopping actions) [V]. We have not built runtime guardrails; the gap is real but outside the verification wedge. Decision: partner or defer.
3. **The method is spreading.** Anytime-valid, paired acceptance tests (PACE), adaptive auditing and conformal selective acting are all in the 2026 literature, and the model-update audit paper cites betting-style paired tests as related work [S29][S45]. A lead cannot rest on the statistic. We responded by tightening our own bounds and shifting the moat to integration, independence, evidence, data and distribution.
4. **Certificates do not travel across distributions.** One 2026 study found static conformal guarantees violated in 14 of 16 cross-dataset transfers while an anytime-valid monitor with full feedback stayed valid [S45]. We added a stationarity warning and a re-qualification rule (ADR-038) and put windowed audits on the roadmap.
5. **Eval in the pull request is standard** (Round UX), so the comment and the status check are table stakes, now implemented.

## What we changed in the product
| Change | Effect (simulation, synthetic worlds) |
|---|---|
| Mixture bound for the disagreement rate (ADR-036) | Equivalent, rarely-disagreeing models certify in a median of 3,000 cases instead of 9,250; regression at twice the tolerance flagged in 55 percent of runs instead of 31 percent; 0 false certificates in 600 runs |
| Real public-data rerun | Equivalent candidate certified in 100 percent of runs at tolerance 0.01 (was 90 percent); regression rejected in 88.5 percent at tolerance 0.03 (was 66.5 percent); no false certificates |
| Parity audit for logged metrics (ADR-037) | Business-metric non-inferiority with signed statement; false promotion rate below alpha in test |
| Stationarity warning (ADR-038) | Warns on planted shifts, silent on steady traffic |
| Verdict-first language and PR comment | Plain-language verdicts; sticky comment; required status check |

## Gap matrix and plan
See arc42 Appendix A.4 (gap analysis against competitor classes) and A.5 (two-year distance plan). Honest summary: we lead on signed, certified, label-efficient, independent verdicts; we trail on enterprise readiness, polished UI, runtime guardrails, tracing depth and distribution. The plan fills the first two, imports the third and fourth, and partners for the fifth.

## Decisions needed
D13 server-rendered console; D14 first personas; D15 read-only first release (all recommended yes, see Appendix D).
