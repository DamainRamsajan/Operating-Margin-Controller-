# ADR-001: Canonical object-centric event model behind anti-corruption adapters

- **Status:** Proposed
- **Context:** Telemetry standards are unstable [S6]; sources are heterogeneous.
- **Decision:** One internal model aligned with OCEL 2.0; every source enters through a versioned adapter.
- **Consequences:** Adapter maintenance is the price; the core stays stable and OCEL export keeps interoperability.
