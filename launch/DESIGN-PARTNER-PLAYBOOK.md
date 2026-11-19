# Design-partner playbook

## Who to target
| Tier | Who | Buyer roles | Why |
|---|---|---|---|
| 1 | Companies with 100,000 or more support tickets a year that already run AI-handled support (Intercom Fin, Zendesk AI, Salesforce Agentforce, Decagon, Sierra or an in-house LLM) | Head of Support Operations, Director of CX Operations, AI or automation lead in support, VP Support | They feel model-retirement, vendor-billing and chatbot-law pain first |
| 2 | BPOs and CX outsourcers running AI for clients | Delivery and quality leaders | Many clients, repeatable audits |
| 3 | AI-support implementation consultancies, CPA firms and auditors | Partners, AI assurance leads | Channel (see arc42 ADR-022) |

**Intent signals (public information only):** job posts for AI support operations or AI agent management; a public case study of an AI support rollout; operating in California above $500M revenue (AB 1609 applies from 1 January 2027) or serving Spain (Law 10/2025) [V]; a vendor change announced.

**Search strings** (LinkedIn jobs or Google): `"AI support operations"`, `"AI agent management" support`, `"Fin" Intercom "support operations"`, `Agentforce "service cloud" "support operations"`, `"conversation designer" OR "AI agent QA" customer support`.

## Outreach rules (2026 mailbox rules and law)
- Hand-reviewed, plain text, 25 to 100 words, one clear ask. No bulk sending tools.
- At most 20 emails a day from your own domain at this scale. If you ever need more than about 50 a day, use a separate sending domain and warm it for weeks.
- SPF, DKIM and DMARC must pass on your domain; include an unsubscribe line and honor opt-outs within two days; keep complaints under 0.3 percent [V].
- Business email addresses from public sources only. For EU recipients rely on documented legitimate interest and an easy objection route [V].
- Sequence: day 0 email, day 4 LinkedIn note, day 9 follow-up with the one-pager, day 16 closing note. Then stop.

## Drafts (plain prose; edit the bracketed parts)
**Email A: model retirement.**
Subject: proving a replacement model is no worse
Hi [Name], I saw [specific signal, for example that [Company] runs AI support on [vendor]]. When a model version is retired, how do you show your team that the replacement is not worse on your own tickets, without labeling thousands of them? I am building a read-only tool that returns a signed pass, hold or reject verdict, usually with a small number of labels, and I am looking for two support teams to test it on a 30-day export with no message text. Worth a 20-minute call? If not relevant, tell me and I will not write again.

**Email B: chatbot-law evidence.**
Subject: evidence for the new human-access rules
Hi [Name], California AB 1609 applies from 1 January and Spain's law is already in force [V]. Both turn disclosure and time to a human into things a regulator can ask you to show. I am building a read-only measurement that reports those rates with confidence intervals and signed evidence, from timestamps you already have. Would a 20-minute call be useful? If not, say so and I will stop.

**Email C: billing audit.**
Subject: are billed resolutions real resolutions
Hi [Name], most AI support vendors bill per resolution and define the word themselves. I am testing an independent audit that estimates your true accepted-resolution rate from a small labeled sample and compares it with the billed count, under both the vendor's definition and yours. Could I show you the method on a 20-minute call?

**LinkedIn note (under 300 characters).** Hi [Name], I work on proving AI support changes are safe and on measuring chatbot-law compliance. Would be glad to compare notes on [specific topic].

**Follow-up (day 9).** Hi [Name], one line on what I sent: a way to prove a model or vendor change is no worse, with signed evidence your auditors can verify. The one-page summary is attached. Would a short call help, or should I leave it?

## Discovery call: ten questions
1. How many AI-handled conversations a month, on which tool?
2. Which model versions are in use, and when did the last change happen?
3. How did you check that the last change was not worse?
4. What happens when a provider announces a retirement?
5. Is billing per resolution, and how does the vendor define resolution?
6. Do you measure how often customers who ask for a human reach one, and how fast?
7. Which actions can the AI take with money (refunds, credits), and how are limits checked?
8. Who owns the budget for a problem like this?
9. What would you need from security and legal to share a pseudonymized export?
10. If this worked, what would it replace or save?

**Scorecard (0 to 2 each, qualify at 10 or more of 14):** volume; AI in production; a model or vendor change within six months; outcome-based billing; regulatory exposure; authority to share data; a champion with budget.

## Pilot flow (30 days)
Week 1: agree scope, sign the agreement, receive the pseudonymized export. Week 2: data check, exposure report, first audit run. Week 3: labels from the partner's experts through the Review Workbench (when built) or a spreadsheet; verdict. Week 4: readout, signed statement, feedback, decision on a paid follow-on.

## Objections
- *We will build it ourselves:* the value is independence and a method that auditors accept without trusting you; the verifier is open source.
- *Security:* read-only, pseudonymized ids, no message text, runs in your environment; see `SECURITY-PACK.md`.
- *We do not have labels:* the method labels only a sample of disagreements.
- *Vendor will not allow shadow scoring:* start with exports and replay on your own models.
