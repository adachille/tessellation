"""Base class for tesselation generators."""

import dataclasses
from abc import ABC
from typing import Union

import numpy as np

from tessellation.procgen.action import Action
from tessellation.procgen.generation_result import GenerationResult


@dataclasses.dataclass
class Point:
    """Class that represents a point on a tessellation line."""

    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, tuple):
            return self.x == other[0] and self.y == other[1]

        return self.x == other.x and self.y == other.y


class Generator(ABC):
    """Base class for tesselation generators."""

    def generate(self) -> GenerationResult:
        """Generate a new tesselation."""
        raise NotImplementedError

    @staticmethod
    def _draw_line(
        mask: np.ndarray,
        start_point: Union[tuple[int, int], Point],
        action_list: list[Action],
    ) -> np.ndarray:
        """Draw a line on the mask."""
        if isinstance(start_point, tuple):
            start_point = Point(x=start_point[0], y=start_point[1])

        cursor = {"x": start_point.x, "y": start_point.y}
        mask[cursor["y"], cursor["x"]] = 1
        for action in action_list:
            if action in [Action.UP_RIGHT, Action.UP]:
                cursor["y"] -= 1
            if action in [Action.DOWN_RIGHT, Action.DOWN]:
                cursor["y"] += 1
            if action in [Action.UP_RIGHT, Action.DOWN_RIGHT, Action.RIGHT]:
                cursor["x"] += 1

            if cursor["y"] >= 0:
                mask[0 : cursor["y"] + 1, cursor["x"]] = 1
            else:
                mask[cursor["y"] :, cursor["x"]] = 1

        return mask
