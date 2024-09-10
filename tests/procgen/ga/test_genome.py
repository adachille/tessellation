import pytest
from tessellation.procgen.ga.genome import (
    TessellationGenome,
    TessellationPhenome,
    TessellationDecoder,
)
from tessellation.procgen import Action


@pytest.fixture
def genome():
    actions = [Action.UP_RIGHT, Action.DOWN_RIGHT, Action.DOWN_RIGHT]
    start_point = (0, 0)
    return TessellationGenome(actions, start_point)


@pytest.fixture
def phenome():
    line_indices = [(0, 0), (-1, 1), (0, 2), (1, 3)]
    return TessellationPhenome(line_indices)


def test_tessellation_genome_init(genome):
    assert genome.actions == [Action.UP_RIGHT, Action.DOWN_RIGHT, Action.DOWN_RIGHT]
    assert genome.start_point == (0, 0)


def test_tessellation_phenome_init(phenome):
    assert phenome.line_indices == [(0, 0), (-1, 1), (0, 2), (1, 3)]


def test_tessellation_decoder_decode(genome, phenome):
    decoder = TessellationDecoder()
    actual = decoder.decode(genome)
    assert actual == phenome
