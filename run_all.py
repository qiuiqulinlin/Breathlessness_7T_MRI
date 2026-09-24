"""
Main analysis pipeline: run the full edge-wise robust regression across all 153
edges and all participants, for both breathlessness outcomes, apply Benjamini-
Hochberg FDR within each outcome, and produce the coefficient heatmaps.

Usage
-----
1. Edit the data paths in config.py to point at your local restricted-data copy
   (formatted as in data/subject_data_template.csv and
   data/connectivity_edges_template.csv).
2. From the repository root:  python run_all.py

Outputs are written to results/ (git-ignored). No individual-level data are
written; only edge-level summary statistics and figures.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import config
from src import data_io
from src.robust_regression import edgewise_screen
from src.multiple_comparison import apply_fdr
from src.visualisation import coefficient_heatmap


def main():
    results_dir = data_io.ensure_results_dir()
    subjects, connectivity = data_io.load_aligned()
    print(f"Loaded {len(subjects)} participants x {connectivity.shape[1]} edges.")

    for key, outcome in config.OUTCOMES.items():
        table = edgewise_screen(subjects, connectivity, outcome)
        table = apply_fdr(table, p_col="p")
        table = table.rename(columns={"p": "p_uncorrected"})

        csv_path = results_dir / f"edgewise_{key}.csv"
        table.to_csv(csv_path, index=False)

        fig_path = results_dir / f"heatmap_{key}.pdf"
        coefficient_heatmap(table.rename(columns={"p_uncorrected": "p"}),
                            outcome_name=key, savepath=fig_path)

        survivors = table.loc[table["significant_fdr"], "edge_id"].tolist()
        print(f"\n{outcome}: edges surviving FDR (q < {config.ALPHA}): "
              f"{survivors if survivors else 'none'}")
        for e in survivors:
            r = table.loc[table.edge_id == e].iloc[0]
            print(f"   {e}: beta = {r.beta:+.3f}  95% CI "
                  f"[{r.ci_lower:+.3f}, {r.ci_upper:+.3f}]  "
                  f"p = {r.p_uncorrected:.2e}  p_fdr = {r.p_fdr:.4f}")
        print(f"   written: {csv_path.name}, {fig_path.name}")


if __name__ == "__main__":
    main()
