# 3. Context and scope

## 3.1 Business context

```
  Workflow owners ──┐                                ┌── Finance, auditors
  IT manager ───────┤                                │
  Reviewers ────────┤          ┌───────────┐         │
                    └─────────►│    OMC    │◄────────┘
  Helpdesks and systems of record ►│           │──────► Agent platforms / routers (enforcement points)
  AI support vendors (traces, billing) ►│           │──────► Helpdesk annotations (advisory)
  Model gateways, deprecation feeds ───►│           │──────► Transparency service (SCITT) and timestamp anchors
  QA and judge tools (scores) ─────────►└───────────┘
```

| Partner | Sends to OMC | Receives from OMC |
|---|---|---|
| Helpdesks and systems of record (Zendesk, Intercom, Salesforce Service Cloud, ServiceNow, ERP) | Cases, state changes, reopen and recontact events, CSAT | Annotations, advisory flags (Phase 2: routing hints) |
| AI support vendors and in-house agents | Traces, tool calls, model identity, billed outcomes and resolution exports | Decisions (executor choice, review policy) in gated mode |
| Model gateways and providers | Usage, version metadata, deprecation notices | None |
| Billing and FinOps | Cost lines, vendor invoices | None |
| QA and judge tools | Case-level scores | Calibration feedback (aggregate) |
| Process-intelligence tools | Graph and log exports | Economic annotations, ranked leaks |
| Finance and auditors | Measurement-plan approvals, queries | Statements, evidence packs, replay |
| Identity provider | Users, groups | None |
| Transparency service and timestamp authority | Receipts, anchors | Signed statements, hashes |
| Assurance partners and insurers (CPA firms, certification bodies, underwriters) | Engagement and control-framework questions | Shared statements, control mappings, offline verifier |
| CI/CD systems and evaluation tools (GitHub Actions, GitLab CI, Langfuse, LangSmith, Braintrust, Kitaru, open-source gates) | Datasets, traces, regression results | Signed promotion verdicts, gate status |
| Cloud and suite marketplaces (Salesforce AgentExchange, ServiceNow Store, Microsoft marketplace, helpdesk marketplaces) | Listings, procurement, co-sell referrals | Offers, usage reports |

## 3.2 Technical context

| Interface | Direction | Protocol and format | Notes |
|---|---|---|---|
| Telemetry ingest | In | OTLP with GenAI conventions; vendor APIs | Version-pinned adapters [S6] |
| Process logs | In | OCEL 2.0 JSON or SQLite, CSV, database extracts | Preferred import and export format [V tooling support] |
| Helpdesk and CRM | In, later out | REST, webhooks, database readers | Read-only through Phase 1 |
| Vendor billing and resolution exports | In | CSV, API, file drops | Needed for the billing audit |
| Deprecation feeds | In | RSS, provider APIs, manual entry | Poller is outbound-only |
| MCP server and client | Both | MCP | OMC exposes ledger queries, precedent retrieval and decision requests; reads tools as client (ADR-013, Proposed) |
| A2A observer | In | A2A | Cross-organization agent traces [S25] |
| Decision API | Out | Synchronous request and response; asynchronous advisory | Customer systems act as enforcement points |
| Billing | In | Cloud and provider usage exports (FOCUS where available) | Joined to cases by tags |
| Identity | In | OIDC, SAML, SCIM | Role mapping |
| Evidence registration | Out | SCITT: COSE_Sign1 signed statements, COSE receipts [S28]; RFC 3161 anchoring as fallback | Self-hosted or third-party transparency service |
| CI promotion gate and import adapters | Both | GitHub Actions or GitLab CI step and CLI returning a signed verdict; importers for Langfuse, LangSmith, Braintrust, Kitaru and similar exports | ADR-028 |
| Partner and verifier interface | Out | Public verifier CLI, schema and test vectors; read-only partner API for statements the customer shares | Open source (ADR-025) |
| Reporting | Out | PDF and Markdown packs, Parquet, OCEL, signed statements | Customer-owned |

## 3.3 Scope

**In scope:** discovery, unit economics, risk calibration, certified model qualification, outcome billing audit, action authority audit, vendor bake-off, contract evidence (Proposed), human access and disclosure audit, replay privacy gate, CI promotion gate, executor allocation, causal measurement, evidence.

**Out of scope:** building or hosting agents; replacing process-mining platforms; model training; general observability; employee performance management or per-agent QA scoring; autonomous action on regulated decisions without assigned human oversight; selling AI agents or models; issuing certificates or attestations (partners do that); legal advice; building general-purpose evaluation runners or replay tooling (OMC imports their output).
