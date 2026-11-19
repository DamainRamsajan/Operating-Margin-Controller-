# ADR-040: Production deployment architecture for pilots

- **Status:** Proposed (pending decisions D16 and D18)
- **Context:** Pilots run inside the customer's tenant (ADR-004). A file-based workspace has no encryption at rest, concurrency control, backup or restore, so it cannot serve a real pilot.
- **Decision:** A stateless web tier and a worker tier in containers, PostgreSQL for structured data with versioned migrations, S3-compatible object storage for statements and artifacts, one deployment per customer, configuration from environment and a secret manager, signed images pinned by digest, Helm or Terraform per target cloud.
- **Consequences:** Real backup, restore and encryption; more moving parts to operate; a data-layer migration from the current file workspace.
