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


def consider_composite(name, code):
    """
    Parses ATF and checks CDLI ID coincides
    """
    afile = AtfFile(sample_file(name))
    assert afile.text.texts[0].code == code


def consider_file(name, code, description):
    """
    Parses ATF and checks CDLI ID and text description coincide
    """
    afile = AtfFile(sample_file(name))
    assert afile.text.code == code
    assert afile.text.description == description


def test_texts():
    """"
    Go through list of selected filenames and check parser deals non-composite
    files.
    """
    for text in texts:
        yield consider_file, text[0], text[1], text[2]


def test_composites():
    """
    Go through list of selected composites and check parser deals with
    composite files correctly
    """
    for composite in composites:
        yield consider_composite, composite[0], composite[1]
