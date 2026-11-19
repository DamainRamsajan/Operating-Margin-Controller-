# ADR-035: Review Workbench constraints

- **Status:** Proposed (extends ADR-024)
- **Context:** Reviewers can be anchored by model confidence and fatigued by long sessions; per-reviewer rankings would amount to worker monitoring (arc42 RC2).
- **Decision:** One atomic decision per screen, blinded random A/B order, no confidence scores, keyboard shortcuts, time-boxed batches, known-answer checks and an overlap sample for agreement. Reviewers see only their own statistics; managers see batch-level quality only.
- **Consequences:** Better label quality and lower regulatory risk; less visibility for managers; needs batch-level quality metrics.
