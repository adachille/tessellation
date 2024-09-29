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

    def __eq__(self, other):
        return all(
            [
                self.actions == other.actions,
                self.start_point == other.start_point,
            ]
        )


@dataclasses.dataclass
class TessellationPhenome:
    """Class that represents a tessellation phenome."""

    line_indices: list[Point]

    def __eq__(self, other):
        return self.line_indices == other.line_indices


class TessellationDecoder(Decoder):
    """Decoder for tessellation genomes."""

    def decode(
        self, genome: TessellationGenome, *args, **kwargs
    ) -> TessellationPhenome:
        """Decode a genome into a phenome."""
        cursor = {"x": genome.start_point.x, "y": genome.start_point.y}
        line_indices = [Point(x=genome.start_point.x, y=genome.start_point.y)]
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
        return TessellationPhenome(line_indices=line_indices)
