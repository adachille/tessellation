import pytest
from tessellation.procgen.rng.rng_generator import RNGGenerator
from tessellation.procgen.action import Action
from tessellation.procgen.generation_result import GenerationResult
from tessellation.procgen.tessellation_type import TessellationType


@pytest.fixture
def rng_generator():
    return RNGGenerator(seed=42, side_len=5)


def test_generate(rng_generator):
    generation_result = rng_generator.generate()

    assert isinstance(generation_result, GenerationResult)
    assert generation_result.mask.shape == (
        rng_generator.side_len,
        rng_generator.side_len,
    )
    assert generation_result.tessellation_type == TessellationType.SQUARE_TRANSLATION


def test_generate_side(rng_generator):
    side_len = 5
    action_probs = [0.2, 0.2, 0.2, 0.2, 0.2]
    mask, action_list = rng_generator._generate_side(side_len, action_probs)

    assert mask.shape == (side_len, side_len)
    assert all(isinstance(action, Action) for action in action_list)


def test_get_rand_action(rng_generator):
    actions_list = [
        Action.UP,
        Action.UP_RIGHT,
        Action.RIGHT,
        Action.DOWN,
        Action.DOWN_RIGHT,
    ]
    action_probs = [0.2, 0.2, 0.2, 0.2, 0.2]
    action = rng_generator._get_rand_action(actions_list, action_probs)

    assert action in actions_list
