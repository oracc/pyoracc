from ...model.corpus import Corpus

from ..fixtures import tiny_corpus, sample_corpus


def test_tiny():
    corpus = Corpus(source=tiny_corpus())
    assert corpus.successes == 1
    assert corpus.failures == 1


def test_sample():
    corpus = Corpus(source=sample_corpus())
    assert corpus.successes == 36
    assert corpus.failures == 3
