"""
Robust linear regression: the single model used throughout the paper.

Each model regresses a z-scored breathlessness outcome on one connectivity edge
(native Pearson units) plus the standardised base covariates, using a robust
M-estimator (Huber's T). This module provides the atomic fit and the edge-wise
screen across all 153 edges.
"""
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm

import config
from src.preprocessing import prepare_outcome, prepare_covariates


def fit_edge(y, edge_values, covariates):
    """
    Fit one robust model: y ~ const + edge + covariates.

    Parameters
    ----------
    y : array-like, z-scored outcome.
    edge_values : array-like, one edge in native Pearson units (the predictor).
    covariates : DataFrame of standardised covariates.

    Returns a dict with the edge term: beta, se, z (Wald = beta/se), p (two-sided
    normal), 95% CI, and the sample size actually used (complete cases).
    """
    design = pd.DataFrame({"edge": np.asarray(edge_values, float)})
    design = pd.concat([design, covariates.reset_index(drop=True)], axis=1)
    design.insert(0, "const", 1.0)
    frame = design.copy()
    frame["_y"] = np.asarray(y, float)
    frame = frame.dropna()
    n = len(frame)

    X = frame.drop(columns="_y").to_numpy()
    yy = frame["_y"].to_numpy()
    fit = sm.RLM(yy, X, M=sm.robust.norms.HuberT(t=config.HUBER_C)).fit()

    beta = float(fit.params[1])          # index 0 = const, index 1 = edge
    se   = float(fit.bse[1])
    z    = float(fit.tvalues[1])         # Wald statistic beta/se
    p    = 2.0 * stats.norm.sf(abs(z))
    return dict(beta=beta, se=se, z=z, p=p,
                ci_lower=beta - 1.96 * se, ci_upper=beta + 1.96 * se, n=n)


def edgewise_screen(subjects, connectivity, outcome):
    """
    Fit the model for every edge and return a tidy DataFrame (one row per edge).
    FDR is applied separately (see src.multiple_comparison).
    """
    y = prepare_outcome(subjects, outcome)
    cov = prepare_covariates(subjects)
    rows = []
    for edge in connectivity.columns:
        roi_1, roi_2 = edge.split("_", 1)
        res = fit_edge(y, connectivity[edge].to_numpy(), cov)
        rows.append({"edge_id": edge, "roi_1": roi_1, "roi_2": roi_2, **res})
    cols = ["edge_id", "roi_1", "roi_2", "beta", "se",
            "ci_lower", "ci_upper", "z", "p", "n"]
    return pd.DataFrame(rows)[cols]
