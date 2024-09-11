import pytest
from tessellation.procgen.ga.genome import TessellationGenome, TessellationPhenome
from tessellation.procgen import Action
from tessellation.procgen.ga.problem import TessellationProblem, initialize_genome


@pytest.fixture
def genome():
    actions = [Action.UP_RIGHT, Action.DOWN_RIGHT, Action.DOWN_RIGHT]
    start_point = (0, 0)
    yield TessellationGenome(actions, start_point)


@pytest.fixture
def phenome():
    yield TessellationPhenome(line_indices=[(0, 0), (-1, 1), (0, 2), (1, 4)])


@pytest.fixture
def population():
    yield [
        TessellationGenome([Action.UP, Action.RIGHT], (0, 0)),
        TessellationGenome([Action.DOWN, Action.LEFT], (1, 1)),
    ]


@pytest.fixture
def problem():
    yield TessellationProblem(
        heuristic_fns=[lambda x: 10.0, lambda x: 5.0],
        fn_weights=[1.0, 1.0],
        side_len=4,
    )


def test_evaluate_fitness(problem, phenome):
    fitness = problem.evaluate(phenome)
    assert fitness == 15.0


def test_equivalent(problem):
    assert problem.equivalent(1.0, 1.0)
    assert not problem.equivalent(1.0, 2.0)


def test_worse_than(problem):
    assert problem.worse_than(1.0, 2.0)
    assert not problem.worse_than(2.0, 1.0)


def test_initialize_genome(problem):
    initialized_genome = initialize_genome(problem)
    assert initialized_genome.start_point == (0, 0)
    assert all(action in Action for action in initialized_genome.actions)
    assert len(initialized_genome.actions) == problem.side_len
