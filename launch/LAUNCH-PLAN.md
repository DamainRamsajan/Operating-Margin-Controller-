# Launch plan (from 28 October 2026)

Definition of launch used here: **L1 private alpha** (1 to 2 design partners running real data), **L2 public beta** (open verifier, docs, pricing, first paid pilot), **L3 general availability** (security attestation, three references, marketplace listing). Dates are targets, not promises.

## Week 0 (28 Oct to 3 Nov): protect and prepare. About 30 minutes of your time in total

| # | Action | Who | Why |
|---|---|---|---|
| 0.1 | **Make the main repo private** (GitHub: repo Settings, General, Danger Zone, Change visibility). It currently holds the strategy, competitive analysis and engine | You, 2 min | Competitors can read a public repo. Codespaces works the same on private repos |
| 0.2 | Create an empty **public** repo `omc-verify` on GitHub, then push `omc-verify-public.zip` (instructions in the chat message) | You, 10 min | Public credibility asset; Apache-2.0; only the verifier and the format spec |
| 0.3 | Connect the **Gmail** and **Google Calendar** connectors in Claude (Connectors directory) | You, 5 min | I can then draft outreach into your Drafts and propose meeting slots. I never send without your approval |
| 0.4 | Create a free **Common Paper** account | You, 5 min | Standard Design Partner, Pilot, DPA and Cloud Service agreements with e-signature |
| 0.5 | Pick the contact email for the website and run `sed -i 's/CONTACT_EMAIL/you@yourdomain.com/g' site/index.html` | You, 2 min | The site has a placeholder |
| 0.6 | Confirm where Intellica AI, Inc. is incorporated and whether it can receive USD (bank, Wise Business) | You, 5 min | Decides the invoicing route for the first paid pilot |
| 0.7 | Deploy `site/` (instructions in `launch/AUTOMATION.md`) | You, 10 min | A page to point people to |
| 0.8 | Build the target list (40 organizations, with role and signal) | Me, next round | Uses public information only |

## Weeks 1 to 2 (4 to 17 Nov): pipeline
- I draft 40 personalized emails into your Gmail Drafts; you review and send about 5 a day (hand-reviewed, plain text, one ask, unsubscribe line).
- I draft three LinkedIn posts (methodology note, chatbot-law explainer, model-retirement explainer); you post.
- Publish `omc-verify` 0.1.0 to PyPI (one-time PyPI setup, then a git tag triggers the release).
- **Gate A (30 Nov):** at least 10 conversations and at least 2 verbal design-partner commitments. If not, change the segment or the message before sending more.

## Weeks 3 to 8 (18 Nov to 31 Dec): design partners and data
- Discovery calls with the script in `DESIGN-PARTNER-PLAYBOOK.md`; sign the Common Paper Design Partner Agreement with 1 to 2 partners.
- Get dataset A from a partner (or run Path 1 in `docs/dev/DATA-REQUEST.md` yourself).
- Engineering (me): milestone M1 in this order: outcome billing audit estimator, human-access deterministic checks, pilot kit as a container, Review Workbench MVP, SCITT and post-quantum spike.
- **Gate B (31 Dec):** one real dataset audited, with a signed verdict and a written methodology note. If no partner data, publish the public-data and LLM-pair results as the note and use it as outreach content.

## January to February 2027: private alpha (L1)
- Run 30-day pilots (`PILOT-OFFER.md`). Chatbot-law rule sets entered by counsel; compliance pilots start after California AB 1609 applies (1 January) and the Spanish deadline (28 December) [V].
- First paid pilot under the Common Paper Pilot Agreement.
- Decide on SOC 2 Type I readiness (not researched in detail yet; verify cost and timeline).
- **Gate C (28 Feb):** at least one paid pilot or a signed letter of intent. If not, lead with the other entry product (see kill rules below).

## March to April 2027: public beta (L2)
Open verifier 1.0, documentation site, pricing page, first marketplace listing matched to a partner's helpdesk, a published case study with the partner's permission.

## L3 general availability
After a security attestation decision, three references and a counsel-reviewed contract set. Target Q3 2027 (assumption).

## Metrics (weekly, run `python scripts/pipeline_report.py launch/pipeline.csv`)
Emails sent, reply rate, calls held, qualified partners, pilots started, days from signature to first verdict, labels spent per verdict, number of statements verified by third parties.

## Kill and pivot rules
- By 31 Jan: fewer than 5 percent replies after 100 targeted contacts, or no discovery calls: change the ICP (try BPOs and AI-support implementation consultancies) before any more engineering.
- By 28 Feb: no pilot: lead with the compliance audit (deadline-driven) or the billing audit, whichever the calls favored.
- If a partner's data shows the audit needs far more labels than planned: publish the finding, shrink claims, and focus on the equivalence and billing products.
