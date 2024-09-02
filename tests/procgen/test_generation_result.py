import json
import os

import numpy as np
import pytest

from tessellation.procgen import GenerationResult


@pytest.fixture(autouse=True)
def saved_generation_result_path(generation_result):
    file_path = "test.json"
    generation_result.save_as_json(file_path)
    yield file_path
    if os.path.exists(file_path):
        os.remove(file_path)


def test_save_as_json(generation_result, saved_generation_result_path):
    with open(saved_generation_result_path, "r") as file:
        data = json.load(file)

    expected_data = {
        "mask": generation_result.mask.tolist(),
        "tessellation_type": generation_result.tessellation_type.value,
        "metadata": generation_result.metadata,
    }
    assert data == expected_data


def test_to_json(generation_result):
    expected_data = {
        "mask": generation_result.mask.tolist(),
        "tessellation_type": generation_result.tessellation_type.value,
        "metadata": generation_result.metadata,
    }
    assert generation_result.to_json() == expected_data


def test_read_json(generation_result, saved_generation_result_path):
    loaded_result = GenerationResult.read_json(saved_generation_result_path)

    assert np.array_equal(loaded_result.mask, generation_result.mask)
    assert loaded_result.tessellation_type == generation_result.tessellation_type
    assert loaded_result.metadata == generation_result.metadata
