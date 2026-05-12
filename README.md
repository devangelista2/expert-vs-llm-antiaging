# Expert vs LLM Anti-Aging Recommendation Experiments

This repository contains the reproducible analysis code for the expert-vs-LLM evaluation study on anti-aging supplement recommendations. The analysis is based on the assessment workbook in [`data/RecsAssessByExperts2025.xlsx`](data/RecsAssessByExperts2025.xlsx), and the paper draft included in this repository is kept as the primary study reference:

## Repository layout

```text
.
├── data/                       Input assessment workbook
├── outputs/                    Generated tables and figures
├── src/antiaging_experiments/  Analysis package
├── tests/                      Lightweight unit tests
├── pyproject.toml              Project metadata and dependencies
└── reproduce_tables.py         Backward-compatible wrapper
```

## What the code produces

The pipeline reproduces the main quantitative artifacts used by the study:

- Table 1: median ratings by criterion and source
- Table 2: mean ratings by criterion and source
- Table 3: perceived authorship attribution percentages
- Table 4: Mann-Whitney U tests comparing human recommendations against LLM groups
- Table 5: pairwise inter-rater agreement summaries using quadratic-weighted Cohen's kappa
- Table 6: Krippendorff's alpha for ordinal ratings
- Figure set: heatmaps of assessor-to-assessor agreement for each evaluation criterion

## Installation

Create a virtual environment and install the package in editable mode:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
```

## Usage

Run the full pipeline with the default workbook:

```bash
python reproduce_tables.py
```

Or use the package CLI directly:

```bash
antiaging-experiments --output-dir outputs
```

Useful options:

```bash
antiaging-experiments --excel-path data/RecsAssessByExperts2025.xlsx --sheet Answers --show-plots
```

By default, generated CSV tables and PNG figures are written to `outputs/`.

## Notes on reproducibility

- The analysis expects the `Answers` sheet structure found in the provided workbook.
- Rating columns are discovered by stable column prefixes rather than hard-coded full header strings.
- The repository preserves the original one-file entry point, but the actual implementation now lives in `src/antiaging_experiments/`.