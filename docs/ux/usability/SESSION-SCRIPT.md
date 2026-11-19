# Moderated session script (45 minutes)

Setup: share the prototype (`ui/prototype/index.html` opened in a browser, or the hosted copy). Ask the participant to share their screen and think aloud. One moderator, one note-taker if possible. Record only with consent.

## Timing
| Minutes | Part |
|---|---|
| 0 to 5 | Welcome, consent, "we are testing the tool, not you" |
| 5 to 10 | Background questions |
| 10 to 35 | Tasks with think-aloud |
| 35 to 40 | Comprehension test (`ui/usability/comprehension.html`) |
| 40 to 45 | SUS questionnaire and debrief |

## Welcome (say this)
"Thank you. I am testing a prototype, not you. There are no wrong answers and you cannot break anything. Everything on screen is demo data. Please think aloud: say what you expect, what you are looking at and what confuses you. I may stay quiet when you ask a question, because I want to see what you would do on your own. You can stop at any time."

## Background (record in participants.csv)
Role, team size, AI support tool in use, who decides on model or vendor changes, what happened the last time the model or vendor changed.

## Tasks
Give only the scenario text. Do not hint. Start the clock when they begin; stop when they say they are done or give up. Mark "assisted" if you had to help.

| ID | Persona focus | Scenario to read aloud | Screen | Success means |
|---|---|---|---|---|
| T1 | Support ops, finance | "You have five minutes before a meeting. What needs your attention this week, and why?" | Home | Names the model retiring in 49 days (acme/llm-small) as critical and says the next step is to qualify a replacement |
| T2 | Support ops, finance, auditor | "Open the borderline result. Explain it to a colleague and say what would settle it." | Verdict (borderline) | Says there is not enough evidence yet, that it is neither safe nor unsafe, and that more traffic is needed |
| T3 | Support ops, finance, developer | "Open the clear-regression result. Would you switch to the new model? Why?" | Verdict (regression) | Says no, and says it is worse than the tolerance (about 10 or more per 1,000) |
| T4 | Reviewer, support ops | "Label three cases." | Review queue | Completes three labels unaided and can say that the model names are hidden and why |
| T5 | Auditor, finance | "Your auditor wants proof of this verdict. What would you do?" | Evidence | Finds the verify command and the share option; says the check works offline |
| T6 | Developer | "Read this pull-request comment. Can you merge?" | CI comment | Says no for reject or hold, and gives the reason |

Assign tasks by persona (T1 to T3 for support ops; T1, T3, T5 for finance; T4 and T2 for reviewers; T5 and T2 for auditors; T6 and T3 for developers).

## Probes (use sparingly, after the task)
- "What did you expect to see?" "What was unclear?" "What would you do next?"
- "How much do you trust this result? What would raise your trust?"
- "Which words or numbers did you not understand?"
- If silent: "What are you thinking?"

## Observation grid (note-taker)
For each task record: success (1, 0.5 or 0), time in seconds, errors, whether assisted, quotes, hesitations, misreads (for example reading a range as exact), workarounds. Rate each issue found: 1 cosmetic, 2 minor, 3 major, 4 blocks the task.

## Debrief
"What was the most useful part? The most confusing? If you could change one thing, what would it be? Would you use this? What would your boss or finance team need to see?"

## After the session (10 minutes)
Fill the CSV templates; copy the comprehension results code; write the top three observations while fresh.
