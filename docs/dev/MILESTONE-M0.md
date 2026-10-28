# Milestone M0: walking skeleton

Goal: prove the core claim of the entry product end to end on synthetic data, with tests, before touching real customer data.

## Built (maps to arc42)

| Capability | Code | arc42 |
|---|---|---|
| Anytime-valid confidence bounds (KL-based, union bound over n) | `omc/stats/cs.py` | 5.3, ADR-019 |
| Certified paired audit, Tier 0 (zero labels) and Tier 1 (labels on a random subset of disagreements) | `omc/audit/paired.py` | 5.7, 6.9, FR15, ADR-019 |
| Outcome-independent label routing (hash threshold) | `selected_for_label` | TC8, Q17 |
| CI promotion gate with signed verdict and exit codes | `omc/audit/gate.py`, `omc gate` | FR26, 6.18, ADR-028 |
| Evidence Statements as COSE_Sign1 (Ed25519), canonical JSON payload | `omc/vault/statement.py` | 5.5, FR16, ADR-018 |
| Append-only hash chain | `omc/vault/chain.py` | 5.5 |
| Standalone verifier (cbor2 and cryptography only) and public test vectors | `omc_verify/`, `vectors/` | FR24, ADR-025 |
| Model exposure inventory and retirement calendar | `omc/exposure/inventory.py` | FR14, 5.7 |
| Leak report (cost per accepted outcome, wasted cost) | `omc/report/leaks.py` | FR2, FR3 |
| Replay Privacy Gate v1: redaction, leakage bound, provider terms | `omc/privacy/gate.py` | FR27, ADR-029 |
| Synthetic worlds with planted ground truth | `omc/audit/simulate.py`, `omc/sample.py` | 8.8 |

## M0b additions

| Capability | Code |
|---|---|
| S-a-lite: audit on real public support text (Banking77), results in `S-A-LITE-RESULTS.md` | `scripts/real_data_spike.py` |
| Real-LLM pair script for the S-a spike (untested, needs API keys) | `scripts/llm_pair_spike.py` |
| Data readiness check and id pseudonymization | `omc check-data`, `omc pseudonymize`, `docs/dev/DATA-REQUEST.md`, `data/templates/` |

## Not built yet (next backlog, in order)

1. **S-a spike on real LLM decisions or real tickets**: public-text classification is done (S-A-LITE-RESULTS.md); the LLM script or a partner export is next (DATA-REQUEST.md).
2. **Material-difference classifier** for free-text answers (ADR-021, S-b).
3. **SCITT registration and post-quantum signatures** (S-d): the current statements are signed COSE_Sign1 only.
4. **Helpdesk connectors** (S-e): read-only adapters beyond CSV.
5. **Equivalence tests on business metrics** and the **canary controller**.
6. **Outcome billing audit estimator** with prediction-powered inference (S-c).
7. **Human-access and disclosure audit** deterministic timing checks (S-j).
8. **Review Workbench** (S-i).
9. Control plane, console, tenancy: not before the above.

## Definition of done for M0
`pytest -q` and `pytest -q -m slow` pass; `python scripts/demo.py` reproduces the three verdicts; the verifier validates all published vectors; limitations are documented (`LIMITATIONS.md`).
