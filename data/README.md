# Expected input data

Individual-level data are held under controlled access and are not distributed
here (see the data availability statement in the paper). This folder contains
only header-only templates that define the expected format. Supply your own two
files locally, matching these layouts, and point `config.py` at them.

The pipeline standardises variables internally: outcomes and continuous
covariates are z-scored, the two volume covariates are cube-root transformed and
then z-scored, and the connectivity predictor is left in native Pearson units.
Provide native (untransformed) values in the tables below.

## 1. `subject_data.csv`  (template: `subject_data_template.csv`)

One row per participant.

| Column | Type | Description |
|---|---|---|
| participant_id | string/int | Unique participant identifier (join key). |
| site | string | Scanning site (for example "Oxford" or "Cardiff"). |
| age_years | numeric | Age at consent, years. |
| sex | 0/1 | Sex (0 = male, 1 = female). |
| BMI | numeric | Body mass index. |
| mean_FD_absolute | numeric | Mean absolute framewise displacement. |
| mean_FD_relative | numeric | Mean relative framewise displacement. |
| total_brain_volume | numeric | Total brain volume (native units; cube-root transformed in the pipeline). |
| total_intracranial_volume | numeric | Total intracranial volume (native units; cube-root transformed in the pipeline). |
| BCS | numeric | Breathlessness Catastrophising Scale total score. |
| D12 | numeric | Dyspnoea-12 total score. |
| GAD7 | numeric | GAD-7 total score (moderation analysis). |
| WHO_severity | numeric | WHO ordinal acute-illness severity score (sensitivity analysis). |
| ventilation | 0/1 | Mechanical ventilation during acute illness (moderation, sensitivity). |
| days_since_infection | numeric | Days from acute infection to scan (sensitivity analysis). |
| hospitalised | 0/1 | Hospitalised during acute illness (sensitivity analysis). |
| respiratory_condition | 0/1 | Pre-existing respiratory condition (sensitivity analysis). |
| cardiac_condition | 0/1 | Pre-existing cardiac condition (sensitivity analysis). |
| spirometry_FEV1_FVC_ratio | numeric | FEV1/FVC ratio, where available (descriptive only). |

## 2. `connectivity_edges.csv`  (template: `connectivity_edges_template.csv`)

One row per participant, one column per region-of-interest pair (edge). Values
are resting-state connectivity in native Pearson correlation units.

| Column | Type | Description |
|---|---|---|
| participant_id | string/int | Join key, matching `subject_data.csv`. |
| <edge columns> | numeric | 153 edges named `ROIa_ROIb` (for example `dPAG_PoI1`), one column per unique pair of the 18 regions. See `connectivity_edges_template.csv` for the full ordered list and `rois/README.md` for the regions. |
