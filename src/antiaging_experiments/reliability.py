"""Inter-rater reliability metrics used in the study."""

from __future__ import annotations

import itertools
import math

import numpy as np
import pandas as pd


def quadratic_weighted_kappa(
    a: np.ndarray | list[float],
    b: np.ndarray | list[float],
    min_rating: int = 1,
    max_rating: int = 5,
) -> float:
    """Compute quadratic-weighted Cohen's kappa between two raters."""
    a_array = np.asarray(a, dtype=float)
    b_array = np.asarray(b, dtype=float)

    mask = ~np.isnan(a_array) & ~np.isnan(b_array)
    a_array = a_array[mask].astype(int)
    b_array = b_array[mask].astype(int)

    if a_array.size == 0:
        return np.nan

    category_count = max_rating - min_rating + 1
    observed = np.zeros((category_count, category_count), dtype=float)
    for left, right in zip(a_array, b_array):
        observed[left - min_rating, right - min_rating] += 1

    total = observed.sum()
    if total == 0:
        return np.nan

    weights = np.zeros((category_count, category_count), dtype=float)
    for row_index in range(category_count):
        for column_index in range(category_count):
            weights[row_index, column_index] = (
                (row_index - column_index) ** 2 / (category_count - 1) ** 2
            )

    row_marginals = observed.sum(axis=1).reshape(-1, 1)
    column_marginals = observed.sum(axis=0).reshape(1, -1)
    expected = row_marginals * column_marginals / total

    observed_disagreement = (weights * observed).sum() / total
    expected_disagreement = (weights * expected).sum() / total
    if expected_disagreement == 0:
        return 1.0
    return 1.0 - observed_disagreement / expected_disagreement


def inter_rater_kappas_for_criterion(
    df: pd.DataFrame,
    rating_column: str,
    min_common_items: int = 5,
) -> list[dict[str, object]]:
    """Compute pairwise weighted kappas between assessors for one criterion."""
    subset = df[["Recommendation ID:", "Assessor", rating_column]].dropna(subset=[rating_column])
    subset = subset.dropna(subset=["Assessor"])
    subset = subset.drop_duplicates(subset=["Recommendation ID:", "Assessor"], keep="first")

    wide = subset.pivot(index="Recommendation ID:", columns="Assessor", values=rating_column)
    assessors = list(wide.columns)
    pairwise: list[dict[str, object]] = []

    for left, right in itertools.combinations(assessors, 2):
        paired_values = wide[[left, right]].dropna()
        if len(paired_values) < min_common_items:
            continue
        kappa = quadratic_weighted_kappa(paired_values[left].values, paired_values[right].values)
        if not math.isnan(kappa):
            pairwise.append({"pair": (left, right), "kappa": kappa, "n": len(paired_values)})

    return pairwise


def summary_inter_rater_agreement(
    df: pd.DataFrame,
    rating_columns: dict[str, str],
    min_common_items: int = 5,
) -> pd.DataFrame:
    """Summarize pairwise inter-rater agreement for each criterion."""
    rows = []
    for criterion, column in rating_columns.items():
        pairwise = inter_rater_kappas_for_criterion(df, column, min_common_items)
        kappas = [pair["kappa"] for pair in pairwise]
        if not kappas:
            rows.append(
                {
                    "Criterion": criterion,
                    "Num pairs": 0,
                    "Mean κ_w": np.nan,
                    "Min κ_w": np.nan,
                    "Max κ_w": np.nan,
                }
            )
            continue

        rows.append(
            {
                "Criterion": criterion,
                "Num pairs": len(kappas),
                "Mean κ_w": float(np.mean(kappas)),
                "Min κ_w": float(np.min(kappas)),
                "Max κ_w": float(np.max(kappas)),
            }
        )

    return pd.DataFrame(rows).set_index("Criterion")


def krippendorffs_alpha(data: np.ndarray, level_of_measurement: str = "ordinal") -> float:
    """Compute Krippendorff's alpha from a rater-by-item matrix."""
    matrix = np.asarray(data, dtype=float)
    mask = ~np.isnan(matrix)
    if mask.sum() == 0 or matrix.shape[0] < 2:
        return np.nan

    if level_of_measurement not in {"ordinal", "interval"}:
        raise ValueError(f"Unsupported level_of_measurement: {level_of_measurement}")

    def delta(left: float, right: float) -> float:
        return (left - right) ** 2

    observed_disagreement = 0.0
    observed_pairs = 0
    for item_index in range(matrix.shape[1]):
        item_ratings = matrix[:, item_index]
        item_ratings = item_ratings[~np.isnan(item_ratings)]
        if len(item_ratings) < 2:
            continue
        for left_index in range(len(item_ratings)):
            for right_index in range(left_index + 1, len(item_ratings)):
                observed_disagreement += delta(item_ratings[left_index], item_ratings[right_index])
                observed_pairs += 1

    if observed_pairs == 0:
        return np.nan

    observed_disagreement /= observed_pairs

    all_ratings = matrix[~np.isnan(matrix)]
    values, counts = np.unique(all_ratings, return_counts=True)
    probabilities = counts / counts.sum()

    expected_disagreement = 0.0
    for left_index, left_value in enumerate(values):
        for right_index, right_value in enumerate(values):
            if right_index > left_index:
                expected_disagreement += (
                    probabilities[left_index]
                    * probabilities[right_index]
                    * delta(left_value, right_value)
                )

    expected_disagreement *= 2
    if expected_disagreement == 0:
        return 1.0
    return 1.0 - observed_disagreement / expected_disagreement


def krippendorff_alpha_for_criterion(df: pd.DataFrame, rating_column: str) -> float:
    """Extract the assessor-by-item matrix and compute Krippendorff's alpha."""
    subset = df[["Recommendation ID:", "Assessor", rating_column]].dropna(subset=[rating_column])
    subset = subset.drop_duplicates(subset=["Recommendation ID:", "Assessor"], keep="first")
    wide = subset.pivot(index="Assessor", columns="Recommendation ID:", values=rating_column)
    return krippendorffs_alpha(wide.values, level_of_measurement="ordinal")


def summary_krippendorff_alpha(df: pd.DataFrame, rating_columns: dict[str, str]) -> pd.DataFrame:
    """Compute Krippendorff's alpha for each criterion."""
    rows = []
    for criterion, column in rating_columns.items():
        rows.append(
            {
                "Criterion": criterion,
                "Krippendorff_alpha": krippendorff_alpha_for_criterion(df, column),
            }
        )
    return pd.DataFrame(rows).set_index("Criterion")


def kappa_matrix_for_criterion(
    df: pd.DataFrame,
    rating_column: str,
) -> tuple[np.ndarray, list[str]]:
    """Build a square assessor-by-assessor matrix of weighted kappa values."""
    subset = df[["Recommendation ID:", "Assessor", rating_column]].dropna(subset=[rating_column])
    subset = subset.dropna(subset=["Assessor"])
    subset = subset.drop_duplicates(subset=["Recommendation ID:", "Assessor"], keep="first")

    wide = subset.pivot(index="Recommendation ID:", columns="Assessor", values=rating_column)
    assessors = list(wide.columns)
    matrix = np.zeros((len(assessors), len(assessors)), dtype=float)

    for row_index, left in enumerate(assessors):
        for column_index, right in enumerate(assessors):
            if row_index == column_index:
                matrix[row_index, column_index] = 1.0
                continue

            paired_values = wide[[left, right]].dropna()
            if len(paired_values) == 0:
                matrix[row_index, column_index] = np.nan
                continue

            matrix[row_index, column_index] = quadratic_weighted_kappa(
                paired_values[left].values,
                paired_values[right].values,
            )

    return matrix, assessors
