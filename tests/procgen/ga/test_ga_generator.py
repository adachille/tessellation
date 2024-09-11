import numpy as np
import pytest
from tessellation.procgen.ga.ga_generator import GATessellationGenerator
from tessellation.procgen.ga.genome import TessellationGenome
from tessellation.procgen import Action, GenerationResult, TessellationType
from leap_ec import Individual


@pytest.fixture
def heuristic_fns():
    yield [lambda x: 10.0, lambda x: 5.0]


@pytest.fixture
def mutation_fns():
    yield [lambda action: [action, Action.RIGHT]]


@pytest.fixture
def generator(heuristic_fns, mutation_fns):
    yield GATessellationGenerator(
        heuristic_fns=heuristic_fns,
        mutation_fns=mutation_fns,
        side_len=4,
        max_generations=10,
        population_size=10,
    )


def test_ga_tessellation_generator_init(generator, heuristic_fns, mutation_fns):
    assert generator.side_len == 4
    assert generator.max_generations == 10
    assert generator.population_size == 10
    assert generator.problem.heuristic_fns == heuristic_fns
    assert generator.mutation_fns == mutation_fns


def test_get_generation_result(generator):
    individual = Individual(TessellationGenome([Action.UP, Action.RIGHT], (0, 0)))
    individual.fitness = 10.0
    expected_mask = np.array([[1, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 0], [1, 1, 0, 0]])
    result = generator.get_generation_result(individual)
    assert isinstance(result, GenerationResult)
    assert result.tessellation_type == TessellationType.SQUARE_TRANSLATION
    assert result.metadata["generator_class"] == "GATessellationGenerator"
    assert result.metadata["fitness"] == 10.0
    assert np.array_equal(result.mask, expected_mask)


def test_get_generation_result_returns_none_on_index_error(generator):
    individual = Individual(TessellationGenome([Action.RIGHT, Action.RIGHT], (0, 0)))
    generator.side_len = 2
    result = generator.get_generation_result(individual)
    assert result is None
