# Threat model v0 (draft; needs an independent review)

Method: STRIDE per component over the data flows in arc42 sections 3 and 5. Status: **I** implemented and tested, **P** planned, **O** open.

## Trust boundaries
1. Customer identity provider and authenticating proxy (edge) to the OMC console.
2. OMC console to its data (today a file workspace; PostgreSQL and object storage planned).
3. OMC to the signing key (local PEM in development; KMS in production).
4. Customer systems and exports to OMC ingestion (untrusted files).
5. OMC releases to the customer's environment (supply chain).

## Threats and mitigations
| # | Component | Threat | Mitigation | Status |
|---|---|---|---|---|
| T1 | Console | Spoofed identity by forging proxy headers | Shared secret header compared in constant time; startup refuses unauthenticated non-local bind; network policy so only the proxy reaches the console | I (code), P (network policy) |
| T2 | Console | Privilege escalation (viewer to reviewer or admin) | Role resolved from IdP groups; route-level role checks; denied attempts audited | I |
| T3 | Console | Cross-site scripting | Autoescaped templates; CSP with per-request nonces, no inline script without nonce | I |
| T4 | Console | Cross-site request forgery on label writes | Form token checked in constant time; SameSite handled by the proxy | I (token), P (cookie flags at the proxy) |
| T5 | Console | Path traversal and arbitrary file download | Name whitelist; resolved-path check; fixed download whitelist | I |
| T6 | Console | Clickjacking and content sniffing | X-Frame-Options, frame-ancestors, nosniff | I |
| T7 | Evidence | Statement forgery or tampering | COSE signatures; verifier rejects algorithm confusion; hash-chained log | I |
| T8 | Evidence | Signing-key theft | KMS-held keys with rotation; no keys in images or repos; separation of duties | P |
| T9 | Evidence | Back-dated or equivocated statements | Transparency-service registration and trusted timestamps | P |
| T10 | Audit log | Tampering or deletion by an administrator | Hash chain plus export to the customer's log platform; external anchoring of the head hash | I (chain), P (external anchor) |
| T11 | Ingestion | Malicious or oversized files (resource exhaustion, parser bugs) | Size, row and encoding limits; fuzzing; sandboxed async workers | P |
| T12 | Ingestion | Personal data in exports | Pseudonymization tool; no free text accepted; privacy gate for replay sets | I (tools), P (enforced by default) |
| T13 | Labels | Poisoned or colluding reviewers skew verdicts | Overlap sampling, known-answer checks, outcome-independent selection, batch-level quality | P |
| T14 | Statistics | Misuse of results (relying on a stale or shifted audit) | Stationarity warning; assumptions in every statement; no legal conclusions | I |
| T15 | Supply chain | Malicious or vulnerable dependency | Hash-pinned locks, weekly audit, SBOM, minimal dependencies in the verifier | I |
| T16 | Supply chain | Tampered release image | Signed images with provenance; digest pinning | P |
| T17 | Operations | Secrets in logs or configuration | JSON logs exclude query strings and secrets (tested); secrets from environment or a secret manager | I |
| T18 | Operations | Data loss | Backups with tested restore | P |
| T19 | Privacy | Cross-tenant exposure | One deployment per customer for pilots; tenant isolation tests before multi-tenancy | P |
| T20 | Compliance | Unintended worker monitoring | No per-person outputs; reviewer statistics private; schema checks | I (design), P (schema checks everywhere) |

## Top residual risks today
1. No identity-provider verification yet (T1 relies on correct proxy configuration).
2. File-based storage: no encryption at rest, backup or restore (T18).
3. Signing keys are PEM files outside development (T8).
4. No independent review of the statistics or the code (T14).
