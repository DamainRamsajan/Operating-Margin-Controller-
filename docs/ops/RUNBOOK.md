# Operations runbook (skeleton: each procedure must be rehearsed before it is marked done)

| Procedure | Steps | Status |
|---|---|---|
| Start and stop | Start the container with the secret and volume; stop by sending SIGTERM; confirm `/healthz` | Drafted |
| Health check | `/healthz` (process up), `/readyz` (workspace writable) | Implemented |
| Rotate the proxy secret | Generate a new value, update the proxy and the container together during a short window, verify 401 for the old value | Not rehearsed |
| Rotate the signing key | Create a new KMS key version, publish the new public key, keep the old one for verification, record the change in the audit log | Not written |
| Export and verify the audit log | `GET /audit/download`, then `omc audit-verify FILE` | Implemented |
| Backup and restore | Snapshot the data volume (today) or the database and object storage (planned); restore into a fresh instance and run the verifier on every statement | Not rehearsed |
| Upgrade and rollback | Pull the signed image by digest, start, check health, keep the previous digest for rollback; database migrations are forward-only with a tested downgrade plan | Not written |
| Incident response | Contain (revoke proxy secret, disable the route), preserve logs, assess data exposure, notify per contract and law (see VULNERABILITY-HANDLING.md), post-incident review | Drafted |
| Contacts | Security owner, engineering, counsel, customer contacts | To fill |
