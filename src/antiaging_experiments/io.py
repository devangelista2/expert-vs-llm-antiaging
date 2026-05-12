"""Input and output helpers for the analysis pipeline."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .constants import AUTHORSHIP_COLUMN_PREFIX, RATING_PREFIXES


def find_column_by_prefix(columns: list[str], prefix: str) -> str:
    """Return the unique column whose name starts with the requested prefix."""
    matches = [column for column in columns if str(column).startswith(prefix)]
    if not matches:
        raise KeyError(f"No column found with prefix: {prefix!r}")
    if len(matches) > 1:
        raise KeyError(f"Multiple columns found with prefix: {prefix!r}: {matches}")
    return matches[0]


def load_answers(excel_path: str | Path, sheet_name: str) -> tuple[pd.DataFrame, dict[str, str], str]:
    """Load the answer sheet and resolve the rating and authorship columns."""
    path = Path(excel_path)
    df = pd.read_excel(path, sheet_name=sheet_name)

    columns = [str(column) for column in df.columns]
    rating_columns = {
        criterion: find_column_by_prefix(columns, prefix)
        for criterion, prefix in RATING_PREFIXES.items()
    }
    authorship_column = find_column_by_prefix(columns, AUTHORSHIP_COLUMN_PREFIX)
    return df, rating_columns, authorship_column


def ensure_output_dir(output_dir: str | Path) -> Path:
    """Create the output directory if needed and return it as a Path."""
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_table(table: pd.DataFrame, output_dir: Path, stem: str) -> Path:
    """Persist a table as CSV and return the output path."""
    path = output_dir / f"{stem}.csv"
    table.to_csv(path)
    return path
