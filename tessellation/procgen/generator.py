"""Base class for tesselation generators."""

from abc import ABC
from enum import Enum, auto

import numpy as np
from skimage.segmentation import flood_fill


class Action(Enum):
    """Enum representing the possible actions for the generator."""

    UP = auto()
    UP_RIGHT = auto()
    UP_LEFT = auto()
    DOWN = auto()
    DOWN_RIGHT = auto()
    DOWN_LEFT = auto()
    RIGHT = auto()
    LEFT = auto()


class Generator(ABC):
    """Base class for tesselation generators."""

    def generate(self, *args, **kwargs) -> np.ndarray:
        """Generate a new tesselation."""
        raise NotImplementedError

    @staticmethod
    def tessellate(mask: np.ndarray, n_shapes: int = 5) -> np.ndarray:
        """Tessellate the mask n_shapes times."""
        side_len = mask.shape[0]
        side_len_full_image = side_len * n_shapes
        tessellation = np.zeros((side_len_full_image, side_len_full_image), dtype=int)

        color = 0
        for i in range(n_shapes):
            for j in range(n_shapes):
                y_start = i * side_len
                y_end = y_start + side_len

                x_start = j * side_len
                x_end = x_start + side_len

                if color == 0:
                    color_mask = np.logical_not(mask)
                    color = 1
                else:
                    color_mask = mask
                    color = 0

                tessellation[y_start:y_end, x_start:x_end] = color_mask

        return tessellation

    @staticmethod
    def _draw_line(
        mask: np.ndarray,
        start_point: tuple[int, int],  # (y, x)
        action_list: list[Action],
        should_flood_fill: bool = True,
    ) -> np.ndarray:
        """Draw a line on the mask."""
        cursor = {"x": start_point[1], "y": start_point[0]}
        mask[cursor["y"], cursor["x"]] = 1
        for action in action_list:
            if action in [Action.UP_LEFT, Action.UP_RIGHT, Action.UP]:
                cursor["y"] -= 1
            if action in [Action.DOWN_LEFT, Action.DOWN_RIGHT, Action.DOWN]:
                cursor["y"] += 1
            if action in [Action.UP_LEFT, Action.DOWN_LEFT, Action.LEFT]:
                cursor["x"] -= 1
            if action in [Action.UP_RIGHT, Action.DOWN_RIGHT, Action.RIGHT]:
                cursor["x"] += 1

            mask[cursor["y"], cursor["x"]] = 1
            if should_flood_fill:
                Generator._flood_fill(mask, (cursor["y"], cursor["x"]), 1)

        return mask

    @staticmethod
    def _flood_fill(mask: np.ndarray, start_point: tuple[int, int], fill_value: int):
        """Flood fill the 2d mask."""
        return flood_fill(mask, start_point, fill_value)
