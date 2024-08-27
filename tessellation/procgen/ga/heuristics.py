"""Fitness functions for the tessellation generation problem."""

from tessellation.procgen.ga.genome import TessellationPhenome


def count_number_points_heuristic(phenome: TessellationPhenome) -> float:
    """Count the number of points in the tessellation line."""
    return len(phenome.line_indices)


def bottom_top_even_heuristic(phenome: TessellationPhenome) -> float:
    """Check that the bottom and top sides have a relatively even number of points."""
    n_top_points = 0
    n_bottom_points = 0
    for idx in phenome.line_indices:
        y_idx = idx[0]
        if y_idx >= 0:
            n_top_points += 1
        else:
            n_bottom_points += 1
    n_points_diff = abs(n_top_points - n_bottom_points)
    score = -1 * n_points_diff  # We are maximizing, so we multiply by negative 1
    return score


def duplicated_points_heuristic(phenome: TessellationPhenome) -> float:
    """Returns negative heuristic value for duplicated points."""
    n_line_indices = len(phenome.line_indices)
    n_unique_line_indices = len(set(phenome.line_indices))
    return n_unique_line_indices - n_line_indices


def is_connected_heuristic(phenome: TessellationPhenome) -> float:
    # TODO: Implement fitness function to check that the line is connected
    raise NotImplementedError()


def reaches_corner_to_corner_heuristic(phenome: TessellationPhenome) -> float:
    # TODO: Implement fitness function to check that the line is connected
    raise NotImplementedError()
