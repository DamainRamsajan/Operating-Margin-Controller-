# From arc42 building blocks to code

| arc42 block | Module | State |
|---|---|---|
| BB1 Connector Layer | `omc/ingest/csv_adapter.py` | CSV only |
| BB2 Ingest and Normalize | `omc/canonical/models.py` | minimal records |
| BB3 Canonical Event Store | not built (files on disk) | planned |
| BB4 Work Twin | `omc/report/leaks.py` | descriptive only |
| BB5 Unit Economics | `omc/report/leaks.py` | cost per accepted outcome |
| BB11 Causal Ledger | `omc/stats/`, `omc/audit/` | certified paired audit only |
| BB12 Evidence Vault | `omc/vault/`, `omc_verify/` | Ed25519, hash chain |
| BB15 Migration Gate | `omc/exposure/`, `omc/audit/gate.py` | exposure, audit, gate |
| BB21 Replay Privacy Gate | `omc/privacy/gate.py` | rule-based v1 |
| Everything else | not started | see MILESTONE-M0.md backlog |
