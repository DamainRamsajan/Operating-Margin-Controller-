# ADR-004: Customer-tenant data plane with a hosted control plane

- **Status:** Proposed
- **Context:** Sovereignty, security review and EU buyers.
- **Decision:** Raw data stays in the tenant; the control plane holds registry, catalog, feeds, console API and updates, and sees metadata and aggregates only.
- **Consequences:** More deployment effort; an update service is required; stronger trust.
