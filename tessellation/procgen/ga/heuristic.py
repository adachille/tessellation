from tessellation.procgen.ga.genome import TessellationPhenome


DISQUALIFICATION_FITNESS = -100_000


def count_number_points(phenome: TessellationPhenome) -> float:
    """Count the number of points in the tessellation line."""
    return len(phenome.line_indices)


def bottom_top_even(phenome: TessellationPhenome) -> float:
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


def duplicated_points(phenome: TessellationPhenome) -> float:
    """Returns negative heuristic value for duplicated points."""
    n_line_indices = len(phenome.line_indices)
    n_unique_line_indices = len(set(phenome.line_indices))
    return n_unique_line_indices - n_line_indices


def out_of_bounds(phenome: TessellationPhenome, side_len: int) -> float:
    """Check that the tessellation line does not go out of bounds."""
    max_x, max_y = side_len - 1, side_len - 1
    min_x, min_y = 0, -1 * side_len
    in_bounds = all(
        [min_x <= x <= max_x and min_y <= y <= max_y for y, x in phenome.line_indices]
    )
    if in_bounds:
        return 0
    return DISQUALIFICATION_FITNESS


def is_connected(phenome: TessellationPhenome) -> float:
    # TODO: Implement fitness function to check that the line is connected
    raise NotImplementedError()


def reaches_corner_to_corner(phenome: TessellationPhenome) -> float:
    # TODO: Implement fitness function to check that the line is connected
    raise NotImplementedError()
