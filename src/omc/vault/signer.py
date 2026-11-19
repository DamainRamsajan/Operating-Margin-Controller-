"""Signing abstraction (ADR-042). Production signers keep keys in a KMS or HSM; local signers are for
development and tests. Every signer exposes the COSE algorithm, a key id and a sign() method, so the
statement format does not change when the key custody does.

Implemented here: Ed25519 (COSE -8) and ECDSA P-256 / ES256 (COSE -7, supported by every major KMS).
Not implemented (interface only): AWS KMS, Azure Key Vault, GCP KMS, HashiCorp Vault adapters, and
post-quantum or hybrid signers. Those need real cloud accounts to test and are tracked in the readiness checklist."""
from __future__ import annotations

import hashlib
from typing import Protocol

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature

ALG_EDDSA = -8
ALG_ES256 = -7


class Signer(Protocol):
    alg: int

    def kid(self) -> bytes: ...
    def sign(self, message: bytes) -> bytes: ...


def spki(pub) -> bytes:
    return pub.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)


def kid_for(pub) -> bytes:
    if isinstance(pub, Ed25519PublicKey):
        raw = pub.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
        return b"omc-ed25519:" + raw[:8].hex().encode()
    return b"omc-es256:" + hashlib.sha256(spki(pub)).digest()[:8].hex().encode()


class Ed25519Signer:
    alg = ALG_EDDSA

    def __init__(self, key: Ed25519PrivateKey):
        self._key = key

    def kid(self) -> bytes:
        return kid_for(self._key.public_key())

    def sign(self, message: bytes) -> bytes:
        return self._key.sign(message)


class P256Signer:
    """ES256: ECDSA over P-256 with SHA-256. COSE requires the signature as raw r || s (64 bytes)."""
    alg = ALG_ES256

    def __init__(self, key: ec.EllipticCurvePrivateKey):
        if not isinstance(key.curve, ec.SECP256R1):
            raise ValueError("ES256 requires a P-256 key")
        self._key = key

    def kid(self) -> bytes:
        return kid_for(self._key.public_key())

    def sign(self, message: bytes) -> bytes:
        try:
            algo = ec.ECDSA(hashes.SHA256(), deterministic_signing=True)   # RFC 6979 where supported
        except TypeError:
            algo = ec.ECDSA(hashes.SHA256())
        r, s = decode_dss_signature(self._key.sign(message, algo))
        return r.to_bytes(32, "big") + s.to_bytes(32, "big")


class KmsSigner:
    """Interface for KMS-backed signers. Subclass for a provider; the private key never leaves the KMS.
    A provider adapter must return a COSE-formatted signature for the algorithm it advertises."""
    alg = ALG_ES256

    def kid(self) -> bytes:                    # pragma: no cover - provider specific
        raise NotImplementedError

    def sign(self, message: bytes) -> bytes:   # pragma: no cover - provider specific
        raise NotImplementedError


def as_signer(obj) -> Signer:
    """Accept a Signer or a raw cryptography private key."""
    if hasattr(obj, "sign") and hasattr(obj, "alg") and not isinstance(obj, (Ed25519PrivateKey, ec.EllipticCurvePrivateKey)):
        return obj
    if isinstance(obj, Ed25519PrivateKey):
        return Ed25519Signer(obj)
    if isinstance(obj, ec.EllipticCurvePrivateKey):
        return P256Signer(obj)
    raise TypeError("unsupported key type")
