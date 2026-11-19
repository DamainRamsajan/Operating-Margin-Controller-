# Deployment guide (draft)

**Verified here:** unit and integration tests of the application, health endpoints, proxy-mode authentication and roles, headers, audit log. **Not yet verified:** the container build, the compose reference, a real identity provider, TLS, a real cluster. The checklist (WS6) tracks this.

## Shape
Edge: TLS and OIDC login (for example oauth2-proxy or the customer's ingress) injects the shared secret and the user and group headers. The OMC console container accepts only requests carrying that secret, maps groups to roles, serves pages, writes the audit log and statements. Data currently lives in a mounted volume (`/data`); PostgreSQL and object storage replace it in Step 2 of the program.

## Steps
1. Build the image in CI (`docker build -t omc:VERSION .`), scan it, sign it, record the digest.
2. Create the shared secret: `openssl rand -base64 32`. Store it in the customer's secret manager; give the same value to the proxy as the `X-OMC-Proxy-Secret` header.
3. Set `OMC_GROUP_MAP` to map your IdP groups to `viewer`, `reviewer` and `admin`.
4. Run behind TLS. Allow only the proxy to reach port 8000 (network policy or security group).
5. Check: `GET /healthz` and `GET /readyz` return 200; a request without the secret returns 401; a user with no mapped group gets 403.
6. Export `/audit/download` to the log platform; verify with `omc audit-verify`.

## Configuration
| Variable | Meaning |
|---|---|
| `OMC_PROXY_SECRET` | Required in proxy mode; the container refuses to start without it |
| `OMC_GROUP_MAP` | JSON map of IdP groups to roles |
| `OMC_AUTH_MODE` | `proxy` (default in the image) or `none` (development, localhost only) |

## Not yet supported
Native OIDC, SCIM, PostgreSQL, KMS signing, multi-replica operation (the file workspace is single-writer), Helm chart.
