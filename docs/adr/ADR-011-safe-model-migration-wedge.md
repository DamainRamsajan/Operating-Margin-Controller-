# ADR-011: Safe model migration and qualification as the entry wedge

- **Status:** Accepted (23 October 2026, founder decision D1)
- **Context:** Providers retire model versions on published calendars and silent updates occur. Re-qualifying production workflows is a recurring, deadline-forced cost that existing evaluation tools address only partly [S22][V].
- **Decision:** Ship Migration Gate (BB15) in Phase 0 alongside the read-only leak report. Qualification uses a certified paired audit (ADR-019), equivalence tests on business metrics and a canary lane with rollback.
- **Consequences:** Short sales cycle and an existing budget; seeds the replay set, baseline and propensity-logged canary for the full controller. Exposed to evaluation-tool vendors and lab-native migration tooling.
