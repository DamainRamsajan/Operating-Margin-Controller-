"""Replay Privacy Gate v1 (FR27, ADR-029, arc42 5.11): redaction, measured residual leakage,
provider data-use checks. Redaction here is rule-based and deliberately simple; leakage is
MEASURED on a reviewed sample and bounded, never assumed zero."""
from __future__ import annotations

import re

from scipy.stats import beta

_EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_IBAN = re.compile(r"\b[A-Z]{2}\d{2}(?:[ ]?[A-Z0-9]{4}){2,7}(?:[ ]?[A-Z0-9]{1,4})?\b")
_SSN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
_IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
_CARD = re.compile(r"\b(?:\d[ -]?){12,18}\d\b")
_PHONE = re.compile(r"(?<!\d)(?:\+?\d{1,3}[ -]?)?(?:\(\d{2,4}\)[ -]?|\d{2,4}[ -])\d{3,4}[ -]?\d{3,4}(?!\d)")


def _luhn(digits: str) -> bool:
    total, alt = 0, False
    for ch in reversed(digits):
        n = int(ch)
        if alt:
            n *= 2
            n -= 9 if n > 9 else 0
        total += n
        alt = not alt
    return total % 10 == 0


def redact(text: str) -> tuple[str, dict[str, int]]:
    counts = {"email": 0, "iban": 0, "ssn": 0, "ipv4": 0, "card": 0, "phone": 0}

    def sub(rx, tag, key, check=None):
        nonlocal text
        def repl(m):
            if check and not check(m.group(0)):
                return m.group(0)
            counts[key] += 1
            return f"[{tag}]"
        text = rx.sub(repl, text)

    sub(_EMAIL, "EMAIL", "email")
    sub(_IBAN, "IBAN", "iban")
    sub(_SSN, "SSN", "ssn")
    sub(_CARD, "CARD", "card", check=lambda s: 13 <= len(re.sub(r"\D", "", s)) <= 19 and _luhn(re.sub(r"\D", "", s)))
    sub(_IPV4, "IP", "ipv4", check=lambda s: all(0 <= int(p) <= 255 for p in s.split(".")))
    sub(_PHONE, "PHONE", "phone")
    return text, counts


def leakage_upper_bound(n_reviewed: int, n_leaks: int, alpha: float = 0.05) -> float:
    """One-sided Clopper-Pearson upper bound on the per-case residual leakage rate."""
    if n_reviewed <= 0:
        return 1.0
    if n_leaks >= n_reviewed:
        return 1.0
    return float(beta.ppf(1 - alpha, n_leaks + 1, n_reviewed - n_leaks))


def leakage_audit(n_reviewed: int, n_leaks: int, limit: float, alpha: float = 0.05) -> dict:
    ub = leakage_upper_bound(n_reviewed, n_leaks, alpha)
    return {"n_reviewed": n_reviewed, "n_leaks": n_leaks, "observed_rate": (n_leaks / n_reviewed) if n_reviewed else None,
            "upper_bound": ub, "limit": limit, "alpha": alpha, "decision": "release" if ub <= limit else "block"}


def check_provider_terms(terms: dict, policy: dict) -> list[str]:
    """Return the list of policy failures (empty means the provider passes)."""
    fails = []
    if terms.get("trains_on_data", True) and not policy.get("allow_training", False):
        fails.append("provider may train on submitted data")
    if terms.get("retention_days", 10**6) > policy.get("max_retention_days", 0):
        fails.append("retention exceeds policy")
    allowed = policy.get("allowed_regions")
    if allowed and terms.get("region") not in allowed:
        fails.append("region not allowed")
    return fails
