"""
Data input/output.

Loads the restricted individual-level inputs (a subject table and a connectivity
edge table), aligns them by participant, and writes results. Neither input is
distributed with this repository; see data/README.md for the expected format and
data/*_template.csv for the exact column layout.
"""
from pathlib import Path
import pandas as pd

import config


def load_subject_data(path: Path = None) -> pd.DataFrame:
    """Load the subject-level table, indexed by participant_id."""
    path = Path(path or config.SUBJECT_DATA)
    df = pd.read_csv(path)
    if "participant_id" not in df.columns:
        raise ValueError("subject data must contain a 'participant_id' column")
    return df.set_index("participant_id")


def load_connectivity(path: Path = None) -> pd.DataFrame:
    """Load the connectivity table (participants x 153 edges), indexed by participant_id."""
    path = Path(path or config.CONNECTIVITY)
    df = pd.read_csv(path)
    if "participant_id" not in df.columns:
        raise ValueError("connectivity data must contain a 'participant_id' column")
    return df.set_index("participant_id")


def load_aligned(subject_path: Path = None, connectivity_path: Path = None):
    """
    Load both inputs and align on participant_id. Returns (subjects, connectivity)
    with identical, matched row order.
    """
    subjects = load_subject_data(subject_path)
    connectivity = load_connectivity(connectivity_path)
    common = subjects.index.intersection(connectivity.index)
    if len(common) == 0:
        raise ValueError("no overlapping participant_id between the two inputs")
    subjects = subjects.loc[common]
    connectivity = connectivity.loc[common]
    return subjects, connectivity


def edges(connectivity: pd.DataFrame) -> list:
    """The list of edge identifiers (column names of the connectivity table)."""
    return list(connectivity.columns)


def ensure_results_dir() -> Path:
    Path(config.RESULTS_DIR).mkdir(parents=True, exist_ok=True)
    return Path(config.RESULTS_DIR)
