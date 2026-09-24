"""
Visualisation.

coefficient_heatmap: the 18 x 18 edge-coefficient matrix. The upper triangle
shows every coefficient; the lower triangle shows only edges with an uncorrected
p < .05 (other lower-triangle cells are left grey); FDR-significant edges are
outlined and starred.

predicted_outcome_scatter: connectivity against model-predicted outcome for a
single edge, with the fitted slope and 95% confidence band.
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle

import config
from src.preprocessing import prepare_outcome, prepare_covariates
from src.robust_regression import fit_edge

plt.rcParams.update({"font.family": "sans-serif",
                     "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
                     "pdf.fonttype": 42, "svg.fonttype": "none"})

_DISPLAY = {"Hyp": "Hypo", "mvaIns": "mvIns", "lvaIns": "lvIns"}


def _label(roi):
    return _DISPLAY.get(roi, roi)


def coefficient_heatmap(results: pd.DataFrame, outcome_name: str, savepath,
                        order=None, vlim=5.0):
    """
    Draw and save the coefficient heatmap from an edge-wise results table that
    already carries 'p' and 'p_fdr' columns.
    """
    order = order or config.ROI_ORDER
    idx = {r: i for i, r in enumerate(order)}
    n = len(order)
    coef = np.full((n, n), np.nan)
    pval = np.full((n, n), np.nan)
    fdr = np.zeros((n, n), dtype=bool)
    for r in results.itertuples():
        i, j = idx[r.roi_1], idx[r.roi_2]
        coef[i, j] = coef[j, i] = r.beta
        pval[i, j] = pval[j, i] = r.p
        if getattr(r, "significant_fdr", r.p_fdr < config.ALPHA):
            fdr[i, j] = fdr[j, i] = True
    np.fill_diagonal(coef, 0.0)

    cmap = plt.cm.RdBu_r
    norm = mcolors.Normalize(-vlim, vlim)
    grey = (0.60, 0.60, 0.60, 1.0)

    def shown(i, j):
        if i == j:
            return False
        if j > i:
            return True
        return pval[i, j] < config.ALPHA

    rgba = np.ones((n, n, 4))
    for i in range(n):
        for j in range(n):
            if shown(i, j):
                rgba[i, j] = cmap(norm(coef[i, j]))
            elif i > j:
                rgba[i, j] = grey

    fig, ax = plt.subplots(figsize=(11.2, 9.6))
    ax.imshow(rgba, aspect="equal", interpolation="none")
    ax.set_xticks(np.arange(-.5, n, 1), minor=True)
    ax.set_yticks(np.arange(-.5, n, 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.1)
    ax.tick_params(which="minor", length=0)

    def textcolour(rgb):
        return "white" if (0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]) < 0.45 else "#1a1a1a"

    for i in range(n):
        for j in range(n):
            if not shown(i, j):
                continue
            is_fdr = fdr[i, j]
            ax.text(j, i, f"{coef[i, j]:.2f}" + ("*" if is_fdr else ""),
                    ha="center", va="center", fontsize=6.6,
                    color=textcolour(rgba[i, j]),
                    fontweight="bold" if is_fdr else "normal", zorder=3)
            if is_fdr:
                ax.add_patch(Rectangle((j-0.5, i-0.5), 1, 1, fill=False,
                                       edgecolor="black", linewidth=1.8, zorder=4))

    ax.add_patch(Rectangle((-.5, -.5), n, n, fill=False, edgecolor="0.6",
                           linewidth=1.0, zorder=5))
    ax.set_xticks(range(n)); ax.set_xticklabels([_label(r) for r in order], rotation=45, ha="right", fontsize=10)
    ax.set_yticks(range(n)); ax.set_yticklabels([_label(r) for r in order], fontsize=10)
    ax.set_xlabel("Region of interest", fontsize=12, labelpad=8)
    ax.set_ylabel("Region of interest", fontsize=12, labelpad=8)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(length=0)

    sm_cbar = plt.cm.ScalarMappable(cmap=cmap, norm=norm); sm_cbar.set_array([])
    cb = fig.colorbar(sm_cbar, ax=ax, fraction=0.045, pad=0.04, ticks=np.arange(-4, 5, 2))
    cb.set_label(f"Regression coefficient (β), {outcome_name}", fontsize=12)
    cb.ax.tick_params(labelsize=10)

    fig.tight_layout()
    fig.savefig(savepath, bbox_inches="tight", dpi=300)
    plt.close(fig)
    return savepath


def predicted_outcome_scatter(subjects, connectivity, edge, outcome, savepath):
    """Scatter of one edge against model-predicted outcome, with fitted slope + 95% CI."""
    import seaborn as sns
    y = prepare_outcome(subjects, outcome)
    cov = prepare_covariates(subjects)
    x = connectivity[edge].to_numpy()
    res = fit_edge(y, x, cov)  # for the annotation

    # predicted outcome from the full model (edge + covariates)
    import statsmodels.api as sm
    design = pd.concat([pd.Series(x, name="edge"), cov.reset_index(drop=True)], axis=1)
    design.insert(0, "const", 1.0)
    frame = design.copy(); frame["_y"] = y
    frame = frame.dropna()
    fit = sm.RLM(frame["_y"].to_numpy(), frame.drop(columns="_y").to_numpy(),
                 M=sm.robust.norms.HuberT(t=config.HUBER_C)).fit()
    predicted = fit.predict(frame.drop(columns="_y").to_numpy())

    d = pd.DataFrame({"edge": frame["edge"].to_numpy(), "predicted": predicted})
    fig, ax = plt.subplots(figsize=(4.2, 3.6))
    sns.regplot(x="edge", y="predicted", data=d, ax=ax, scatter=False, ci=95,
                line_kws={"color": "0.4", "linewidth": 1.4})
    ax.scatter(d["edge"], d["predicted"], s=45, facecolor="0.15", edgecolor="white", linewidth=0.6)
    ax.set_xlabel(f"{edge.replace('_', '-')} connectivity", fontsize=11)
    ax.set_ylabel(f"Predicted {outcome} (z)", fontsize=11)
    ax.set_title(f"{edge.replace('_', '-')}  (β = {res['beta']:+.2f})", fontsize=11, fontweight="bold")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(savepath, bbox_inches="tight", dpi=300)
    plt.close(fig)
    return savepath
