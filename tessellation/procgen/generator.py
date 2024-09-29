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

    def _draw_line(
        self,
        mask: np.ndarray,
        start_point: Union[tuple[int, int], Point],
        action_list: list[Action],
    ) -> np.ndarray:
        """Draw a line on the mask."""
        if isinstance(start_point, tuple):
            start_point = Point(x=start_point[0], y=start_point[1])

        self._draw_point_column(mask, start_point)

        cur_point = start_point
        for action in action_list:
            new_x, new_y = cur_point.x, cur_point.y
            if action in [Action.UP_RIGHT, Action.UP]:
                new_y -= 1
            if action in [Action.DOWN_RIGHT, Action.DOWN]:
                new_y += 1
            if action in [Action.UP_RIGHT, Action.DOWN_RIGHT, Action.RIGHT]:
                new_x += 1
            cur_point = Point(x=new_x, y=new_y)
            self._draw_point_column(mask, cur_point)

        return mask

    @staticmethod
    def _draw_point_column(mask: np.ndarray, point: Point):
        """Draw a point in the mask and fill in vertical space between the point and 0."""
        if point.y >= 0:
            mask[0 : point.y + 1, point.x] = 1
        else:
            mask[point.y :, point.x] = 1
