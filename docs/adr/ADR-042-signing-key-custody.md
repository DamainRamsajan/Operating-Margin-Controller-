# ADR-042: Signing key custody and algorithm agility

- **Status:** Proposed (signer abstraction and ES256 implemented; KMS adapters pending D16)
- **Context:** Production signing keys must not live in files; major KMS products support ECDSA P-256 widely; post-quantum signatures are coming.
- **Decision:** A Signer interface with Ed25519 for development and ES256 (COSE -7) for production KMS keys; the verifier checks that the algorithm matches the key type; rotation keeps old public keys for verification; hybrid post-quantum signers plug into the same interface.
- **Consequences:** Statements verify identically regardless of custody; KMS adapters need real cloud accounts to test.
