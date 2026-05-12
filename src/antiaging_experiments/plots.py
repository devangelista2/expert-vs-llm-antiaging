"""Plotting helpers for agreement visualizations."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .reliability import kappa_matrix_for_criterion


def plot_kappa_heatmap(
    matrix: np.ndarray,
    assessors: list[str],
    title: str,
    output_path: Path,
    show: bool = False,
) -> Path:
    """Render and save a heatmap of pairwise weighted kappas."""
    figure, axis = plt.subplots(figsize=(8, 6))
    masked = np.ma.masked_invalid(matrix)
    image = axis.imshow(masked, interpolation="nearest")

    axis.set_xticks(range(len(assessors)))
    axis.set_yticks(range(len(assessors)))
    axis.set_xticklabels(assessors, rotation=45, ha="right")
    axis.set_yticklabels(assessors)
    axis.set_title(title)

    colorbar = figure.colorbar(image, ax=axis)
    colorbar.set_label("Quadratic-weighted κ")

    for row_index in range(len(assessors)):
        for column_index in range(len(assessors)):
            if np.isnan(matrix[row_index, column_index]):
                continue
            axis.text(
                column_index,
                row_index,
                f"{matrix[row_index, column_index]:.2f}",
                ha="center",
                va="center",
                fontsize=7,
            )

    figure.tight_layout()
    figure.savefig(output_path, dpi=200, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(figure)
    return output_path


def plot_all_kappa_heatmaps(
    df: pd.DataFrame,
    rating_columns: dict[str, str],
    output_dir: Path,
    show: bool = False,
) -> list[Path]:
    """Generate one heatmap per rating criterion and return the saved file paths."""
    paths: list[Path] = []
    for criterion, column in rating_columns.items():
        matrix, assessors = kappa_matrix_for_criterion(df, column)
        slug = criterion.lower().replace(" ", "_")
        path = output_dir / f"kappa_heatmap_{slug}.png"
        plot_kappa_heatmap(
            matrix=matrix,
            assessors=assessors,
            title=f"Inter-rater agreement - {criterion}",
            output_path=path,
            show=show,
        )
        paths.append(path)
    return paths
