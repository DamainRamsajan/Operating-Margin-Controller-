# ADR-019: Disagreement-supported certified migration audits

- **Status:** Proposed (pending spike S-a)
- **Context:** For a prediction-determined loss, the risk difference between two models lives on inputs where they disagree, observable without labels. A published protocol certifies benign updates with zero labels and labels only sampled disagreements through an anytime-valid confidence sequence, valid under any pre-label routing and composable across a sequence of updates; it reports large label savings on classification and small language-model updates [S29]. It is a single-author preprint, and it excludes open-ended judged text.
- **Decision:** Implement a two-tier audit in the Migration Gate: Tier 0 zero-label certificate; Tier 1 disagreement-only labeling with per-slice verdicts and a lifetime error budget. Label routing may use judges but never reads the outcome (TC8). Windowed variants handle drift.
- **Consequences:** Low label cost on benign swaps; validity does not depend on judge quality; theory scope limits require ADR-021; replication on support data is mandatory before external claims.
