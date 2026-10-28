# Appendix D. Open items and next steps

## D.1 Decisions

| ID | Decision | Status |
|---|---|---|
| D1 | Migration qualification as Phase 0 entry wedge | Approved |
| D2 | Open Evidence Statement specification | Approved; design-partner review before publication |
| D3 | Independent measurement authority positioning | Approved |
| D4 | Beachhead workflow | Decided by delegation: customer-support ticket resolution (ADR-017) |
| D5 | First design-partner profile | Open: support organization with 100,000 or more tickets a year, an AI vendor or model with a retirement date, read access to billing exports, and exposure to California, Spain or EU chatbot rules |
| D6 | Entry-product pricing | Open: guided by ADR-026; contingent fees excluded by ADR-016 |
| D7 | Third entry product (action authority audit) and ADR-022 to ADR-026 | Approved 26 October 2026 |
| D8 | Open-source licence for the verifier (permissive recommended) | Open |
| D9 | First assurance partner to approach (CPA firm or certifier) | Open |
| D10 | Adopt the human access and disclosure compliance module and ADR-027 to ADR-030 | Open: recommended yes |
| D11 | First marketplace to list on (recommend the one matching the design partner's helpdesk) | Open |
| D12 | Engage compliance counsel for rule sets and statement templates | Open: recommended before the first compliance pilot |

## D.2 Feasibility spikes

| ID | Spike | Question |
|---|---|---|
| S-a | Paired-audit replication on a support workflow | Do disagreement-supported audits work at decision and action level on real tickets? What is the label spend? |
| S-b | Material-difference classifier | Can free-text differences be reduced to action-level disagreement reliably? |
| S-c | Outcome-audit coverage | Do prediction-powered intervals for the true resolution rate cover planted truth under realistic label noise? |
| S-d | SCITT profile prototype | Register and verify a statement; test post-quantum COSE support; check SCRAPI status |
| S-e | Helpdesk export coverage | What do the target helpdesks expose for reopen, recontact, CSAT, actions with amounts, vendor resolution flags, human-request and disclosure events? |
| S-f | Conformal gate under model flips | Do recalibration windows restore coverage after planted model changes? |
| S-g | Action authority audit | How much of authority is machine-checkable? Does the leakage interval cover planted truth? |
| S-h | Control mapping | Which AIUC-1, ISO/IEC 42001 and SOC 2 controls can a statement credibly support? Validate with a certifier |
| S-i | Review Workbench | Do blinded comparisons and time-boxed budgets keep label quality and expert time within targets? |
| S-j | Human-access audit | Which events are available to compute time to a human per channel? Do intervals cover planted truth? Which rules can counsel express as data? |
| S-k | Replay privacy leakage | What residual leakage does the gate achieve on real support transcripts, and what sample size bounds it? |
| S-l | CI gate and import adapters | Can exports from Langfuse, LangSmith, Braintrust and Kitaru be imported without loss? What verdict latency is achievable in CI? |

## D.3 Verification items

- Confirm the Salesforce and Intercom transaction and its effect on Fin's pricing and data access [V].
- Confirm AIUC-1 certification claims for support vendors and the AICPA and AIUC offering's scope [V].
- Counsel review of employment classification (RC2), chatbot-law applicability and thresholds (RC7), and the legal framing of leakage, liability and compliance evidence packs.
- Confirm Digital Omnibus publication and dates on EUR-Lex (RC1) [V].
- Obtain documentation or demos of Celonis Transformation Hub attribution and Make Process Intelligence.
- Check vendor contracts for rights to shadow scoring, exports and audit (R22), and provider data-use terms for replay (TC9).
- Check current marketplace fee schedules and co-sell terms before any pricing assumption [V].

## D.4 Research queue

See `docs/research/research-queue.md`.
