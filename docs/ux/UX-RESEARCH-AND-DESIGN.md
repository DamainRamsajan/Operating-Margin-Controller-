# UX research and design: how people use OMC

Date: 29 October 2026. Companion to the clickable prototype (`ui/prototype/index.html`, built by `scripts/build_prototype.py`). Claims marked [V] rest on vendor, blog or secondary sources.

## 1. What the research says, in short

1. **Experiment platforms already solved "how to show a sequential result", and the lessons transfer.** They pair an interval with a decision rule and a sense of how much more data is needed, and they warn that always-valid methods trade power for the freedom to look early [V]. OMC's verdicts are exactly this kind of object, so the display should show the interval, the tolerance line and an "evidence progress" indicator, not a bare p-value.
2. **Error bars are widely misread, even by experts.** Visualization research finds people read intervals as exact, mistake the shape, and do better with frequency framing ("out of 1,000") and with quantile dot plots or icon arrays than with bars [S43]. Design consequence: lead with a plain sentence, use per-1,000 counts everywhere, always show the denominator, and keep exact bounds one level down.
3. **Review queues work when each screen is one small decision.** Annotation guidance converges on atomic comparisons, blinded A/B order to avoid anchoring, keyboard shortcuts, an overlap sample to measure agreement, and short sessions to limit fatigue [V]. Showing a model's confidence to the reviewer risks anchoring them, so we do not.
4. **Evaluation in code review has become a pull-request comment plus a required status check**, not a separate dashboard; several tools show Wilson intervals and paired tests there, and six platforms ship GitHub integrations [V]. Developers will judge OMC by that comment, so it must read like a verdict, not a log.
5. **Compliance dashboards win on automation and an auditor view, and lose on "checkbox" feel.** Users praise automated evidence collection and auditor portals; they complain about tests that cannot be customized and about re-uploading evidence when an auditor flags something [V]. Design consequence: customer-defined definitions and rules as data, versioned evidence with supersession, and a read-only auditor view.
6. **Suites ship ROI views.** Competitors show cost and ROI charts; none was reported to show a signed, offline-verifiable verdict with an evidence grade. Our interface differentiator is verdict, grade and one-step verification.

## 2. Who uses it and what they need

| Persona | How often | Job to be done | Must see | Must never see |
|---|---|---|---|---|
| Support operations lead | Daily | Keep AI support safe through model and vendor changes | Retirement calendar, verdicts, label progress, alerts | Per-agent performance |
| AI or IT platform manager (champion) | Weekly | Justify spend and manage change risk | Portfolio of workflows, savings, risk, setup state | Raw message text |
| Finance controller | Monthly | Trust the numbers and dispute vendor bills | Billing audit, reproducible statements, evidence grade | Unlabeled projections presented as measurements |
| Expert reviewer | Daily, in batches | Label cases quickly and accurately | One case at a time, blinded decisions, own stats | Model identity, other reviewers' scores |
| Compliance and legal | Periodic | Show human-access and disclosure compliance, set rules | Rule sets, rates with ranges, evidence packs | Conclusions framed as legal advice |
| Auditor or partner | Episodic | Verify a claim without trusting us | Read-only statements, verifier, version history | Anything not shared with them |
| Developer | Per change | Know if a prompt or model change is safe to merge | The PR comment and status check | Dashboards they have to leave the PR to read |
| Admin and security | Setup | Connect data safely | Connectors, permissions, audit log | Credentials in clear |

## 3. Core journeys

| Journey | Steps | Moment of truth |
|---|---|---|
| J1 First value | Connect read-only, data readiness check, exposure report | First retirement calendar within a week |
| J2 Retirement notice | Alert, qualify replacement, review labels, verdict, canary, promote | A signed verdict before the retirement date |
| J3 CI gate | Change opened, comment posted, status check, merge or fix | Developer understands the verdict in under 10 seconds |
| J4 Label sprint | Open batch, label with keys, break, see progress to verdict | Reviewer sees their effort move the verdict |
| J5 Billing dispute | Choose vendor and period, see billed versus true rate, export pack | Finance can send the pack to the vendor unchanged |
| J6 Compliance pack | Counsel confirms rule set, run measurement, review, export | Counsel sees measurements and ranges, not conclusions |
| J7 Audit replay | Auditor opens a shared statement, verifies, replays | Verification works offline in one command |

## 4. Gap analysis (what is missing today) and the fix

Today: the architecture has one line for the console (BB13) and the product is a CLI with JSON output.

| # | Gap | Priority | Fix |
|---|---|---|---|
| 1 | No verdict language; output was JSON | P0 | Done this round: `omc/render.py`, `verdict.md`, `gate --markdown` |
| 2 | No PR comment or status-check integration | P0 | Done: composite action `.github/actions/omc-gate`, example workflow |
| 3 | No visual for the evidence trajectory | P0 | Done in prototype; implement in the console |
| 4 | No onboarding or data readiness flow | P0 | Setup wizard around `omc check-data`; empty states with next step |
| 5 | No retirement calendar view | P0 | Home screen from the exposure inventory |
| 6 | No review queue | P0 | Review Workbench (spec below) |
| 7 | No evidence page or share flow | P0 | Statement page, verify instructions, versions, read-only link |
| 8 | No alerting design | P1 | Notifications (spec below) |
| 9 | No definitions and rules editor (outcome definitions, authority rules, human-access rule sets) | P1 | Versioned editors with counsel approval |
| 10 | No approvals flow for policy changes | P1 | Approval queue with diff and risk statement |
| 11 | No billing audit, action authority, human-access views | P1 | One screen per module, same verdict pattern |
| 12 | No auditor or partner portal | P1 | Read-only shared view with comments and requests |
| 13 | No evidence supersession (version history) | P1 | Versions with state (current, superseded) |
| 14 | No cost transparency (label budget, shadow-scoring inference) | P1 | Budget meter on every audit |
| 15 | No glossary or "what does this mean" help | P1 | Inline definitions on first use; plain-language tooltips |
| 16 | No role model in the interface | P1 | Persona-based default views and permissions |
| 17 | No accessibility standard | P1 | WCAG 2.2 AA target; never color alone |
| 18 | No empty, loading, error and partial-data states | P1 | State catalogue per screen |
| 19 | No demo mode with sample data | P1 | Built-in sample workspace for evaluation |
| 20 | No executive pack (board or finance summary) | P2 | One-page export per quarter |
| 21 | No trust page | P2 | Public page of verified statements customers choose to publish |
| 22 | No bake-off and actuation consoles | P2 | After read-only products prove value |
| 23 | No feedback channel in product | P2 | Feedback button with context |
| 24 | No localization plan | P2 | Dates, numbers, currency; copy externalized |

## 5. Design principles

1. **Verdict first.** Every analysis opens with promote, hold or reject (or a measured rate) in one plain sentence.
2. **Per 1,000, with a denominator.** Frequencies, not percentages or p-values, in summary views; always say how many cases.
3. **Uncertainty is part of the answer.** Show the range and the tolerance together; never a single bare number.
4. **Grade on every number.** An evidence chip (E0 to E3) next to each figure, with text, not just color.
5. **Say what is missing.** For a hold, state what would settle it (more traffic or N labels) and show progress.
6. **Progressive disclosure.** Summary, analyst and auditor levels over the same data.
7. **Nothing happens without approval.** Read-only by default; changes show a diff and a risk statement.
8. **One command to verify.** Every statement shows the offline verification step.
9. **No individual scoring anywhere.** Reviewers see only their own statistics; managers see aggregates.
10. **Fits where people already work.** PR comments, Slack or Teams, email digests, not only a portal.

## 6. Screen inventory

| Screen | Priority | Purpose and key content |
|---|---|---|
| Home | P0 | Retirement calendar, verdict cards, next actions |
| Verdict | P0 | Decision card, dot grid, evidence trajectory, progress, fields, verify command |
| Review queue | P0 | Blinded atomic comparisons, keyboard, progress to verdict |
| Evidence | P0 | Statement, signer, versions, verify steps, share |
| Setup and data readiness | P0 | Connect, check, fix, sample size and label coverage |
| Alerts and approvals | P1 | Notification center; approval queue |
| Rules and definitions | P1 | Outcome definitions, authority rules, human-access rule sets with versions |
| Billing audit | P1 | Billed versus true outcome rate under vendor and customer definitions |
| Action authority | P1 | Leakage rate and currency with ranges; guardrail suggestions |
| Human access | P1 | Disclosure and time-to-human rates with ranges by channel and jurisdiction |
| Auditor portal | P1 | Read-only shared statements, verification, comments |
| Settings and roles | P1 | Connectors, permissions, audit log |
| Bake-off, control, trust page, executive pack | P2 | Later |

## 7. Specifications

**Verdict phrasing (examples used by `render.py`).** Promote: "No worse than the current model. With 95% confidence the replacement makes at most 7.2 more wrong decisions per 1,000 cases; your tolerance is 10.0." Reject: "Worse than the current model. With 95% confidence at least 10.3 more per 1,000." Hold: "Not enough evidence yet..." plus what is needed.

**Review Workbench.** One case per screen with redacted text; two decisions in random order, model names hidden; options: A correct, B correct, neither (pick the label), cannot tell; keys 1 to 4; batches of about 25 with a break prompt; known-answer checks mixed in; an overlap sample for agreement; no confidence scores; progress tied to labels needed for the verdict; a reviewer sees only their own throughput and agreement; managers see batch-level quality, never per-person rankings.

**CI comment.** One sticky comment updated in place; headline verdict word, plain sentence, small table (change, cases, labels, grade, method), collapsible technical detail, offline verify command. A required status check returns pass for promote and fail for hold or reject (exit codes 0, 10, 20).

**Notifications.** Retirement alerts at 90, 60, 30, 14 and 7 days; verdict state changes; label budget exhausted; regime shift detected; kill switch used. Channels: in-app, email digest, Slack or Teams webhook. Group by workflow and severity; one daily digest by default to avoid alert fatigue.

**States.** Every screen defines empty (what to do next), loading, partial data (what is missing), error (what happened, what to try) and permission-denied states.

**Accessibility.** WCAG 2.2 AA target; color is never the only signal; full keyboard operation; charts have text alternatives; respects reduced-motion and dark mode.

## 8. Technical approach for the UI

Server-rendered pages (FastAPI with Jinja and HTMX) with SVG charts, shipped in the same container as the engine and the pilot kit. Reasons: tenant deployment must be simple, the attack surface small, pages accessible by default, and the prototype already shows the needed charts are plain SVG. A single-page app can come later if interaction demands it. Test with jsdom or Playwright and screenshot comparison (ADR-033).

## 9. How we will test it

Five sessions per persona on the prototype, with tasks: find what needs attention today; explain a hold to a colleague; decide on a reject; label ten cases; verify a statement. Compare three phrasings of the same verdict (per 1,000, percentage, p-value) for comprehension. Targets: system usability score of 80 or more, task success of 90 percent or more, verdict comprehension of 85 percent or more, time to first verdict inside the 10-business-day target, reviewer agreement reported per batch, alert actionability above 70 percent.

## 10. Decisions needed

- **D13.** UI stack: server-rendered first. **Approved 29 October 2026.**
- **D14.** First two personas to design and test: support operations lead and finance controller, then reviewer. **Approved.**
- **D15.** First release is read-only (no actuation console). **Approved.**

## 11. Sources
[S43] Uncertainty visualization and communication: Padilla, Kay and Hullman (2020); arXiv 2011.07586 (uncertainty as transparency); clinical uncertainty visualization studies (PMC10623599); cross-language icon-array study (arXiv 2207.09608). [V] Experiment-platform behavior from vendor documentation and blogs (Statsig, Eppo, Optimizely). [V] Annotation practice from Label Studio and LangSmith guidance. [V] Eval-in-PR practice from tianpan.co, Langfuse and eval-action posts. [V] Compliance-dashboard feedback from review sites on Vanta and Drata.
