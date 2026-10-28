import json
from pathlib import Path

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from omc.vault import chain
from omc.vault.statement import canonical_json, dec, sign_statement, verify_statement
from omc_verify.__main__ import main as verify_main

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = {"schema": "omc.evidence.v0", "verdict": "promote", "tolerance": dec(0.01), "n": 10}


def test_roundtrip_and_tamper_detection():
    k = Ed25519PrivateKey.generate()
    cose = sign_statement(PAYLOAD, k, "iss", "sub")
    assert verify_statement(cose, k.public_key()) == PAYLOAD
    bad = bytearray(cose); bad[-70] ^= 1
    with pytest.raises(ValueError):
        verify_statement(bytes(bad), k.public_key())


def test_wrong_key_fails():
    k, other = Ed25519PrivateKey.generate(), Ed25519PrivateKey.generate()
    with pytest.raises(ValueError):
        verify_statement(sign_statement(PAYLOAD, k, "i", "s"), other.public_key())


def test_floats_rejected_and_canonical_json_is_stable():
    with pytest.raises(TypeError):
        canonical_json({"x": 0.1})
    assert canonical_json({"b": 1, "a": "é"}) == canonical_json({"a": "é", "b": 1}) == '{"a":"é","b":1}'.encode()


def test_chain_detects_removal_and_edit(tmp_path):
    k = Ed25519PrivateKey.generate()
    p = tmp_path / "chain.jsonl"
    for i in range(3):
        chain.append(p, sign_statement({**PAYLOAD, "n": i}, k, "i", "s"))
    assert chain.verify_chain(p) == (True, "ok")
    lines = p.read_text().splitlines()
    (tmp_path / "gap.jsonl").write_text("\n".join([lines[0], lines[2]]) + "\n")
    assert chain.verify_chain(tmp_path / "gap.jsonl")[0] is False


def test_published_vectors_match_expectations():
    exp = json.loads((ROOT / "vectors" / "EXPECTED.json").read_text())
    for name, e in exp.items():
        kind = "chain" if name.endswith(".jsonl") else "statement"
        code = verify_main([kind, str(ROOT / "vectors" / name), "--pubkey", str(ROOT / "vectors" / e["pubkey"])])
        assert (code == 0) == e["valid"], name
