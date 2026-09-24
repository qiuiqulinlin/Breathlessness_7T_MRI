# Figure source data

Edge-level source data underlying the connectivity coefficient figures. These are
aggregate statistics only: one row per region-of-interest pair (153 edges), with
no individual-level values. They are the output of `run_all.py` (written locally
as `results/edgewise_BCS.csv` and `results/edgewise_D12.csv`), rounded for
presentation, and are provided here so the figures can be reproduced without
access to the restricted individual-level data.

| File | Outcome | Figure |
|---|---|---|
| `Figure1_source_data1.csv` | Breathlessness Catastrophising Scale (BCS) | Coefficient heatmap, BCS |
| `Figure2_source_data1.csv` | Dyspnoea-12 (D-12) | Coefficient heatmap, D-12 |

## Columns

| Column | Description |
|---|---|
| edge_id | Edge label, `ROIa_ROIb`. |
| roi_1 | First region of the pair. |
| roi_2 | Second region of the pair. |
| beta | Robust regression coefficient for the edge (outcome z-scored, edge in native Pearson units). |
| se | Standard error of the coefficient. |
| ci_lower | Lower bound of the 95% confidence interval. |
| ci_upper | Upper bound of the 95% confidence interval. |
| z | Coefficient divided by its standard error. |
| p_uncorrected | Two-sided p-value, normal approximation. |
| p_fdr | Benjamini-Hochberg FDR-adjusted p-value across the 153 edges, within outcome. |
| n | Number of participants contributing to the fit. |

## Reproduction

Running the public pipeline against the restricted data regenerates these values:

```
python run_all.py
```

For BCS, two edges survive FDR at q < 0.05: dPAG-PoI1 (beta = -4.62) and
BLA-dACC (beta = +4.14). No D-12 edge survives correction.
