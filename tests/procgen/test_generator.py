import numpy as np
import pytest
from tessellation.procgen.generator import Generator
from tessellation.procgen.action import Action


class TestGenerator(Generator):
    """A concrete implementation of Generator for testing purposes."""

    pass


@pytest.fixture
def generator():
    return TestGenerator()


def test_generate_not_implemented(generator):
    with pytest.raises(NotImplementedError):
        generator.generate()


def test_draw_line(generator):
    mask = np.zeros((5, 5), dtype=int)
    start_point = (0, 0)
    action_list = [
        Action.UP,
        Action.UP_RIGHT,
        Action.DOWN_RIGHT,
        Action.DOWN,
        Action.DOWN_RIGHT,
    ]

    expected_mask = np.array(
        [
            [1, 0, 1, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [1, 1, 1, 0, 0],
        ]
    )

    result_mask = generator._draw_line(mask, start_point, action_list)
    np.testing.assert_array_equal(result_mask, expected_mask)
