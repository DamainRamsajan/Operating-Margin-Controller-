"""Append-only hash chain of signed statements (arc42 BB12, tamper evidence).
Each entry: {"seq", "prev", "cose" (base64), "hash"} with hash = SHA-256(prev_bytes || cose_bytes)."""
from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path

GENESIS = "00" * 32


def _hash(prev_hex: str, cose: bytes) -> str:
    return hashlib.sha256(bytes.fromhex(prev_hex) + cose).hexdigest()


def read_entries(path) -> list[dict]:
    p = Path(path)
    if not p.exists():
        return []
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]


def append(path, cose: bytes) -> dict:
    entries = read_entries(path)
    prev = entries[-1]["hash"] if entries else GENESIS
    entry = {"seq": len(entries), "prev": prev, "cose": base64.b64encode(cose).decode(),
             "hash": _hash(prev, cose)}
    with open(path, "a") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")
    return entry


def verify_chain(path) -> tuple[bool, str]:
    prev = GENESIS
    for i, e in enumerate(read_entries(path)):
        cose = base64.b64decode(e["cose"])
        if e["seq"] != i or e["prev"] != prev or e["hash"] != _hash(prev, cose):
            return False, f"chain broken at seq {i}"
        prev = e["hash"]
    return True, "ok"
