import json
import subprocess
import sys
from pathlib import Path

import pytest
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from omc.vault.signer import ALG_EDDSA, ALG_ES256, Ed25519Signer, P256Signer, as_signer, kid_for
from omc.vault.statement import sign_statement, verify_statement

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = {"schema": "omc.evidence.v0", "verdict": "promote", "n": 1}


def test_es256_roundtrip_and_cose_signature_length():
    k = ec.generate_private_key(ec.SECP256R1())
    cose = sign_statement(PAYLOAD, k, "iss", "sub")
    assert verify_statement(cose, k.public_key()) == PAYLOAD
    assert len(P256Signer(k).sign(b"x")) == 64 and as_signer(k).alg == ALG_ES256


def test_es256_is_deterministic_for_vectors():
    k = ec.generate_private_key(ec.SECP256R1())
    assert sign_statement(PAYLOAD, k, "i", "s") == sign_statement(PAYLOAD, k, "i", "s")


def test_tamper_and_wrong_key_fail_for_both_algorithms():
    for key in (ec.generate_private_key(ec.SECP256R1()), Ed25519PrivateKey.generate()):
        other = Ed25519PrivateKey.generate() if isinstance(key, Ed25519PrivateKey) else ec.generate_private_key(ec.SECP256R1())
        cose = sign_statement(PAYLOAD, key, "i", "s")
        bad = bytearray(cose)
        bad[-70] ^= 1
        with pytest.raises(ValueError):
            verify_statement(bytes(bad), key.public_key())
        with pytest.raises(ValueError):
            verify_statement(cose, other.public_key())


def test_algorithm_confusion_is_rejected():
    ed, es = Ed25519PrivateKey.generate(), ec.generate_private_key(ec.SECP256R1())
    with pytest.raises(ValueError):
        verify_statement(sign_statement(PAYLOAD, ed, "i", "s"), es.public_key())
    with pytest.raises(ValueError):
        verify_statement(sign_statement(PAYLOAD, es, "i", "s"), ed.public_key())


def test_non_p256_curve_is_refused():
    with pytest.raises(ValueError):
        P256Signer(ec.generate_private_key(ec.SECP384R1()))


def test_kid_formats_and_signer_classes():
    ed, es = Ed25519PrivateKey.generate(), ec.generate_private_key(ec.SECP256R1())
    assert kid_for(ed.public_key()).startswith(b"omc-ed25519:") and kid_for(es.public_key()).startswith(b"omc-es256:")
    assert Ed25519Signer(ed).alg == ALG_EDDSA


def test_gate_with_es256_key_end_to_end(tmp_path):
    def run(*a):
        r = subprocess.run([sys.executable, "-m", "omc.cli", *map(str, a)], capture_output=True, text=True, cwd=ROOT)
        return r.returncode, r.stdout
    run("keygen", "--out-dir", tmp_path / "k", "--alg", "es256")
    run("sample", "--out-dir", tmp_path / "d", "--n", 12000)
    d = tmp_path / "d" / "benign"
    code, _ = run("gate", "--incumbent", d / "incumbent.csv", "--candidate", d / "candidate.csv", "--labels", d / "gold.csv",
                  "--key", tmp_path / "k" / "omc-key.pem", "--out-dir", tmp_path / "o")
    assert code == 0
    vcode, vout = run("verify", "statement", tmp_path / "o" / "verdict.cose", "--pubkey", tmp_path / "k" / "omc-key.pub.pem")
    assert vcode == 0 and json.loads(vout)["valid"] is True
