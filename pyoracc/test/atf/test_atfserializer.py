# -*- coding: utf-8 -*-
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

from pyoracc.atf.common.atffile import AtfFile
from pyoracc.model.line import Line
from pyoracc.test.fixtures import belsunu


def test_belsunu_serializer():
    """
    Parse belsunu.atf, then serialize, parse again, serialize again,
    compare.
    Comparing serialized output with input file would bring up differences
    that might not be significant (white spaces, newlines, etc).
    The solution is to parse again the serialized file, serialize again,
    then compare the two serializations.
    """
    serialized_1 = AtfFile(belsunu()).serialize()
    serialized_2 = AtfFile(serialized_1).serialize()
    assert serialized_1 == serialized_2


@pytest.mark.xfail
def test_line_word():
    """
    Get a sample word with unicode chars and check serialization is
    correct.
    """
    line = Line("1")
    line.words.append(u"\u2086")
    line_ser = line.serialize()
    assert line_ser == "1.\t" + u"\u2086"


def test_line_words():
    """
    Get a sample line of words with unicode chars and test serialization.
    1. [MU] 1.03-KAM {iti}AB GE₆ U₄ 2-KAM
    """
    atf_file = AtfFile(belsunu())
    uline = atf_file.text.children[0].children[0].children[0]
    uwords = uline.words
    gold = [u'[MU]', u'1.03-KAM', u'{iti}AB', u'GE\u2086', u'U\u2084',
            u'2-KAM']
    assert uwords == gold


def test_line_lemmas():
    """
    Get a sample line of lemmas with unicode chars and test serialization.
    šatti[year]N; n; Ṭebetu[1]MN; mūša[at night]AV; ūm[day]N; n
    """
    atf_file = AtfFile(belsunu())
    uline = atf_file.text.children[0].children[0].children[0]
    ulemmas = uline.lemmas
    gold = [u' \u0161atti[year]N', u'n', u'\u1e6cebetu[1]MN',
            u'm\u016b\u0161a[at night]AV', u'\u016bm[day]N', u'n']
    assert ulemmas == gold


# TODO: Build list of atf files for testing and make a test to go through the
# list of test and try serializing each of them.
@pytest.mark.xfail
def test_text_code_and_description():
    """
    Check if serializing works for the code/description case - first line
    of ATF texts.
    """
    text = "&X001001 = JCS 48, 089\n"
    atf = AtfFile(text)
    serialized = atf.serialize()
    assert serialized.strip()+"\n" == text


@pytest.mark.xfail
def test_text_project():
    """
    Check if serializing works for the project lines.
    """
    text = "#project: cams/gkab\n"
    serialized = AtfFile(text).serialize()
    assert serialized.strip()+"\n" == text


@pytest.mark.skip("test_text_language is not implemented yet")
def test_text_language():
    pass


@pytest.mark.skip("test_text_protocols is not implemented yet")
def test_text_protocols():
    pass
