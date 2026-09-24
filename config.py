"""
Central configuration for the post-COVID breathlessness functional connectivity
analysis. Edit the data paths below to point at your local copy of the restricted
individual-level data. Everything else in the pipeline reads from this file, so
paths appear in one place only.

Individual-level data are held under controlled access (see the data availability
statement in the paper) and are NOT included in this repository. The two files
referenced here must be supplied locally in the format described in data/README.md.
"""
from pathlib import Path

# ---------------------------------------------------------------------------
# Data paths (PLACEHOLDERS -- edit to your local restricted-data location)
# ---------------------------------------------------------------------------
SUBJECT_DATA   = Path("/PATH/TO/subject_data.csv")          # see data/subject_data_template.csv
CONNECTIVITY   = Path("/PATH/TO/connectivity_edges.csv")    # see data/connectivity_edges_template.csv

# Output directory (created if absent; git-ignored)
RESULTS_DIR    = Path(__file__).resolve().parent / "results"

# ---------------------------------------------------------------------------
# Analysis specification (matches the Methods)
# ---------------------------------------------------------------------------
# Outcomes, modelled separately and z-scored before fitting.
OUTCOMES = {"BCS": "BCS", "D12": "D12"}

# Base covariates. Continuous covariates are z-scored; the two volumes are
# cube-root transformed and then z-scored. The connectivity predictor is left
# in native Pearson correlation units.
COVARIATES          = ["age_years", "sex", "BMI",
                       "mean_FD_absolute", "mean_FD_relative",
                       "total_brain_volume", "total_intracranial_volume"]
CUBEROOT_COVARIATES = ["total_brain_volume", "total_intracranial_volume"]
BINARY_COVARIATES   = ["sex"]  # left unscaled

# Robust regression (statsmodels RLM, Huber's T)
HUBER_C = 1.345

# Multiple comparison
FDR_METHOD = "fdr_bh"   # Benjamini-Hochberg
ALPHA      = 0.05

# Resampling
SEED   = 42
N_BOOT = 5000
N_PERM = 5000

# The 18 regions of interest, ordered by system (subcortical, ACC, insula,
# cortical). See rois/README.md for provenance and recreation details.
ROI_ORDER = ["vlPAG", "dPAG", "piri", "Hyp", "BLA", "sgACC", "pACC", "dACC",
             "mvaIns", "lvaIns", "dmIns", "PoI1", "PoI2", "dpIns",
             "dmPFC", "vmPFC", "S1", "M1"]
