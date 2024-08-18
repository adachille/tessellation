"""Fitness functions for the tessellation generation problem."""

from tessellation.procgen.ga.genome import TessellationPhenome


def count_number_points_heuristic(phenome: TessellationPhenome) -> float:
    """Count the number of points in the tessellation line."""
    return len(phenome.line_indices)


def is_connected_heuristic(phenome: TessellationPhenome) -> float:
    # TODO: Implement fitness function to check that the line is connected
    raise NotImplementedError()


def reaches_corner_to_corner_heuristic(phenome: TessellationPhenome) -> float:
    # TODO: Implement fitness function to check that the line is connected
    raise NotImplementedError()
