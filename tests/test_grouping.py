import math

from antiaging_experiments.grouping import collapse_authorship


def test_collapse_authorship_groups_scale_correctly():
    assert collapse_authorship(1) == "LLM"
    assert collapse_authorship(2) == "LLM"
    assert collapse_authorship(3) == "don't know"
    assert collapse_authorship(4) == "Human"
    assert collapse_authorship(5) == "Human"


def test_collapse_authorship_handles_missing_values():
    assert math.isnan(collapse_authorship(float("nan")))
