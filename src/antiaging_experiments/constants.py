"""Project-wide constants."""

from pathlib import Path

DEFAULT_EXCEL_PATH = Path("data/RecsAssessByExperts2025.xlsx")
DEFAULT_SHEET_NAME = "Answers"
DEFAULT_OUTPUT_DIR = Path("outputs")

GROUP_DISPLAY_ORDER = ["H", "LLMs", "Gemini", "GPT", "Claude"]
HUMAN_COMPARISON_ORDER = ["LLMs", "Gemini", "GPT", "Claude"]

RATING_PREFIXES = {
    "Effectiveness": "Effectiveness:",
    "Safety": "Safety:",
    "Personalization": "Personalization:",
    "Suitability": "Overall Suitability:",
}

AUTHORSHIP_COLUMN_PREFIX = "Authorship: Do you think that this recommendation"

MODEL_NAME_MAP = {
    "Gemini 2.0 Flash": "Gemini",
    "GPT 4o": "GPT",
    "Claude Opus 4": "Claude",
}
