# ADR-013: MCP and A2A as first-class surfaces

- **Status:** Proposed
- **Context:** MCP and A2A are under the Agentic AI Foundation and A2A has a stable 1.0 specification [S25][V]. OpenTelemetry GenAI conventions remain unstable.
- **Decision:** OMC exposes an MCP server (ledger queries, precedent retrieval, decision requests) and acts as MCP client for read tools; it observes A2A traces. Telemetry still enters through the anti-corruption layer (ADR-001).
- **Consequences:** Agents and suites can consume OMC without bespoke integration; the decision API becomes an attack surface requiring a threat model and strict authorization.
