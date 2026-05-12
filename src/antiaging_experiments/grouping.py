"""Grouping logic used across the paper tables."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .constants import MODEL_NAME_MAP


def make_groups(df: pd.DataFrame) -> dict[str, pd.Series]:
    """Build boolean masks for human, all LLMs, and each named model."""
    groups: dict[str, pd.Series] = {}
    is_human = df["Source"].eq("Human")
    is_ai = df["Source"].eq("AI")

    groups["H"] = is_human
    groups["LLMs"] = is_ai
    groups["Gemini"] = is_ai & df["AI model"].eq("Gemini 2.0 Flash")
    groups["GPT"] = is_ai & df["AI model"].eq("GPT 4o")
    groups["Claude"] = is_ai & df["AI model"].eq("Claude Opus 4")
    return groups


def collapse_authorship(raw_value: int | float) -> str | float:
    """Collapse the 1-5 authorship scale into LLM / don't know / Human."""
    if pd.isna(raw_value):
        return np.nan

    value = int(raw_value)
    if value in (1, 2):
        return "LLM"
    if value == 3:
        return "don't know"
    if value in (4, 5):
        return "Human"
    return np.nan


def real_authorship(row: pd.Series) -> str | float:
    """Return the broad ground-truth authorship label used in attribution analyses."""
    if row["Source"] == "Human":
        return "Human"
    if row["Source"] == "AI":
        return "LLMs"
    return np.nan


def real_authorship_model_level(row: pd.Series) -> str | float:
    """Return the model-level ground-truth authorship label used in Table 3."""
    if row["Source"] == "Human":
        return "Human"
    if row["Source"] != "AI":
        return np.nan
    return MODEL_NAME_MAP.get(row["AI model"], "LLMs")
