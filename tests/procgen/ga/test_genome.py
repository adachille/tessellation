import pytest
from tessellation.procgen.ga.genome import (
    Point,
    TessellationGenome,
    TessellationPhenome,
    TessellationDecoder,
)
from tessellation.procgen import Action


@pytest.fixture
def genome():
    actions = [Action.UP_RIGHT, Action.DOWN_RIGHT, Action.DOWN_RIGHT]
    start_point = Point(x=0, y=0)
    end_point = Point(x=3, y=0)
    yield TessellationGenome(actions, start_point, end_point=end_point)


@pytest.fixture
def phenome():
    line_indices = [
        Point(x=x, y=y) for x, y in [(0, 0), (1, -1), (2, 0), (3, 1), (3, 0)]
    ]
    yield TessellationPhenome(line_indices)


def test_tessellation_genome_init(genome):
    assert genome.actions == [Action.UP_RIGHT, Action.DOWN_RIGHT, Action.DOWN_RIGHT]
    assert genome.start_point == Point(x=0, y=0)
    assert genome.end_point == Point(x=3, y=0)


def test_tessellation_phenome_init(phenome):
    assert phenome.line_indices == [
        Point(x=x, y=y) for x, y in [(0, 0), (1, -1), (2, 0), (3, 1), (3, 0)]
    ]


def test_tessellation_decoder_decode(genome, phenome):
    decoder = TessellationDecoder()
    actual = decoder.decode(genome)
    assert actual == phenome
