"""Table-generation functions for the paper analyses."""

from __future__ import annotations

import pandas as pd
from scipy.stats import mannwhitneyu

from .constants import GROUP_DISPLAY_ORDER, HUMAN_COMPARISON_ORDER
from .grouping import collapse_authorship, real_authorship, real_authorship_model_level


def table1_medians(
    df: pd.DataFrame,
    rating_columns: dict[str, str],
    groups: dict[str, pd.Series],
) -> pd.DataFrame:
    """Compute median ratings by criterion and source."""
    rows = []
    for criterion, column in rating_columns.items():
        row = {"Criterion": criterion}
        for group_name in GROUP_DISPLAY_ORDER:
            row[group_name] = df.loc[groups[group_name], column].median()
        rows.append(row)
    return pd.DataFrame(rows).set_index("Criterion")[GROUP_DISPLAY_ORDER]


def table2_means(
    df: pd.DataFrame,
    rating_columns: dict[str, str],
    groups: dict[str, pd.Series],
) -> pd.DataFrame:
    """Compute mean ratings by criterion and source."""
    rows = []
    for criterion, column in rating_columns.items():
        row = {"Criterion": criterion}
        for group_name in GROUP_DISPLAY_ORDER:
            row[group_name] = df.loc[groups[group_name], column].mean()
        rows.append(row)
    return pd.DataFrame(rows).set_index("Criterion")[GROUP_DISPLAY_ORDER]


def table3_attribution(df: pd.DataFrame, authorship_column: str) -> pd.DataFrame:
    """Compute perceived authorship percentages by broad and model-level source."""
    attribution_df = df.copy()
    attribution_df["Attributed"] = attribution_df[authorship_column].apply(collapse_authorship)
    attribution_df["RealBroad"] = attribution_df.apply(real_authorship, axis=1)
    attribution_df["RealModel"] = attribution_df.apply(real_authorship_model_level, axis=1)

    broad = pd.crosstab(
        attribution_df["RealBroad"],
        attribution_df["Attributed"],
        normalize="index",
    ) * 100.0
    broad = broad.reindex(index=["Human", "LLMs"], columns=["Human", "don't know", "LLM"])

    model = pd.crosstab(
        attribution_df["RealModel"],
        attribution_df["Attributed"],
        normalize="index",
    ) * 100.0
    model = model.reindex(
        index=["Gemini", "GPT", "Claude"],
        columns=["Human", "don't know", "LLM"],
    )

    table = pd.concat([broad, model]).round(1)
    table.index.name = "Real authorship"
    table.columns.name = "Attributed to"
    return table


def table4_mannwhitney(
    df: pd.DataFrame,
    rating_columns: dict[str, str],
    groups: dict[str, pd.Series],
) -> pd.DataFrame:
    """Compute two-sided Mann-Whitney U test p-values against human recommendations."""
    rows = []
    for criterion, column in rating_columns.items():
        row = {"Criterion": criterion}
        human_values = df.loc[groups["H"], column]
        for group_name in HUMAN_COMPARISON_ORDER:
            comparison_values = df.loc[groups[group_name], column]
            _, p_value = mannwhitneyu(
                human_values,
                comparison_values,
                alternative="two-sided",
                method="auto",
            )
            row[f"H vs {group_name}"] = p_value
        rows.append(row)
    return pd.DataFrame(rows).set_index("Criterion")[
        [f"H vs {group_name}" for group_name in HUMAN_COMPARISON_ORDER]
    ]
