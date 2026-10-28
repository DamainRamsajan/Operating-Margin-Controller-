# Operating-Margin Controller (OMC)

OMC is a closed-loop system that raises and proves the financial value of work shared between people, AI models and agents.
For repeatable, high-volume workflows it **senses** how work really runs, **prices** the risk of each step, **decides** which executor handles each case inside a declared risk budget, and **proves** the causal P&L effect with evidence the customer can re-run.

Status: design phase (no code yet). Working codename: OMC.

**Entry products:** certified model migration qualification (with a CI promotion gate), outcome billing audit with vendor bake-off, and action authority audit, plus a human-access and disclosure compliance module. First workflow family: customer-support ticket resolution.

## Quickstart (Codespaces or local)

```bash
pip install -e ".[dev,spike]" && python scripts/make_vectors.py && pytest -q && python scripts/demo.py
```

See `docs/dev/CODESPACES.md` for the upload steps, `docs/dev/DATA-REQUEST.md` for the data we need next, `docs/dev/MILESTONE-M0.md` for what is built, and `docs/dev/LIMITATIONS.md` before relying on any result.

## Repository map

| Path | Content |
|---|---|
| `docs/arc42/` | Architecture documentation (arc42), v0.2 |
| `docs/adr/` | Architecture decision records (statuses in `docs/arc42/09-architecture-decisions.md`) |
| `docs/research/` | Research dossiers by round and the research queue |
| `docs/dev/`, `docs/spec/` | Developer guides, validation results, the Evidence Statement spec |
| `src/omc/`, `src/omc_verify/` | Engine (statistics, audit, vault, privacy) and the standalone verifier |
| `tests/`, `vectors/`, `scripts/` | Tests, public verifier test vectors, demo and vector generator |
| `CHANGELOG.md` | What changed and when |

## Conventions

- Research claims carry source tags `[S#]` (Appendix C); `[V]` marks vendor or secondary sources to verify before external use.
- Every product number carries an evidence grade E0 to E3 (arc42 section 4.4).
- Decisions are ADRs. Independence charter: no fees contingent on findings, no sale of agents or models.
