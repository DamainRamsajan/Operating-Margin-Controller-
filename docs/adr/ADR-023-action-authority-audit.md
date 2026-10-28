# ADR-023: Action authority audit

- **Status:** Accepted (26 October 2026, founder decision D7; spike S-g pending)
- **Context:** Agents issue refunds, credits and discounts; one practitioner account describes a credit issued with no log explaining the trigger or authority; refunds can double-pay alongside chargebacks; vendor liability caps often limit recourse [S35][V].
- **Decision:** Add BB19: authority rules as versioned data, deterministic checks where possible, sampled expert review with prediction-powered correction where not, currency-denominated leakage estimates with intervals, guardrail calibration through the risk gate, and a signed liability evidence pack.
- **Consequences:** Direct dollar value and a third entry product; depends on rule documentation (R30); legal framing of evidence packs needs counsel.
