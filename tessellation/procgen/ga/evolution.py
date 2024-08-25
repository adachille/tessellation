"""Methods for evolving tessellation genomes."""

from typing import Optional, Iterator, Callable

import numpy as np
from leap_ec import Individual

from tessellation.procgen.ga.genome import TessellationGenome
from tessellation.procgen.generator import Action, ALL_ACTIONS

rng = np.random.default_rng(42)


# TODO: convert this to functions rather than class methods
class Mutator:
    """Class that defines mutations for tessellation genomes."""

    def __init__(
        self,
        action_probs: Optional[list[float]] = None,
        substitution_prob: float = 0.1,
        insertion_prob: float = 0.1,
        deletion_prob: float = 0.1,
    ):
        if action_probs is None:
            self.action_probs = np.ones(len(Action)) / len(Action)
        else:
            self.action_probs = np.array(action_probs)
        self.substitution_prob = substitution_prob
        self.insertion_prob = insertion_prob
        self.deletion_prob = deletion_prob

    def substitute_action(self, existing_action: Action) -> list[Action]:
        """Substitute existing action with random action with substitution_prob."""
        if rng.random() < self.substitution_prob:
            return [rng.choice(np.array(ALL_ACTIONS), p=self.action_probs)]
        else:
            return [existing_action]

    def insert_action(self, existing_action: Action) -> list[Action]:
        """Insert random action with insertion_prob probability."""
        if rng.random() < self.insertion_prob:
            new_action = rng.choice(np.array(ALL_ACTIONS), p=self.action_probs)
            if rng.random() < 0.5:
                return [existing_action, new_action]
            else:
                return [new_action, existing_action]
        return [existing_action]

    def delete_action(self, existing_action: Action) -> list[Action]:
        """Delete existing action with deletion_prob probability."""
        if rng.random() < self.deletion_prob:
            return []
        return [existing_action]

    @staticmethod
    def apply_mutation(
        mutation_fn: Callable[[int, Action], list[Action]],
        next_individual: Iterator,
    ) -> Individual:
        """Apply mutation to each individual."""
        while True:
            individual = next(next_individual)
            genome = individual.genome
            new_action_list: list[Action] = []
            for idx, action in enumerate(genome.actions):
                new_actions = mutation_fn(action)
                new_action_list.extend(new_actions)

            individual.fitness = None  # invalidate fitness since we have new genome

            individual.genome = TessellationGenome(
                actions=new_action_list, start_point=genome.start_point
            )

            yield individual
