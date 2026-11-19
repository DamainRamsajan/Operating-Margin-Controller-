# Security summary for pilots (draft; have counsel and a security reviewer read it before sending)

## In place
- Runs in the partner's own environment (customer-tenant deployment); no raw data leaves it by default.
- Read-only access to exports only; no connection to production systems in the pilot.
- No free text, names, emails or account numbers required; ids are pseudonymized with a keyed hash the partner controls (`omc pseudonymize`).
- Signed statements and an open-source offline verifier; the partner can verify any result without us.
- Redaction and leakage measurement for any replay set (Replay Privacy Gate v1: rule-based, leakage measured on a reviewed sample).
- No sub-processors in the pilot.

## Not yet in place (say so plainly)
- No SOC 2 or ISO 27001 report. A decision on SOC 2 Type I follows the first two partners (cost and timeline not yet researched).
- No third-party penetration test.
- Signatures are Ed25519 only (not post-quantum); no transparency-service registration yet.
- Statistical methods are our own implementation, tested by simulation and on public data, not yet independently audited.

## Incident contact
[to be filled: name, email, response time]

## Questions we expect and honest answers
- *Where is data processed?* In your environment. We receive only the summary statistics you choose to share.
- *Do you train on our data?* No. The product does not train models.
- *What if the pseudonymization secret leaks?* Rotate it and re-export; ids in earlier shared files then no longer match new ones.
