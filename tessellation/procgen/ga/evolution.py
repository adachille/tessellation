"""Methods for evolving tessellation genomes."""

from typing import Optional, Iterator

import numpy as np
from leap_ec import Individual

from tessellation.procgen.ga.genome import TessellationGenome
from tessellation.procgen.generator import Action, ALL_ACTIONS

rng = np.random.default_rng(42)


# TODO: convert this to functions rather than class methods
class Mutator:
    """Class that defines mutations for tessellation genomes."""

    def __init__(
        self, action_probs: Optional[list[float]] = None, mutation_prob: float = 0.2
    ):
        if action_probs == None:
            self.action_probs = np.ones(len(Action)) / len(Action)
        else:
            self.action_probs = np.array(action_probs)
        self.mutation_prob = mutation_prob

    def mutate_actions_randomly(self, next_individual: Iterator) -> Individual:
        """Choose a random action from the list of actions with the given probabilities."""
        while True:
            individual = next(next_individual)
            genome = individual.genome
            new_action_list: list[Action] = []
            for idx, action in enumerate(genome.actions):
                if rng.random() < self.mutation_prob:
                    new_action = rng.choice(np.array(ALL_ACTIONS), p=self.action_probs)
                else:
                    new_action = action
                new_action_list.append(new_action)

            individual.fitness = None  # invalidate fitness since we have new genome

            individual.genome = TessellationGenome(
                actions=new_action_list, start_point=genome.start_point
            )

            yield individual
