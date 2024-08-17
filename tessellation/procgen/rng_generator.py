from copy import deepcopy
from enum import Enum, auto
from typing import Optional

import numpy as np

from tessellation.procgen.generator import Generator


class Action(Enum):
    """Enum representing the possible actions for the generator."""

    UP = auto()
    DOWN = auto()
    UP_RIGHT = auto()
    DOWN_RIGHT = auto()
    RIGHT = auto()


ACTIONS_LIST = np.array([action for action in Action])


class RNGGenerator(Generator):
    """Generator that uses a random number generator to generate the tesselation mask."""

    def __init__(self, seed: int = 42):
        self.rng = np.random.default_rng(seed)

    def generate(
        self,
        side_len: int,
        action_list: Optional[list[Action]] = None,
        action_probs: Optional[list[Action]] = None,
    ) -> np.ndarray:
        """Generate a tesselation mask using a random number generator."""
        if action_list is None:
            action_list = ACTIONS_LIST
        if action_probs is None:
            action_probs = [1 / len(action_list)] * len(action_list)

        assert len(action_list) == len(action_probs)

        y_mask = self._generate_side(side_len, action_list, action_probs)
        x_mask = self._generate_side(side_len, action_list, action_probs).T
        return x_mask | y_mask

    def _generate_side(
        self, side_len: int, actions_list: list, action_probs: list
    ) -> np.ndarray:
        mask = np.zeros((side_len, side_len), dtype=int)
        cursor = {"x": 0, "y": 0}
        while cursor["x"] < side_len - 1:
            action = self._get_rand_action(
                actions_list=actions_list, action_probs=action_probs
            )
            # Note: it's probably inefficient to call flood_fill on every step, but for
            # now, it's giving the most consistent results.
            self._flood_fill(mask, (cursor["y"], cursor["x"]), 1)
            if action == Action.UP:
                cursor["y"] -= 1
            elif action == Action.UP_RIGHT:
                cursor["y"] -= 1
                cursor["x"] += 1
            elif action == Action.RIGHT:
                cursor["x"] += 1
            elif action == Action.DOWN:
                cursor["y"] += 1
            elif action == Action.DOWN_RIGHT:
                cursor["y"] += 1
                cursor["x"] += 1
            else:
                raise ValueError(f"Unsupported action: {action}")

            if cursor["y"] >= 0:
                mask[0 : cursor["y"], cursor["x"]] = 1
            else:
                mask[cursor["y"] :, cursor["x"]] = 1

        return mask

    def _get_rand_action(
        self, actions_list: list[Action], action_probs: list[float]
    ) -> int:
        """Choose a random action from the list of actions with the given probabilities."""
        return self.rng.choice(actions_list, p=action_probs)
