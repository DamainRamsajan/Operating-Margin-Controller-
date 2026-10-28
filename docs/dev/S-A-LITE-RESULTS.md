# S-a-lite: audit on real public support text

**What this is.** The certified paired audit run on Banking77 (PolyAI): 13,083 real banking customer-support queries with gold intent labels. Two model versions are trained here (classical text classifiers) with 5-fold out-of-fold predictions, so every case is predicted by models that never saw it. The full set is treated as the population and each audit run draws a random permutation (sampling without replacement), so the true change in error rate is known exactly. 200 runs per row, alpha 0.05, label rate 0.5, at most 13,083 cases, bounds checked every 50 cases. Reproduce with `python scripts/real_data_spike.py` (takes about a minute).

**What this is not.** It is not a test on LLM support agents, on live tickets, or on traffic with drift. It checks the statistical machinery on real text and real disagreement patterns. The regressed candidate is deliberately degraded.

### near-equivalent (C 0.5 -> 0.6)

Candidate accuracy 0.8919 vs incumbent 0.8902; disagreement rate 0.0055; **true change in error rate -0.0017**.

| Tolerance | Certified | Rejected | Median cases to certify | Median labels to certify |
|---|---|---|---|---|
| 0.01 | 90.0% | 0.0% | 10550.0 | 30.0 |
| 0.02 | 100.0% | 0.0% | 2550.0 | 7.0 |
| 0.03 | 100.0% | 0.0% | 1125.0 | 3.0 |

### improved (word + char n-grams)

Candidate accuracy 0.9118 vs incumbent 0.8902; disagreement rate 0.0564; **true change in error rate -0.0216**.

| Tolerance | Certified | Rejected | Median cases to certify | Median labels to certify |
|---|---|---|---|---|
| 0.01 | 100.0% | 0.0% | 3550.0 | 103.0 |
| 0.02 | 100.0% | 0.0% | 2375.0 | 65.5 |
| 0.03 | 100.0% | 0.0% | 1700.0 | 47.0 |

### regressed (2000 unigrams, 30% of training data)

Candidate accuracy 0.8289 vs incumbent 0.8902; disagreement rate 0.1357; **true change in error rate +0.0614**.

| Tolerance | Certified | Rejected | Median cases to certify | Median labels to certify |
|---|---|---|---|---|
| 0.01 | 0.0% | 100.0% |  |  |
| 0.02 | 0.0% | 100.0% |  |  |
| 0.03 | 0.0% | 66.5% |  |  |

## Reading the results
- **No false certificates.** In the regressed case (true error up by 6.1 points) no run was certified at any tolerance, including 0.03, where 33.5 percent of runs stayed on hold within the available cases and the rest were rejected.
- **A truly equivalent candidate** (error change -0.17 points) was certified in 90 percent of runs at tolerance 0.01 and in 100 percent at 0.02 and 0.03. The other 10 percent stayed on hold: the bounds are conservative and 13,083 cases are not always enough at the tightest tolerance.
- **An improved candidate** was certified in every run at every tolerance, using about 47 to 103 labels.
- **Label cost.** At tolerance 0.01 the equivalent candidate needed a median of 30 labels (the guardrail minimum) and the improved candidate about 103, instead of labeling thousands of cases.

## Caveats
Sampling without replacement from a finite population is slightly more favorable than a live i.i.d. stream. The intents are a single-label classification task, the setting the theory covers best. LLM agents, multi-step actions and shifting traffic still need the real-data spike with a design partner or the LLM script (`scripts/llm_pair_spike.py`, untested here).
