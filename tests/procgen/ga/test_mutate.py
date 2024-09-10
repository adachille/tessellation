import numpy as np
import pytest
from tessellation.procgen.ga.mutate import (
    apply_mutation,
    substitute_action,
    insert_action,
    delete_action,
)
from tessellation.procgen import Action, ALL_ACTIONS
from tessellation.procgen.ga.genome import TessellationGenome
from leap_ec import Individual


@pytest.fixture
def actions():
    return [Action.UP, Action.RIGHT]


@pytest.fixture
def individual(actions):
    genome = TessellationGenome(actions, (0, 0))
    return Individual(genome)


def test_apply_mutation(individual):
    def mock_mutation_fn(action: Action, **kwargs) -> list[Action]:
        return [Action.DOWN]

    individual_iterator = iter([individual])
    mutated_individual = next(apply_mutation(mock_mutation_fn, individual_iterator))

    assert mutated_individual.genome.actions == [
        Action.DOWN,
        Action.DOWN,
    ]
    assert mutated_individual.fitness is None


def test_substitute_action(actions):
    action = actions[0]
    new_actions = substitute_action(action, substitution_prob=1.0)
    assert all(a in ALL_ACTIONS for a in new_actions)

    new_actions = substitute_action(action, substitution_prob=0.0)
    assert new_actions == [action]


def test_substitution_action_uses_action_probs(actions):
    action_probs = np.zeros(len(ALL_ACTIONS)).tolist()
    action_probs[-1] = 1
    new_actions = substitute_action(
        actions[0], substitution_prob=1.0, action_probs=action_probs
    )
    assert new_actions == [ALL_ACTIONS[-1]]


def test_insert_action(actions):
    action = actions[0]
    new_actions = insert_action(action, insertion_prob=1.0)
    assert all(a in ALL_ACTIONS for a in new_actions)
    assert len(new_actions) == 2

    new_actions = insert_action(action, insertion_prob=0.0)
    assert new_actions == [action]
    assert len(new_actions) == 1


def test_insert_action_uses_action_probs(actions):
    action_probs = np.zeros(len(ALL_ACTIONS)).tolist()
    action_probs[-1] = 1
    new_actions = insert_action(
        actions[0], insertion_prob=1.0, action_probs=action_probs
    )
    assert new_actions in [
        [actions[0], ALL_ACTIONS[-1]],
        [ALL_ACTIONS[-1], actions[0]],
    ]


def test_delete_action(actions):
    action = actions[0]
    new_actions = delete_action(action, deletion_prob=1.0)
    assert new_actions == []

    new_actions = delete_action(action, deletion_prob=0.0)
    assert new_actions == [action]
