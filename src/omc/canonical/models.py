"""Canonical records (arc42 5.2 and 5.6). Only fields needed by milestone M0."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelIdentity:
    provider: str
    model: str
    version: str

    def key(self) -> str:
        return f"{self.provider}/{self.model}@{self.version}"


@dataclass(frozen=True)
class DecisionRecord:
    case_ref: str            # pseudonymous case reference, never a person identifier
    ts: str                  # ISO 8601
    workflow_id: str
    model: ModelIdentity
    chosen_option: str = ""
    propensity: float | None = None   # required for gated and canary modes (ADR-002)


@dataclass(frozen=True)
class RetirementNotice:
    model: ModelIdentity
    retirement_date: str     # YYYY-MM-DD
    source: str = ""
