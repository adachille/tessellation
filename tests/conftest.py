import numpy as np
import pytest
from tessellation.procgen import GenerationResult, TessellationType


@pytest.fixture
def square_tessellation_mask():
    return np.array([[1, 0], [0, 1]])


@pytest.fixture
def generation_result(square_tessellation_mask):
    return GenerationResult(
        mask=square_tessellation_mask,
        tessellation_type=TessellationType.SQUARE_TRANSLATION,
    )
