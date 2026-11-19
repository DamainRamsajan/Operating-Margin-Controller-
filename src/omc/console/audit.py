"""Tamper-evident administrative audit log (ADR-043). Hash-chained JSON lines: each entry commits to the
previous one, so removing or editing an entry is detectable. It records who did what, never case content.
Export it and ship it to the customer's log platform; anchor the head hash externally for stronger evidence."""
from __future__ import annotations

import hashlib
import json
import threading
from datetime import UTC, datetime
from pathlib import Path

GENESIS = "00" * 32


def _digest(prev: str, entry: dict) -> str:
    body = json.dumps(entry, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(bytes.fromhex(prev) + body.encode("utf-8")).hexdigest()


class AuditLog:
    def __init__(self, path):
        self.path = Path(path)
        self._lock = threading.Lock()

    def entries(self) -> list[dict]:
        if not self.path.exists():
            return []
        return [json.loads(line) for line in self.path.read_text().splitlines() if line.strip()]

    def append(self, user: str, role: str, action: str, target: str = "", outcome: str = "ok") -> dict:
        with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            entries = self.entries()
            prev = entries[-1]["hash"] if entries else GENESIS
            entry = {"seq": len(entries), "ts": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"), "user": user,
                     "role": role, "action": action, "target": target, "outcome": outcome, "prev": prev}
            entry["hash"] = _digest(prev, {k: v for k, v in entry.items() if k != "hash"})
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, sort_keys=True) + "\n")
            return entry

    def verify(self) -> tuple[bool, str]:
        return verify_file(self.path)


def verify_file(path) -> tuple[bool, str]:
    prev = GENESIS
    p = Path(path)
    if not p.exists():
        return True, "empty"
    for i, line in enumerate(x for x in p.read_text().splitlines() if x.strip()):
        e = json.loads(line)
        body = {k: v for k, v in e.items() if k != "hash"}
        if e.get("seq") != i or e.get("prev") != prev or e.get("hash") != _digest(prev, body):
            return False, f"audit log broken at seq {i}"
        prev = e["hash"]
    return True, "ok"
