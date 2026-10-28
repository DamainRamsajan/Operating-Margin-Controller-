"""Create public test vectors for the verifier. The key below is a TEST KEY ONLY and is not secret."""
import json
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from omc.vault import chain
from omc.vault.statement import dec, sign_statement

root = Path(__file__).resolve().parents[1] / "vectors"
root.mkdir(exist_ok=True)
priv = Ed25519PrivateKey.from_private_bytes(bytes(range(32)))      # fixed, public, TEST ONLY
other = Ed25519PrivateKey.from_private_bytes(bytes(range(1, 33)))
(root / "test-key.pub.pem").write_bytes(priv.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))
(root / "test-key-other.pub.pem").write_bytes(other.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))
payload = {"schema": "omc.evidence.v0", "type": "model-promotion-verdict", "verdict": "promote", "tier": "tier0",
           "tolerance": dec(0.01), "alpha": dec(0.05), "n_cases": 12000, "n_disagree": 36, "n_labeled": 0,
           "grade": "E3", "issued_at": "2026-10-27T00:00:00Z"}
good = sign_statement(payload, priv, "omc-test", "vector:good")
(root / "valid.cose").write_bytes(good)
bad = bytearray(good); bad[-70] ^= 1                                  # flip a bit inside the signed content
(root / "tampered.cose").write_bytes(bytes(bad))
(root / "wrong-key-signed.cose").write_bytes(sign_statement(payload, other, "omc-test", "vector:wrong-key"))
chain_path = root / "chain-valid.jsonl"
chain_path.unlink(missing_ok=True)
for i in range(3):
    chain.append(chain_path, sign_statement({**payload, "n_cases": 12000 + i}, priv, "omc-test", f"vector:{i}"))
lines = chain_path.read_text().splitlines()
(root / "chain-broken.jsonl").write_text("\n".join([lines[0], lines[2]]) + "\n")
(root / "EXPECTED.json").write_text(json.dumps({
    "valid.cose": {"pubkey": "test-key.pub.pem", "valid": True},
    "tampered.cose": {"pubkey": "test-key.pub.pem", "valid": False},
    "wrong-key-signed.cose": {"pubkey": "test-key.pub.pem", "valid": False},
    "chain-valid.jsonl": {"pubkey": "test-key.pub.pem", "valid": True},
    "chain-broken.jsonl": {"pubkey": "test-key.pub.pem", "valid": False}}, indent=2))
print("vectors written to", root)
