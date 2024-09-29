"""Genetic Algorithm based tessellation generator."""

from typing import Callable, Optional

import numpy as np
from leap_ec import Representation, ops, probe, Individual
from leap_ec.algorithm import generational_ea

from tessellation.procgen import Generator, GenerationResult, Action, TessellationType
from tessellation.procgen.ga.genome import TessellationPhenome, TessellationDecoder
from tessellation.procgen.ga.problem import TessellationProblem, initialize_genome
from tessellation.procgen.generator import Point


class GATessellationGenerator(Generator):
    """Genetic Algorithm based tessellation generator."""

    def __init__(
        self,
        heuristic_fns: list[Callable[[TessellationPhenome], float]],
        mutation_fns: list[Callable[[Action, ...], list[Action]]],
        heuristic_fn_weights: Optional[list[float]] = None,
        side_len: int = 100,
        use_endpoint: bool = True,
        max_generations: int = 100,
        population_size: int = 100,
    ):
        self.side_len = side_len
        self.use_endpoint = use_endpoint
        self.problem = TessellationProblem(
            heuristic_fns=heuristic_fns,
            fn_weights=heuristic_fn_weights,
            side_len=self.side_len,
            use_endpoint=self.use_endpoint,
        )
        self.representation = Representation(
            decoder=TessellationDecoder(),
            initialize=lambda: initialize_genome(self.problem),
        )
        self.mutation_fns = mutation_fns

        self.max_generations = max_generations
        self.population_size = population_size

        self.population = None

    def generate(self, individual_idx: int = 0) -> GenerationResult:
        """Generate a new tesselation."""
        if self.population is None:
            self.evolve()

        return self.get_generation_result(self.population[individual_idx])

    def evolve(self) -> list[GenerationResult]:
        """Run genetic algorithm and evolve the population."""
        self.population = generational_ea(
            max_generations=self.max_generations,
            pop_size=self.population_size,
            problem=self.problem,
            representation=self.representation,
            # The operator pipeline
            pipeline=[
                ops.tournament_selection,  # Select parents via tournament
                ops.clone,  # Copy them (just to be safe)
                *self.mutation_fns,  # Apply mutation functions
                # Crossover w/ 40% chance of swapping gen
                # ops.UniformCrossover(p_swap=0.4), es
                ops.evaluate,  # Evaluate fitness
                # pylint: disable=no-value-for-parameter
                ops.pool(size=self.population_size),  # Collect offspring into new pop
                probe.BestSoFarProbe(),  # Print best so far
            ],
        )
        return [
            self.get_generation_result(individual) for individual in self.population
        ]

    def get_generation_result(
        self, individual: Individual
    ) -> Optional[GenerationResult]:
        """Return the generation result for the individual."""
        genome = individual.genome
        mask = np.zeros((self.side_len, self.side_len), dtype=int)
        try:
            mask = self._draw_line(
                mask, genome.start_point, genome.actions, genome.end_point
            )
            mask_t = self._draw_line(
                mask.T, genome.start_point, genome.actions, genome.end_point
            )
            final_mask = mask | mask_t

            return GenerationResult(
                final_mask,
                TessellationType.SQUARE_TRANSLATION,
                metadata={
                    "generator_class": "GATessellationGenerator",
                    "fitness": individual.fitness,
                },
            )
        except IndexError:
            print(f"Invalid individual: {individual}, returning None")
            return None

    def _draw_line(
        self,
        mask: np.ndarray,
        start_point: Point,
        action_list: list[Action],
        end_point: Optional[Point] = None,
    ) -> np.ndarray:
        """Draw a line on the mask."""
        if end_point is None:
            end_point = Point(x=mask.shape[1] - 1, y=0)
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

        self._draw_point_column(mask, end_point)

        return mask
