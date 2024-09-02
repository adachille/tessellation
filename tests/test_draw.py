import numpy as np
import pytest

from tessellation.draw import Drawer


@pytest.fixture
def drawer():
    return Drawer()


def test_tessellate(drawer, generation_result):
    n_shapes = 2
    actual_tessellation = drawer.tessellate(generation_result, n_shapes)

    expected_tessellation = np.array(
        [
            [1, 0, 0, 1],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [1, 0, 0, 1],
        ]
    )
    np.testing.assert_array_equal(actual_tessellation, expected_tessellation)
