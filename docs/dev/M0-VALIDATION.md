# M0 validation (planted ground truth, synthetic)

Setup: tolerance epsilon = 0.01, alpha = 0.05, label rate 0.5, bounds checked every 100 cases, 300 runs per row, at most 40,000 cases per run, seeds fixed in the test code. Reproduce with the snippet in `scripts/` or the slow tests (`pytest -q -m slow`).

| World | True regression | Certified | Rejected | Median cases to certify | Median labels to certify |
|---|---|---|---|---|---|
| Regression 25% above tolerance | 0.0125 | 0.0% | 0.0% |  |  |
| Regression 2x tolerance | 0.0200 | 0.0% | 31.3% |  |  |
| Equivalent models, 0.4% disagreement | 0.0000 | 100.0% | 0.0% | 9250.0 | 17.0 |
| Equivalent models, 2% disagreement | 0.0000 | 100.0% | 0.0% | 20300.0 | 200.5 |
| Candidate better, 2% disagreement | -0.0080 | 100.0% | 0.0% | 4700.0 | 48.0 |
| Clear regression | 0.0330 | 0.0% | 100.0% |  |  |

## Reading the table
- **No false certificates.** In both worlds where the true regression exceeds the tolerance, 0 of 300 runs were certified. The nominal ceiling is 5 percent; the method is conservative.
- **Equivalent models are certified**, in every run here, after about 9,000 cases and 17 labels when the models rarely disagree, and after about 20,000 cases and about 200 labels when they disagree on 2 percent of cases.
- **A better candidate is certified faster** (about 4,700 cases, 48 labels).
- **A clear regression (0.033) is rejected in every run.**
- **Weak spot.** A regression of twice the tolerance was flagged as a regression in only 31 percent of runs within 40,000 cases. The bounds are valid but wide; borderline cases stay on hold. See `LIMITATIONS.md`.

These numbers describe the synthetic worlds above, not real traffic.
