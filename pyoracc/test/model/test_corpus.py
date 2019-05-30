'''
Copyright 2015, 2016 University College London.

This file is part of PyORACC.

PyORACC is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyORACC is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyORACC. If not, see <http://www.gnu.org/licenses/>.
'''


import pytest

from ...model.corpus import Corpus

from ..fixtures import tiny_corpus, sample_corpus, whole_corpus


def test_tiny():
    corpus = Corpus(source=tiny_corpus(), atftype='oracc')
    assert corpus.successes == 1
    assert corpus.failures == 1


def test_sample():
    corpus = Corpus(source=sample_corpus(), atftype='oracc')
    assert corpus.successes == 37
    assert corpus.failures == 2


@pytest.mark.skipif(not whole_corpus(),
                    reason="Need to set oracc_corpus_path to point "
                           "to the whole corpus, which is not bundled with "
                           "pyoracc")
def test_whole():
    corpus = Corpus(source=whole_corpus(), atftype='oracc')
    # There are a total of 8229 files in the corpus.
    # We have ommmited lacost/00atf/cdliatf_unblocked.atf
    # which is 61 MB and too large to fit in the git repository.
    assert corpus.successes == 6750
    assert corpus.failures == 1479
