# Post-COVID breathlessness: 7T resting-state fMRI connectivity analysis

This repository contains the analysis code for a 7T resting-state functional MRI
study of breathlessness in post-COVID patients (N = 53, two sites). It tests
whether resting-state functional connectivity between 18 regions of interest is
associated with self-reported breathlessness, using robust linear regression with
edge-wise multiple comparison correction.

Individual-level data are held under controlled access and are not included here;
the code runs against a locally supplied data file in the documented format.

## Repository structure

```
.
├── config.py                 Single place for data paths and analysis constants
├── run_all.py                Main pipeline: all edges, all participants, both outcomes
├── requirements.txt          Pinned dependencies
├── src/
│   ├── data_io.py            Load and align the two input tables
│   ├── preprocessing.py      Z-scoring and cube-root transforms
│   ├── robust_regression.py  Core RLM fit and the 153-edge screen
│   ├── multiple_comparison.py Benjamini-Hochberg FDR
│   ├── moderation.py         Interaction models with permutation inference
│   ├── sensitivity.py        Alternative covariate specifications
│   └── visualisation.py      Coefficient heatmap and predicted-outcome scatter
├── data/
│   ├── README.md             Data dictionary (expected columns and units)
│   ├── subject_data_template.csv        Header only, no data
│   └── connectivity_edges_template.csv  Header only, no data
├── source_data/             Edge-level figure source data (aggregate, no individuals)
│   ├── README.md            Column dictionary
│   ├── Figure1_source_data1.csv  BCS coefficient heatmap
│   └── Figure2_source_data1.csv  D-12 coefficient heatmap
├── rois/README.md            Region-of-interest provenance and recreation
├── results/                  Outputs (git-ignored)
├── LICENSE                   MIT (code); Glasser-atlas terms noted
└── CITATION.cff
```

## Analysis specification

- Univariate robust linear regression (statsmodels RLM, Huber's T, c = 1.345).
- Two outcomes modelled separately: Breathlessness Catastrophising Scale (BCS)
  and Dyspnoea-12 (D-12), each z-scored before fitting.
- Predictor: one connectivity edge at a time, in native Pearson correlation units.
- Covariates: age, sex, BMI, mean absolute and relative framewise displacement,
  cube-root-transformed total intracranial volume and total brain volume.
- Benjamini-Hochberg FDR across the 153 edges, within each outcome.
- Bootstrap and permutation analyses use 5000 iterations, seed 42.

## How to run

1. Install dependencies (a virtual environment is recommended):
   ```
   pip install -r requirements.txt
   ```
2. Format your data as in `data/README.md` and `data/*_template.csv`.
3. Edit the two data paths in `config.py`.
4. From the repository root:
   ```
   python run_all.py
   ```
   This fits every edge for both outcomes, applies FDR, and writes edge-level
   results (`results/edgewise_BCS.csv`, `results/edgewise_D12.csv`) and the
   coefficient heatmaps. No individual-level values are written.

## Figure source data

`source_data/` holds the edge-level statistics underlying the coefficient
heatmaps (`Figure1_source_data1.csv` for BCS, `Figure2_source_data1.csv` for
D-12). These are aggregate values only, one row per edge, and match the output
of `run_all.py` (rounded for presentation). They let the figures be reproduced
without the restricted individual-level data. See `source_data/README.md` for
the column dictionary.

## Expected input

Two locally supplied tables joined on `participant_id`: a subject table (one row
per participant, native variable values) and a connectivity table (one row per
participant, 153 edge columns in native Pearson units). Full column definitions
are in `data/README.md`; the header-only templates in `data/` give the exact
layout.

## Software

Reference interpreter Python 3.11.6; pinned library versions in
`requirements.txt`. The reported results were reproduced with the versions listed
there.

## Data availability

Individual-level data (connectivity matrices, questionnaire scores and
demographics) are restricted NHS patient data and are available under controlled
access only, as described in the data availability statement of the paper. They
must never be added to this repository.

## Regions of interest

The 18 regions are not shared as image files; several are defined on native
anatomy and are subject-specific. They can be recreated from the seed
coordinates and definitions in the paper. See `rois/README.md`.

## How to cite

Please cite the associated paper and this software (see `CITATION.cff`), which
lists the authors and the repository URL.

## Licence

Code is released under the MIT Licence (`LICENSE`). The posterior insula regions
PoI1 and PoI2 derive from the Glasser et al. (2016) atlas, which carries the
Human Connectome Project Open Access Data Use Terms; any mask recreated from them
remains subject to those terms.
