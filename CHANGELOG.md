# Changelog

## 2026-11-05, Production readiness program (arc42 v0.6)
- Direction change: production-grade, pilot-ready; no local, MVP or prototype work. Program, Gate P definition, workstreams and sequence in `docs/production/`; 91-item checklist and `scripts/readiness_report.py`.
- Code: Signer abstraction with ES256 (KMS-compatible) and Ed25519, verifier with algorithm-confusion protection, vectors for both; console hardening (CSP nonces and headers, health and readiness, shared-secret proxy authentication, roles, hash-chained audit log, structured logs, refusal to serve unauthenticated on non-local addresses); `omc audit-verify`.
- Supply chain and operations: hash-pinned locks, CycloneDX SBOM, bandit and pip-audit in CI (0 findings, no known vulnerabilities at last run), Dockerfile, compose reference, release and weekly security workflows, Dependabot, CODEOWNERS, SECURITY.md.
- Docs: threat model v0, vulnerability handling and CRA runbook draft, deployment guide, runbook skeleton, ADR-040 to ADR-045.
- Tests: 73 fast, 4 slow. Container build, IdP, KMS and real-infrastructure checks are not run here and are tracked in the checklist.

## 2026-11-03, Milestone M1: console
- D13 to D15 approved; ADR-033 accepted; ADR-039 added.
- Read-only console (`omc console`): Home, Verdict, Evidence with live signature and chain checks, Setup, Review queue with blinded decisions and CSRF-protected label writes; `omc demo-workspace`; gate now writes `trajectory.json` and `review_queue.csv`.
- 8 console tests (pages, signature tamper detection, path safety, review flow); total 51 fast tests, 4 slow.

## 2026-10-29, Round 12 (arc42 v0.5)
- arc42 v0.5: UX merged; competitor gap matrix and two-year distance plan; consolidation and method-spread added to threats; exit paths in Appendix E.9.
- Code: mixture confidence sequence for the disagreement rate, business-metric parity audit, stationarity warning in every verdict. 43 fast tests, 4 slow.
- ADR-036 to ADR-038; Round 12 dossier; refreshed validation and public-data results.

## 2026-10-29, Usability kit
- `docs/ux/usability/`: study README, recruiting guide, 45-minute session script with six tasks, comprehension-test design (three phrasings, Latin square), SUS, consent template, CSV templates.
- `ui/usability/comprehension.html` (self-running test with counterbalancing and scoring) and `scripts/usability_report.py` (SUS, Wilson intervals, paired exact tests, issues). 37 fast tests.

## 2026-10-29, UX
- UX research and design spec (`docs/ux/`), clickable prototype (`ui/prototype/`, rebuilt by `scripts/build_prototype.py`), proposed amendments for arc42 v0.5, ADR-033 to ADR-035.
- Code: plain-language verdict rendering (`omc/render.py`), `omc gate --markdown` and `verdict.md`, composite GitHub Action for sticky PR comments, `trajectory()` for evidence charts. 33 fast tests.

## 2026-10-28, Launch pack
- `launch/`: launch plan with gates and kill rules, design-partner playbook, pilot offer, security pack draft, contracts guide, automation guide, pipeline template; `scripts/pipeline_report.py`.
- `site/index.html`: landing page (placeholder CONTACT_EMAIL to be set).
- Public verifier repo prepared separately (omc-verify, Apache-2.0).

## 2026-10-28, Milestone M0b
- S-a-lite: certified audit on 13,083 real public support queries (Banking77); no false certificates, equivalent and improved candidates certified, regression rejected (`docs/dev/S-A-LITE-RESULTS.md`).
- `omc check-data`, `omc pseudonymize`, data templates, `docs/dev/DATA-REQUEST.md`, and an untested real-LLM pair script.
- 29 fast tests.

## 2026-10-28, Milestone M0 (code)
- Python package `omc` and standalone verifier `omc_verify`; certified paired audit with Tier 0 and Tier 1, CI promotion gate, signed statements and hash chain, exposure inventory, leak report, Replay Privacy Gate v1.
- 25 fast tests and 3 statistical simulations; planted-ground-truth validation in `docs/dev/M0-VALIDATION.md`.
- Codespaces dev container, CI workflow, ADR-031 and ADR-032.

## 2026-10-27, Round 11
- arc42 v0.4: human access and disclosure compliance module, interoperability with developer tools (import adapters, CI promotion gate), Replay Privacy Gate, channel strategy, valuation reality check.
- ADR-022 to ADR-026 accepted (D7); ADR-027 to ADR-030 added as Proposed. FR25 to FR27, BB21 and BB22, R16 to R18, Q22 to Q25, risks R31 to R36, spikes S-j to S-l.
- Round 11 research dossier and extended research queue.

## 2026-10-26, Round 10
- arc42 v0.3: third entry product (action authority audit), assurance-ecosystem alignment, public verifier, Review Workbench, packaging and pricing principles; Appendix E (business model, hypotheses).
- ADR-022 to ADR-026 added (all Proposed). FR21 to FR24, BB19 and BB20, R13 to R15, Q18 to Q21, risks R26 to R30.
- Round 10 research dossier and extended research queue.

## 2026-10-23, Round 9
- arc42 v0.2 merged and split by section under `docs/arc42/`; replaces the v0.1 draft and the Round 8 amendment file.
- ADR-001 to ADR-021 written as files. Accepted: 011, 015, 016, 017. Proposed: the rest.
- Beachhead decided: customer-support ticket resolution (ADR-017).
- New entry product: outcome billing audit and vendor bake-off (ADR-020).
- Evidence Statements become SCITT signed statements (ADR-018).
- Certified disagreement-supported audits and action-level disagreement (ADR-019, ADR-021).
- Round 9 research dossier and updated research queue.

## 2026-10-23, Round 8
- Research dossier (academic map, competitive scan, threat model). See `docs/research/round-08-research-dossier.md`.

## 2026-10-23, Round 7
- arc42 v0.1 drafted.
