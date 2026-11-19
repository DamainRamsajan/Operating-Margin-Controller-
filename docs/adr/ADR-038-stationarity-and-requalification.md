# ADR-038: Stationarity warning and re-qualification rule

- **Status:** Proposed (implemented in `omc/audit/stationarity.py`)
- **Context:** Guarantees assume stable traffic, and recent work shows guarantees calibrated on one distribution can fail after a shift [S45].
- **Decision:** Every audit reports the disagreement rate in each half of the window with a two-proportion test and a warning flag in the statement and the verdict comment. A warning, or any regime shift, requires a fresh window before the verdict is relied on.
- **Consequences:** Honest limits and fewer silent failures; some extra holds; windowed audits and shift-aware certificates stay on the roadmap.
