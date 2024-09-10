import pytest
from tessellation.procgen.ga.heuristic import (
    bottom_top_not_even_penalty,
    duplicated_points_penalty,
    out_of_bounds_penalty,
    count_number_points_reward,
    bottom_top_even_reward,
    DISQUALIFICATION_FITNESS,
)
from tessellation.procgen.ga.genome import TessellationPhenome


# TODO: these come from Copilot, update!!!
@pytest.fixture
def phenome():
    return TessellationPhenome(line_indices=[])


def test_bottom_top_not_even_penalty(phenome):
    phenome.line_indices = [(0, 0), (1, 1), (0, 2), (-1, 3), (-1, 4)]
    assert bottom_top_not_even_penalty(phenome, max_diff_before_penalty=3) == 0
    assert bottom_top_not_even_penalty(phenome, max_diff_before_penalty=0) == -1
    phenome.line_indices = [(0, 0), (0, 1), (-1, 2), (-1, 2)]
    assert bottom_top_not_even_penalty(phenome, max_diff_before_penalty=0) == 0


def test_duplicated_points_penalty(phenome):
    phenome.line_indices = [(0, 0), (1, 1), (0, 0)]
    assert duplicated_points_penalty(phenome) == -1


def test_out_of_bounds_penalty(phenome):
    phenome.line_indices = [(0, 0), (1, 1), (0, 2)]
    assert out_of_bounds_penalty(phenome, side_len=3) == 0
    assert out_of_bounds_penalty(phenome, side_len=2) == DISQUALIFICATION_FITNESS


def test_count_number_points_reward(phenome):
    phenome.line_indices = [(0, 0)]
    assert count_number_points_reward(phenome) == 1

    phenome.line_indices = [(0, 0), (1, 1), (0, 2)]
    assert count_number_points_reward(phenome) == 3


def test_bottom_top_even_reward(phenome):
    phenome.line_indices = [(0, 0), (1, 1), (0, 2), (-1, 3), (-1, 4)]
    assert bottom_top_even_reward(phenome, max_diff_before_reward=0) == 0
    assert bottom_top_even_reward(phenome, max_diff_before_reward=1) == 0
    assert bottom_top_even_reward(phenome, max_diff_before_reward=3) == 2
