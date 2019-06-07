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


from pyoracc.atf.common.atffile import AtfFile
from ..fixtures import anzu, belsunu, sample_file
import pytest
import json


def test_create():
    """
    Parse belsunu.atf and check &-line was parsed correctly
    """
    afile = AtfFile(belsunu())
    assert afile.text.code == "X001001"
    assert afile.text.description == "JCS 48, 089"


def test_composite():
    """
    Parse anzu.atf (composite sample) and check separate text elements were
    parsed correctly
    """
    afile = AtfFile(anzu())
    assert afile.text.texts[0].code == "X002001"
    assert afile.text.texts[0].description == "SB Anzu 1"
    assert afile.text.texts[1].code == "Q002770"
    assert afile.text.texts[1].description == "SB Anzu 2"


# Pairs of filenames and CDLI IDs chosen form composite files
composites = [
    ['SAA19_13', 'P393708'],
    ['SAA19_11', 'P224439'],
    ['SAA17_02', 'P238121'],
    ['SAA17_03', 'P237960'],
    ['SAA18_01', 'P334274'],
    ['5-fm-erimh-p', 'P346083'],
    ['5-fm-emesal-p', 'P228608'],
]

# Triples of ATF filenames, CDLI ID and text designation
texts = [
    ['bb', 'X002002', "BagM Beih. 02, 005"],
    ['bb_2_6', 'X002004', "BagM Beih. 02, 006"],
    ['bb_2_7', 'X002005', "BagM Beih. 02, 007"],
    ['bb_2_10', 'X002006', "BagM Beih. 02, 010"],
    ['bb_2_13', 'X002013', "BagM Beih. 02, 013"],
    ['bb_2_61', 'X002061', "BagM Beih. 02, 061"],
    ['bb_2_062', 'P363326', 'BagM Beih. 02, 062'],
    ['bb_2_79', 'X002079', "BagM Beih. 02, 079"],
    ['bb_2_83', 'X002083', "Bagm Beih. 02, 083"],
    ['bb_2_96', 'X002096', "BagM Beih. 02, 096"],
    # ['cmawro-01-01','Q004184',
    # "MB Boghazkoy Anti-witchcraft Text 1 [CMAwRo 1.1]"],
    ['afo', 'X002003', 'AfO 14, Taf. VI'],
    ['brm_4_6', 'P363407', 'BRM 4, 06'],
    ['brm_4_19', 'P363411', 'BRM 4, 19'],
    ['cm_31_139', 'P415763', 'CM 31, 139'],
    ['ctn_4_006', 'P363421', 'CTN 4, 006'],
    ['Senn2002', 'Q004089', 'Sennacherib 2002'],
    ['Senn0128', 'Q003933', 'Sennacherib 128'],
    ['Esar1014', 'Q003386', 'Esarhaddon 1014'],
    ['Esar0032', 'Q003261', 'Esarhaddon 32'],
    ['UF_10_16', 'P405422', 'UF 10, 16'],
    ['P229574', 'P229574', 'MSL 13, 14 Q1'],
    ['MEE15_54', 'P244115', 'MEE 15, 054'],
    ['BagM_27_217', 'P405130', 'BagM 27 217'],
    ['3-ob-ura2-q-l-t', 'Q000040', 'OB Nippur Ura 2'],
    ['TPIII0001', 'Q003414', 'Tiglath-pileser III 1'],
    ['K_04145F', 'P382580', 'CT 11, pl. 33, K 04145F'],
    ['3-ob-buex-q', 'Q000260', 'OB Sippar Ura I-II']
    ]


@pytest.mark.parametrize('name, code', [
    (text[0], text[1]) for text in composites])
def test_composite_code(name, code):
    """
    Parses ATF and checks CDLI ID coincides.
    """
    afile = AtfFile(sample_file(name))
    assert afile.text.texts[0].code == code


@pytest.mark.parametrize('name, code, description', [
    (text[0], text[1], text[2]) for text in texts])
def test_text_designation(name, code, description):
    """
    Parses ATF and checks CDLI ID and text description coincide.
    """
    afile = AtfFile(sample_file(name))
    assert afile.text.code == code
    assert afile.text.description == description


# ATF filenames which fail the serialization tests.
_xfail_texts = [
    # Multilingual objects store the unmarked language
    # under the `None` key in their `lines` dictionary,
    # which is incompatible with `sort_keys=True`.
    'bb_2_6',
    ]


@pytest.mark.parametrize('name', [
    name if name not in _xfail_texts
    else pytest.param(name, marks=[pytest.mark.xfail()])
    for name in [text[0] for text in texts]])
def test_json_serialization(name):
    """
    Parses ATF and verifies the to_json() method output.
    """
    afile = AtfFile(sample_file(name))
    js = afile.to_json()
    result = json.loads(js)
    assert result
    noskipjs = afile.to_json(skip_empty=False, sort_keys=True)
    result = json.loads(noskipjs)
    assert result
    assert len(noskipjs) >= len(js)
