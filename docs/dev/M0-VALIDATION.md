# Validation (planted ground truth, synthetic)

Setup: tolerance epsilon = 0.01, alpha = 0.05, label rate 0.5, bounds checked every 100 cases, 300 runs per row, at most 40,000 cases per run, fixed seeds. Each cell shows **union bound / mixture bound** for the disagreement rate (ADR-036). Reproduce with the slow tests (`pytest -q -m slow`) or the campaign code in `omc/audit/simulate.py`.

| World | True regression | Certified | Rejected | Median cases to certify |
|---|---|---|---|---|
| Equivalent models, 0.4% disagreement | 0.0000 | 100.0% / 100.0% | 0.0% / 0.0% | 9,250 / 3,000 |
| Equivalent models, 2% disagreement | 0.0000 | 100.0% / 100.0% | 0.0% / 0.0% | 20,300 / 15,500 |
| Candidate better, 2% disagreement | -0.0080 | 100.0% / 100.0% | 0.0% / 0.0% | 4,700 / 4,025 |
| Regression 25% above tolerance | 0.0125 | 0.0% / 0.0% | 0.0% / 0.0% |  /  |
| Regression 2x tolerance | 0.0200 | 0.0% / 0.0% | 31.3% / 54.7% |  /  |
| Clear regression (0.033) | 0.0330 | 0.0% / 0.0% | 100.0% / 100.0% |  /  |

## Reading the table
- **No false certificates** with either bound: in both worlds where the true regression exceeds the tolerance, 0 of 300 runs were certified.
- **The mixture bound certifies equivalent models much sooner** when disagreement is rare (median 3,000 cases instead of 9,250) and moderately sooner when it is common (15,500 instead of 20,300).
- **It also flags regressions more often:** a regression of twice the tolerance was flagged in 55 percent of runs instead of 31 percent within 40,000 cases. Borderline regressions can still stay on hold.
- These numbers describe the synthetic worlds above, not real traffic.
