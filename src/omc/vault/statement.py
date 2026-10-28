"""Evidence Statements as COSE_Sign1 signed statements (ADR-018, ADR-015, arc42 5.5).

Profile v0 (SCITT-style, RFC 9052 COSE_Sign1, RFC 9597 CWT claims header):
  protected headers: alg (1) = -8 EdDSA, kid (4), content type (3), CWT claims (15) {iss (1), sub (2)}
  payload: canonical JSON (sorted keys, no whitespace, UTF-8). Numbers are integers only; fractional
           values are decimal strings, so canonicalization never depends on float formatting.
Registration in a transparency service and post-quantum signatures are Phase 0 spike S-d.
"""
from __future__ import annotations

import json
from datetime import UTC, datetime

import cbor2
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

CONTENT_TYPE = "application/vnd.omc.statement+json"
ALG_EDDSA = -8
COSE_SIGN1_TAG = 18


def dec(x: float, places: int = 6) -> str:
    """Decimal string for fractional values."""
    return f"{x:.{places}f}"


def _check_no_floats(o):
    if isinstance(o, float):
        raise TypeError("floats are not allowed in statement payloads; use dec() decimal strings")
    if isinstance(o, dict):
        for v in o.values():
            _check_no_floats(v)
    elif isinstance(o, list):
        for v in o:
            _check_no_floats(v)


def canonical_json(obj) -> bytes:
    _check_no_floats(obj)
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_private_key(path) -> Ed25519PrivateKey:
    return serialization.load_pem_private_key(open(path, "rb").read(), password=None)


def load_public_key(path) -> Ed25519PublicKey:
    return serialization.load_pem_public_key(open(path, "rb").read())


def key_id(pub: Ed25519PublicKey) -> bytes:
    raw = pub.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return b"omc-ed25519:" + raw[:8].hex().encode()


def generate_keypair(out_dir, name="omc-key"):
    from pathlib import Path
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    priv = Ed25519PrivateKey.generate()
    (out / f"{name}.pem").write_bytes(priv.private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
    (out / f"{name}.pub.pem").write_bytes(priv.public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))
    return out / f"{name}.pem", out / f"{name}.pub.pem"


def _protected(kid: bytes, issuer: str, subject: str) -> bytes:
    return cbor2.dumps({1: ALG_EDDSA, 4: kid, 3: CONTENT_TYPE, 15: {1: issuer, 2: subject}})


def _sig_structure(protected: bytes, payload: bytes) -> bytes:
    return cbor2.dumps(["Signature1", protected, b"", payload])


def sign_statement(payload: dict, priv: Ed25519PrivateKey, issuer: str, subject: str) -> bytes:
    pub = priv.public_key()
    protected = _protected(key_id(pub), issuer, subject)
    body = canonical_json(payload)
    sig = priv.sign(_sig_structure(protected, body))
    return cbor2.dumps(cbor2.CBORTag(COSE_SIGN1_TAG, [protected, {}, body, sig]))


def verify_statement(cose: bytes, pub: Ed25519PublicKey) -> dict:
    """Return the payload dict if the signature verifies; raise ValueError otherwise."""
    obj = cbor2.loads(cose)
    if not isinstance(obj, cbor2.CBORTag) or obj.tag != COSE_SIGN1_TAG:
        raise ValueError("not a COSE_Sign1 message")
    protected, _unprotected, body, sig = obj.value
    hdr = cbor2.loads(protected)
    if hdr.get(1) != ALG_EDDSA:
        raise ValueError("unsupported algorithm")
    try:
        pub.verify(sig, _sig_structure(protected, body))
    except Exception as e:  # cryptography raises InvalidSignature
        raise ValueError("signature verification failed") from e
    return json.loads(body.decode("utf-8"))
