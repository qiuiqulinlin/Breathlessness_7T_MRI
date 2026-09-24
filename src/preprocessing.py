"""
Preprocessing: standardisation of outcomes and covariates.

Continuous variables are z-scored. The two volume covariates are cube-root
transformed before z-scoring, following the Methods. The connectivity predictor
is never transformed here; it enters the models in native Pearson units.
"""
import numpy as np
import pandas as pd

import config


def zscore(x: pd.Series) -> pd.Series:
    """Z-score a numeric series (population SD; ddof=0), ignoring NaN."""
    x = pd.to_numeric(x, errors="coerce")
    return (x - x.mean()) / x.std(ddof=0)


def prepare_outcome(subjects: pd.DataFrame, outcome: str) -> np.ndarray:
    """Return the z-scored outcome vector for 'BCS' or 'D12'."""
    return zscore(subjects[outcome]).to_numpy()


def prepare_covariates(subjects: pd.DataFrame) -> pd.DataFrame:
    """
    Build the standardised covariate design (without the connectivity term).
    Volumes are cube-root transformed then z-scored; other continuous
    covariates are z-scored; binary covariates are left unscaled.
    """
    out = pd.DataFrame(index=subjects.index)
    for col in config.COVARIATES:
        if col in config.BINARY_COVARIATES:
            out[col] = pd.to_numeric(subjects[col], errors="coerce")
        elif col in config.CUBEROOT_COVARIATES:
            out[col] = zscore(np.cbrt(pd.to_numeric(subjects[col], errors="coerce")))
        else:
            out[col] = zscore(subjects[col])
    return out
