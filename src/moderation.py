"""
Moderation analysis (secondary, exploratory).

For a selected edge, test whether a moderator (for example GAD-7 or ventilation
status) changes the edge-outcome association, using the same robust estimator.
Inference on the interaction term is by non-parametric permutation of the
moderator (n = 5000, seed = 42), because the small sample makes the analytic
robust standard errors unreliable.
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm

import config
from src.preprocessing import prepare_outcome, prepare_covariates, zscore


def _interaction_beta(y, edge, moderator, covariates):
    """Robust interaction coefficient for edge x moderator, adjusting for covariates."""
    df = pd.DataFrame({"edge": np.asarray(edge, float),
                       "mod": np.asarray(moderator, float)})
    df["edge_x_mod"] = df["edge"] * df["mod"]
    df = pd.concat([df, covariates.reset_index(drop=True)], axis=1)
    df.insert(0, "const", 1.0)
    df["_y"] = np.asarray(y, float)
    df = df.dropna()
    fit = sm.RLM(df["_y"].to_numpy(), df.drop(columns="_y").to_numpy(),
                 M=sm.robust.norms.HuberT(t=config.HUBER_C)).fit()
    # columns: const, edge, mod, edge_x_mod, covariates...  -> interaction at index 3
    return float(fit.params[3])


def moderation_test(subjects, connectivity, edge, outcome, moderator_col,
                    binary_moderator=False, n_perm=None, seed=None):
    """
    Returns the observed interaction coefficient and a permutation p-value.
    Continuous moderators are z-scored; binary moderators are used as 0/1.
    """
    n_perm = n_perm or config.N_PERM
    seed = config.SEED if seed is None else seed
    y = prepare_outcome(subjects, outcome)
    cov = prepare_covariates(subjects)
    edge_vals = connectivity[edge].to_numpy()
    mod = subjects[moderator_col].to_numpy().astype(float)
    if not binary_moderator:
        mod = zscore(pd.Series(mod)).to_numpy()

    observed = _interaction_beta(y, edge_vals, mod, cov)
    rng = np.random.default_rng(seed)
    null = np.empty(n_perm)
    for k in range(n_perm):
        null[k] = _interaction_beta(y, edge_vals, rng.permutation(mod), cov)
    p_perm = (np.sum(np.abs(null) >= abs(observed)) + 1) / (n_perm + 1)
    return dict(edge=edge, outcome=outcome, moderator=moderator_col,
                interaction_beta=observed, p_permutation=p_perm, n_perm=n_perm)
