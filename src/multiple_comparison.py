"""
Multiple comparison correction.

Benjamini-Hochberg FDR is applied across the 153 edges within each outcome,
separately for BCS and D-12.
"""
import pandas as pd
from statsmodels.stats.multitest import multipletests

import config


def apply_fdr(results: pd.DataFrame, p_col: str = "p") -> pd.DataFrame:
    """
    Add 'p_fdr' and 'significant_fdr' columns to an edge-wise results table.
    Correction is Benjamini-Hochberg across all rows of the table (i.e. within
    one outcome).
    """
    out = results.copy()
    reject, p_fdr, _, _ = multipletests(out[p_col].to_numpy(),
                                        alpha=config.ALPHA,
                                        method=config.FDR_METHOD)
    out["p_fdr"] = p_fdr
    out["significant_fdr"] = reject
    return out
