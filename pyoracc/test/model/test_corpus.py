from ...model.corpus import Corpus

from ..fixtures import tiny_corpus


def test_tiny():
    corpus = Corpus(source=tiny_corpus())
    assert corpus.successes == 1
    assert corpus.failures == 1
