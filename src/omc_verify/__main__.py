"""Standalone verifier (ADR-025). Deliberately independent of the omc package: it needs only
cbor2 and cryptography so that auditors can inspect and trust a very small code base.

Usage:
  omc-verify statement FILE.cose --pubkey PUB.pem
  omc-verify chain CHAIN.jsonl --pubkey PUB.pem
Exit code 0 when everything verifies, 1 otherwise.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys

import cbor2
from cryptography.hazmat.primitives import serialization

GENESIS = "00" * 32


def _verify(cose: bytes, pub) -> dict:
    obj = cbor2.loads(cose)
    if not isinstance(obj, cbor2.CBORTag) or obj.tag != 18:
        raise ValueError("not a COSE_Sign1 message")
    protected, _u, body, sig = obj.value
    if cbor2.loads(protected).get(1) != -8:
        raise ValueError("unsupported algorithm")
    try:
        pub.verify(sig, cbor2.dumps(["Signature1", protected, b"", body]))
    except Exception as e:
        raise ValueError("signature verification failed") from e
    return json.loads(body.decode("utf-8"))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="omc-verify")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("statement"); s.add_argument("file"); s.add_argument("--pubkey", required=True)
    c = sub.add_parser("chain"); c.add_argument("file"); c.add_argument("--pubkey", required=True)
    a = ap.parse_args(argv)
    pub = serialization.load_pem_public_key(open(a.pubkey, "rb").read())
    if a.cmd == "statement":
        try:
            payload = _verify(open(a.file, "rb").read(), pub)
        except ValueError as e:
            print(json.dumps({"valid": False, "error": str(e)})); return 1
        print(json.dumps({"valid": True, "payload": payload}, indent=2, sort_keys=True)); return 0
    prev = GENESIS
    count = 0
    try:
        for i, line in enumerate(ln for ln in open(a.file) if ln.strip()):
            e = json.loads(line)
            cose = base64.b64decode(e["cose"])
            good = hashlib.sha256(bytes.fromhex(prev) + cose).hexdigest()
            if e["seq"] != i or e["prev"] != prev or e["hash"] != good:
                print(json.dumps({"valid": False, "error": f"chain broken at seq {i}"}))
                return 1
            _verify(cose, pub)
            prev = e["hash"]
            count += 1
    except ValueError as e:
        print(json.dumps({"valid": False, "error": str(e)}))
        return 1
    print(json.dumps({"valid": True, "entries": count}))
    return 0

if __name__ == "__main__":
    sys.exit(main())
