"""End-to-end pipeline orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .grouping import make_groups
from .io import ensure_output_dir, load_answers, write_table
from .plots import plot_all_kappa_heatmaps
from .reliability import summary_inter_rater_agreement, summary_krippendorff_alpha
from .tables import table1_medians, table2_means, table3_attribution, table4_mannwhitney


@dataclass(slots=True)
class AnalysisResult:
    """Structured outputs from one pipeline run."""

    tables: dict[str, pd.DataFrame]
    table_paths: dict[str, Path]
    figure_paths: list[Path]
    output_dir: Path


def run_analysis(
    excel_path: str | Path,
    sheet_name: str,
    output_dir: str | Path,
    show_plots: bool = False,
) -> AnalysisResult:
    """Run the full analysis pipeline and persist all outputs."""
    df, rating_columns, authorship_column = load_answers(excel_path, sheet_name)
    groups = make_groups(df)
    output_path = ensure_output_dir(output_dir)

    tables = {
        "table1_medians": table1_medians(df, rating_columns, groups),
        "table2_means": table2_means(df, rating_columns, groups).round(2),
        "table3_attribution": table3_attribution(df, authorship_column),
        "table4_mannwhitney": table4_mannwhitney(df, rating_columns, groups),
        "table5_inter_rater_agreement": summary_inter_rater_agreement(
            df,
            rating_columns,
            min_common_items=5,
        ).round(3),
        "table6_krippendorff_alpha": summary_krippendorff_alpha(df, rating_columns).round(3),
    }

    table_paths = {
        name: write_table(table, output_path, name)
        for name, table in tables.items()
    }
    figure_paths = plot_all_kappa_heatmaps(
        df=df,
        rating_columns=rating_columns,
        output_dir=output_path,
        show=show_plots,
    )

    return AnalysisResult(
        tables=tables,
        table_paths=table_paths,
        figure_paths=figure_paths,
        output_dir=output_path,
    )
