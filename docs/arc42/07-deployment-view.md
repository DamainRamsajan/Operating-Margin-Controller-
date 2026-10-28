# 7. Deployment view

## 7.1 Infrastructure level 1

```
CUSTOMER TENANT (VPC or on-premises cluster)
  [Connectors] [Ingest] [Event Store: object storage + metadata DB]
  [Policy Service (stateless, replicated)] [Migration Gate and Outcome Audit jobs]
  [Estimator Runner (sandboxed, no egress)]
  [Evidence Vault: immutable storage + signing service + HSM or KMS] -> [Transparency service client]
  [Console Agent]
          ^                                   | outbound-only, metadata and aggregates
          | enforcement-point calls             v
HOSTED CONTROL PLANE (multi-region)
  [Estimator Registry] [Model and Price Catalog] [Deprecation Feeds] [Console API] [Update Service] [Benchmarks (opt-in)]
```

| Block | Node | Notes |
|---|---|---|
| BB1 to BB3 | Ingest workers, object storage, metadata database | Scale with event volume; columnar files for analytics |
| BB4 to BB8, BB15, BB18 | Batch and stream jobs | Scheduled; isolated from the decision path |
| BB9, BB10 | Policy Service replicas | Stateless; cached policy tables; failover returns baseline |
| BB11 | Estimator Runner | Sandboxed, pinned digests, no network egress |
| BB12 | Vault services | Immutable storage; keys in HSM or KMS; transparency service self-hosted or third-party |
| BB13, BB14 | Console agent, identity bridge | SSO through the customer provider |
| CP1 to CP6 | Hosted control plane | No raw case data; outbound-only tunnel from the tenant |

**Trust boundaries.** Raw case data stays inside the tenant. The control plane receives metadata and aggregates only, and customers can disable even that. Enforcement points hold their own credentials and can revoke OMC authority independently.

**Planning sizes (A4).** 5 million decisions per day is about 58 per second on average, with peaks perhaps ten times higher. At 2 to 4 KB per record that is roughly 10 to 20 GB per day before compression. Shadow scoring doubles inference spend on audited traffic; audits sample and stop early (anytime-valid), so qualification cost is bounded by the audit design.

## 7.2 Variants

- **Pilot kit:** single-node bundle for Phase 0, installable in a customer tenant in a day, read-only, with the Migration Gate and a deprecation-feed poller.
- **Production:** replicated policy service; separate estimator runners.
- **Air-gapped:** control-plane functions replaced by signed offline update bundles; registry mirrored; self-hosted transparency service.
