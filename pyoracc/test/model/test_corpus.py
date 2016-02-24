import pytest

from ...model.corpus import Corpus

from ..fixtures import tiny_corpus, sample_corpus


slow = pytest.mark.skipif(
    not pytest.config.getoption("--runslow"),
    reason="need --runslow option to run"
)


def test_tiny():
    corpus = Corpus(source=tiny_corpus())
    assert corpus.successes == 1
    assert corpus.failures == 1


@slow
def test_sample():
    corpus = Corpus(source=sample_corpus())
    assert corpus.successes == 36
    assert corpus.failures == 3
