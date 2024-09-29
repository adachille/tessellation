"""Definitions for LEAP genome/phenome primitives for tessellation generation."""

import dataclasses

from leap_ec import Decoder

from tessellation.procgen import Action
from tessellation.procgen.generator import Point


@dataclasses.dataclass
class TessellationGenome:
    """Class that represents a tessellation genome."""

    actions: list[Action]
    start_point: Point
    end_point: Point

    def __init__(self, actions: list[Action], start_point: Point, end_point: Point):
        self.actions = actions
        self.start_point = start_point
        self.end_point = end_point

    def __eq__(self, other):
        return all(
            [
                self.actions == other.actions,
                self.start_point == other.start_point,
                self.end_point == self.end_point,
            ]
        )


@dataclasses.dataclass
class TessellationPhenome:
    """Class that represents a tessellation phenome."""

    line_indices: list[Point]

    def __init__(self, line_indices: list[Point]):
        self.line_indices = line_indices

    def __eq__(self, other):
        return self.line_indices == other.line_indices


class TessellationDecoder(Decoder):
    """Decoder for tessellation genomes."""

    def decode(
        self, genome: TessellationGenome, *args, **kwargs
    ) -> TessellationPhenome:
        """Decode a genome into a phenome."""
        cursor = {"x": genome.start_point.x, "y": genome.start_point.y}
        line_indices = [genome.start_point]
        for action in genome.actions:
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

            line_indices.append(Point(x=cursor["x"], y=cursor["y"]))
        line_indices.append(genome.end_point)
        return TessellationPhenome(line_indices=line_indices)
