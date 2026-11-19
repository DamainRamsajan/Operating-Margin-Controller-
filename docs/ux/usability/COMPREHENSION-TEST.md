# Comprehension test: three phrasings of the same verdict

## Question
Do people understand a verdict better when it is phrased as counts per 1,000 cases (A), as percentage points (B), or in statistical notation (C)?

## Design
Within-subject Latin square. Each participant sees three trials, each with a different scenario (benign, regression, borderline) and a different phrasing, so every person gives data on all three phrasings. Assignment and order are balanced by participant code in `comprehension.html`. No charts or dot grids are shown, so the test isolates wording. A later round can test the visual separately.

## Phrasings (numbers come from the real scenario runs)
| Scenario | A: per 1,000 | B: percentage points | C: statistical |
|---|---|---|---|
| Benign (promote) | "No worse than the current model. With 95% confidence the replacement makes at most 7.2 more wrong decisions per 1,000 cases; your tolerance is 10.0." | "With 95% confidence, the replacement's error rate is at most 0.72 percentage points higher than the current model's. Your tolerance is 1.00 percentage point." | "Verdict: promote (tier 0). Upper 95% anytime-valid confidence bound on the risk difference (candidate minus incumbent): 0.0072; tolerance 0.0100. Evidence grade E3." |
| Regression (reject) | "Worse than the current model. With 95% confidence the replacement makes at least 10.3 more wrong decisions per 1,000 cases; your tolerance is 10.0." | "With 95% confidence, the replacement's error rate is at least 1.03 percentage points higher than the current model's. Your tolerance is 1.00 percentage point." | "Verdict: reject (tier 1). Lower 95% anytime-valid confidence bound on the risk difference: 0.0103; tolerance 0.0100. Evidence grade E3." |
| Borderline (hold) | "Not enough evidence yet. The replacement could make up to 11.8 more wrong decisions per 1,000 cases; the evidence must show at most 10.0. More traffic needed." | "The replacement's error rate could be up to 1.18 percentage points higher than the current model's; the evidence must show at most 1.00 percentage point. More traffic needed." | "Verdict: hold. Upper 95% anytime-valid confidence bound on the risk difference: 0.0118; tolerance 0.0100. Evidence grade E1. More traffic needed." |

Each trial also shows the same facts table (cases scored, labels used, evidence grade), so every phrasing has the same denominators.

## Questions and scoring key
| Q | Question | Correct |
|---|---|---|
| Q1 | What does this result tell you to do? (Switch, wait, do not switch) | Benign: switch. Regression: do not switch. Borderline: wait |
| Q2 | How sure is this result? (certain; very likely right with a stated margin; rough guess; not enough evidence yet) | Benign and regression: "very likely right with a stated margin". Borderline: "not enough evidence yet" |
| Q3 | Worst-case numeric: per 1,000 cases, how many more wrong decisions could the new model make (at most for benign and borderline, at least for regression)? | Benign 7.2; regression 10.3; borderline 11.8. Correct if within the larger of 1.5 or 20 percent |
| Q4 | How confident would you be explaining this to a colleague? (1 to 5) | Not scored; compare means |
| Q5 | Borderline only: what would settle it? (more traffic; more human-checked labels; either; nothing) | More traffic |
Also recorded automatically: seconds per trial.

## How to read the results
- Q1 and Q3 accuracy per phrasing with Wilson intervals; paired exact tests for A versus B, A versus C and B versus C on Q1 and Q3 (the report script does this).
- Q4 means per phrasing; seconds per phrasing.
- With fewer than 30 participants treat differences as directional.
