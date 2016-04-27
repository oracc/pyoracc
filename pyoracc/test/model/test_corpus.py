import pytest

from ...model.corpus import Corpus

from ..fixtures import tiny_corpus, sample_corpus, whole_corpus


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


@pytest.mark.skipif(not whole_corpus(),
                    reason="Need to set oracc_corpus_path to point "
                           "to the whole corpus, which is not bundled with "
                           "pyoracc")
@slow
def test_whole():
    corpus = Corpus(source=whole_corpus())
    # there is a total of 2868 files in the corpus
    assert corpus.successes == 2477
    assert corpus.failures == 391
