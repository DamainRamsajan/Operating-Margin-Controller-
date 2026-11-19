# S-a-lite: audit on real public support text

**What this is.** The certified paired audit (with the mixture bound for the disagreement rate, ADR-036) run on Banking77 (PolyAI): 13,083 real banking customer-support queries with gold intent labels. Two model versions are trained here (classical text classifiers) with 5-fold out-of-fold predictions, so every case is predicted by models that never saw it. The full set is the population and each audit run draws a random permutation (sampling without replacement), so the true change in error rate is known exactly. 200 runs per row, alpha 0.05, label rate 0.5, bounds checked every 50 cases. Reproduce with `python scripts/real_data_spike.py` (about a minute).

**What this is not.** It is not a test on LLM support agents, on live tickets, or on traffic with drift. It checks the statistical machinery on real text and real disagreement patterns. The regressed candidate is deliberately degraded. "Labels requested" counts disagreements selected for labeling before the verdict; a zero-label (tier 0) certificate does not need them.

### near-equivalent (C 0.5 -> 0.6)

Candidate accuracy 0.8919 vs incumbent 0.8902; disagreement rate 0.0055; **true change in error rate -0.0017**.

| Tolerance | Certified | Rejected | Median cases to verdict | Median labels requested |
|---|---|---|---|---|
| 0.01 | 100.0% | 0.0% | 5800.0 | 15.0 |
| 0.02 | 100.0% | 0.0% | 850.0 | 2.0 |
| 0.03 | 100.0% | 0.0% | 450.0 | 1.0 |

### improved (word + char n-grams)

Candidate accuracy 0.9118 vs incumbent 0.8902; disagreement rate 0.0564; **true change in error rate -0.0216**.

| Tolerance | Certified | Rejected | Median cases to verdict | Median labels requested |
|---|---|---|---|---|
| 0.01 | 100.0% | 0.0% | 3300.0 | 93.0 |
| 0.02 | 100.0% | 0.0% | 2075.0 | 58.0 |
| 0.03 | 100.0% | 0.0% | 1450.0 | 39.0 |

### regressed (2000 unigrams, 30% of training data)

Candidate accuracy 0.8289 vs incumbent 0.8902; disagreement rate 0.1357; **true change in error rate +0.0614**.

| Tolerance | Certified | Rejected | Median cases to verdict | Median labels requested |
|---|---|---|---|---|
| 0.01 | 0.0% | 100.0% |  |  |
| 0.02 | 0.0% | 100.0% |  |  |
| 0.03 | 0.0% | 88.5% |  |  |

## Reading the results
- **No false certificates.** The regressed candidate (true error up by 6.1 points) was never certified at any tolerance. It was rejected in every run at tolerances 0.01 and 0.02 and in 88.5 percent of runs at 0.03; the remaining runs stayed on hold within the available cases.
- **A truly equivalent candidate** (error change -0.17 points) was certified in every run at all three tolerances, after a median of 5,800 cases at tolerance 0.01, 850 at 0.02 and 450 at 0.03.
- **An improved candidate** was certified in every run, needing a median of 3,300 cases and 93 labeled disagreements at tolerance 0.01.
- **Change from the earlier union-bound version:** the equivalent candidate went from 90 percent certified at tolerance 0.01 to 100 percent, and rejection of the regression at tolerance 0.03 went from 66.5 to 88.5 percent.

## Caveats
Sampling without replacement from a finite population is slightly more favorable than a live i.i.d. stream. The intents are a single-label classification task, the setting the theory covers best. LLM agents, multi-step actions and shifting traffic still need the real-data spike with a design partner or the LLM script (`scripts/llm_pair_spike.py`, untested here).
