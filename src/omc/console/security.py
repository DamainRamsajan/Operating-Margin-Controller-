"""Security helpers for the console: headers, roles, startup safety, structured logging (ADR-040, ADR-041)."""
from __future__ import annotations

import json
import logging
import secrets
import sys
from datetime import UTC, datetime

ROLE_RANK = {"viewer": 1, "reviewer": 2, "admin": 3}
DEFAULT_GROUP_MAP = {"omc-admins": "admin", "omc-reviewers": "reviewer", "omc-viewers": "viewer"}
LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1"}


def csp(nonce: str) -> str:
    return ("default-src 'none'; "
            f"style-src 'nonce-{nonce}'; style-src-attr 'unsafe-inline'; script-src 'nonce-{nonce}'; "
            "img-src 'self' data:; form-action 'self'; base-uri 'none'; frame-ancestors 'none'")


def security_headers(nonce: str, hsts: bool) -> dict[str, str]:
    h = {"Content-Security-Policy": csp(nonce), "X-Content-Type-Options": "nosniff", "X-Frame-Options": "DENY",
         "Referrer-Policy": "no-referrer", "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
         "Cross-Origin-Opener-Policy": "same-origin", "Cross-Origin-Resource-Policy": "same-origin", "Cache-Control": "no-store"}
    if hsts:
        h["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return h


def required_role(method: str, path: str) -> str:
    if path.startswith("/audit"):
        return "admin"
    if method == "POST":
        return "reviewer"
    return "viewer"


def resolve_role(groups: list[str], group_map: dict[str, str]) -> str | None:
    best = None
    for g in groups:
        r = group_map.get(g.strip())
        if r and (best is None or ROLE_RANK[r] > ROLE_RANK[best]):
            best = r
    return best


def check_bind_safety(host: str, auth_mode: str, allow_insecure: bool = False) -> None:
    """Refuse to serve an unauthenticated console on a non-local address."""
    if auth_mode == "none" and host not in LOCAL_HOSTS and not allow_insecure:
        sys.exit("refusing to serve without authentication on a non-local address; use --auth-mode proxy behind your identity provider")


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        data = {"ts": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ"), "level": record.levelname, "msg": record.getMessage()}
        data.update(getattr(record, "fields", {}))
        return json.dumps(data, separators=(",", ":"))


def get_logger() -> logging.Logger:
    log = logging.getLogger("omc.console")
    if not log.handlers:
        h = logging.StreamHandler()
        h.setFormatter(JsonFormatter())
        log.addHandler(h)
        log.setLevel(logging.INFO)
        log.propagate = False
    return log


def new_nonce() -> str:
    return secrets.token_urlsafe(16)
