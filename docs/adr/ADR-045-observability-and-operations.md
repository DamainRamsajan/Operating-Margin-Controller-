# ADR-045: Observability and operations baseline

- **Status:** Proposed (health, readiness and JSON logs implemented)
- **Context:** A pilot needs to be operable by someone who did not write the code, with stated recovery objectives.
- **Decision:** Liveness and readiness endpoints, structured logs without sensitive data, OpenTelemetry traces and metrics, stated SLOs and alerts, runbooks that are rehearsed, backups with tested restores and a disaster-recovery drill before go-live.
- **Consequences:** Operational confidence; time spent on drills; some work is only verifiable on real infrastructure.
