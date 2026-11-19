# Usability study kit

Goal: find out whether support leaders, finance controllers, reviewers, auditors and developers can use the verdict, review, evidence and CI screens correctly, and whether our plain-language verdict phrasing is understood better than percentages or statistical notation.

## Two studies, different sample sizes
| Study | Question | People | What the result can and cannot tell you |
|---|---|---|---|
| **Formative sessions** | Where do people get stuck? | 5 per persona (start with support operations lead and finance controller) | Finds most major problems early. Does not give reliable rates |
| **Comprehension test** | Which phrasing is understood best? | At least 12 people for a directional answer; at least 30 for a confirmatory one | With 12 people, 12 of 12 correct only guarantees a true rate of about 76 percent or better (95% Wilson bound); 30 of 30 guarantees about 89 percent. The 85 percent target in Q26 needs 30 or more people |

## Files
| File | Use |
|---|---|
| `RECRUITING.md` | Who to recruit, screener, outreach text, incentives |
| `SESSION-SCRIPT.md` | 45-minute moderated session, tasks, probes, observation grid |
| `COMPREHENSION-TEST.md` | Design, phrasings, questions, scoring key |
| `SUS.md` | The ten-item System Usability Scale and scoring |
| `CONSENT.md` | Consent template (not legal advice) |
| `templates/*.csv` | Where to record results |
| `ui/usability/comprehension.html` | Self-running comprehension test (open in a browser) |
| `scripts/usability_report.py` | Turns the CSVs into a findings report |

## Schedule (three weeks)
Week 1: recruit, run one pilot session with a friendly colleague and fix the script. Week 2: run sessions (about 45 minutes each, up to 3 a day). Week 3: run `python scripts/usability_report.py docs/ux/usability/results`, fix the top issues, update the prototype, re-test the changed screens.

## Decision rules
| Finding | Action |
|---|---|
| Phrasing A (per 1,000) comprehension below 85 percent with 30 or more people | Revise wording or add the dot grid; re-test |
| Phrasing C (statistical) beats A on comprehension for finance or auditors | Offer it as the default for those roles |
| Any task below 90 percent success | Fix the screen before building it |
| SUS below 68 | Redesign; between 68 and 80, iterate; 80 or more, proceed |
| Two or more severity-4 issues | Stop and fix before more sessions |
