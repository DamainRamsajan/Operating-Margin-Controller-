# ADR-006: Estimator isolation and registry

- **Status:** Proposed
- **Context:** Reproducibility is quality goal 1.
- **Decision:** Estimators ship as signed, content-addressed images with no network egress; plans pin versions.
- **Consequences:** Release discipline and slower estimator changes; replay is exact.
