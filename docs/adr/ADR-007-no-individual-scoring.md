# ADR-007: No individual-level worker scoring

- **Status:** Proposed
- **Context:** Task allocation by individual traits and individual performance monitoring are high-risk employment uses [RC2][V].
- **Decision:** Units of analysis are workflow, step, case class and queue; person identifiers are never features, outputs or filters; third-party QA scores are ingested at case level only.
- **Consequences:** Less personalization; lower regulatory and works-council risk; counsel must confirm.
