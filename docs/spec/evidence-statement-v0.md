# Evidence Statement v0 (draft, ADR-015, ADR-018)

Envelope: COSE_Sign1 (RFC 9052), CBOR tag 18, array `[protected, unprotected, payload, signature]`.

Protected header map:

| Label | Name | Value |
|---|---|---|
| 1 | alg | -8 (EdDSA, Ed25519) |
| 3 | content type | `application/vnd.omc.statement+json` |
| 4 | kid | `omc-ed25519:` plus the first 8 bytes of the public key, hex |
| 15 | CWT claims | `{1: issuer, 2: subject}` |

Signature input: CBOR array `["Signature1", protected, h'', payload]`.

Payload: canonical JSON, UTF-8, keys sorted, no whitespace. **No floating-point numbers**: integers only; fractional values are decimal strings with six places (`"0.009957"`).

Fields for `type = "model-promotion-verdict"`: schema, type, subject {workflow, incumbent, candidate}, verdict (promote, hold, reject), tier (tier0, tier1, none), reason, grade (E0 to E3), tolerance, alpha, n_cases, n_disagree, n_labeled, stopping_index, rho_ub, rho_lb, delta_ub, delta_lb, label_routing {rule, salt, rate}, inputs {incumbent_sha256, candidate_sha256, labels_sha256}, estimator {name, version}, assumptions, issued_at.

Chain: JSON lines `{seq, prev, cose (base64), hash}` with `hash = SHA-256(prev_bytes || cose_bytes)`; genesis prev is 32 zero bytes.

Status: draft. Not yet registered with a SCITT transparency service; no post-quantum signature (spike S-d). Published test vectors are in `vectors/` and signed with a **public test key**.
