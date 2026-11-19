# ADR-041: Identity and access control

- **Status:** Proposed (extends the implemented proxy mode; pending D17)
- **Context:** Enterprise reviews expect SSO, role-based access and exportable audit logs [V]. The customer already has an identity provider.
- **Decision:** Authenticate at the edge through the customer's IdP (OIDC), with the console trusting only requests that carry a shared secret; map IdP groups to viewer, reviewer and admin; no local passwords in production. Add native OIDC with PKCE, scoped service accounts for the CI gate, and SCIM later.
- **Consequences:** Fast, auditable integration; correctness depends on proxy configuration until native OIDC exists; network policy must restrict the console to the proxy.
