from antiaging_experiments.reliability import krippendorffs_alpha, quadratic_weighted_kappa


def test_quadratic_weighted_kappa_is_one_for_identical_ratings():
    assert quadratic_weighted_kappa([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]) == 1.0


def test_krippendorffs_alpha_is_one_for_complete_agreement():
    matrix = [
        [1, 2, 3, 4],
        [1, 2, 3, 4],
        [1, 2, 3, 4],
    ]
    assert krippendorffs_alpha(matrix) == 1.0
