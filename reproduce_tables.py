"""Backward-compatible entry point for the experiment analysis pipeline."""

from antiaging_experiments.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
