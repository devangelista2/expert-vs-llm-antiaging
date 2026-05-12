"""Command-line interface for the analysis package."""

from __future__ import annotations

import argparse

from .constants import DEFAULT_EXCEL_PATH, DEFAULT_OUTPUT_DIR, DEFAULT_SHEET_NAME
from .pipeline import run_analysis


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line parser."""
    parser = argparse.ArgumentParser(
        description="Reproduce tables and agreement plots for the anti-aging recommendation study."
    )
    parser.add_argument(
        "--excel-path",
        default=str(DEFAULT_EXCEL_PATH),
        help="Path to the Excel workbook containing assessor answers.",
    )
    parser.add_argument(
        "--sheet",
        default=DEFAULT_SHEET_NAME,
        help="Workbook sheet to analyze.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory where CSV tables and PNG figures will be written.",
    )
    parser.add_argument(
        "--show-plots",
        action="store_true",
        help="Display plots interactively in addition to saving them.",
    )
    return parser


def main() -> int:
    """Run the CLI."""
    args = build_parser().parse_args()
    result = run_analysis(
        excel_path=args.excel_path,
        sheet_name=args.sheet,
        output_dir=args.output_dir,
        show_plots=args.show_plots,
    )

    print(f"Generated outputs in: {result.output_dir}")
    for name, path in result.table_paths.items():
        print(f"{name}: {path}")
    for path in result.figure_paths:
        print(f"figure: {path}")
    return 0
