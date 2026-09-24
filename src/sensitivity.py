"""
Covariate sensitivity analysis.

Refit a selected edge model under alternative covariate specifications, to check
that the association is not attributable to cohort structure, clinical
heterogeneity or comorbidity. Each specification adds one covariate to the base
set (or, for the reduced model, drops the volume and BMI terms). Models that add
a covariate with missing values are fit on the available complete cases.
"""
import numpy as np
import pandas as pd

import config
from src.preprocessing import prepare_outcome, prepare_covariates, zscore
from src.robust_regression import fit_edge


def sensitivity_table(subjects, connectivity, edge, outcome, extra_covariates=None):
    """
    Fit the base model and one model per extra covariate, for a single edge.

    extra_covariates : dict {label: column_name} of additional covariates to add
    one at a time (e.g. {"+Site": "site_code", "+WHO severity": "WHO_severity"}).
    Continuous extras are z-scored; binary extras (0/1) are added unscaled.

    Returns a tidy DataFrame: Edge, Model, N, beta, ci_lower, ci_upper, z, p.
    """
    y_full = prepare_outcome(subjects, outcome)
    base_cov = prepare_covariates(subjects)
    edge_vals = connectivity[edge].to_numpy()

    rows = []

    def add(label, res):
        rows.append({"Edge": edge, "Model": label, "N": res["n"],
                     "beta": round(res["beta"], 3),
                     "ci_lower": round(res["ci_lower"], 3),
                     "ci_upper": round(res["ci_upper"], 3),
                     "z": round(res["z"], 3), "p": res["p"]})

    add("Base", fit_edge(y_full, edge_vals, base_cov))

    for label, col in (extra_covariates or {}).items():
        extra = subjects[col]
        uniq = pd.unique(extra.dropna())
        if len(uniq) > 2:
            extra = zscore(extra)
        cov = base_cov.copy()
        cov[col] = np.asarray(extra, float)
        add(label, fit_edge(y_full, edge_vals, cov))

    return pd.DataFrame(rows)
