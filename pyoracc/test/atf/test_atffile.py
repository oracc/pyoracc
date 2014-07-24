from ...atf.atffile import AtfFile
from nose.tools import assert_in, assert_equal

from ..fixtures import anzu, belsunu, sample_file


def test_create():
    afile = AtfFile(belsunu())
    assert_equal(afile.text.code, "X001001")
    assert_equal(afile.text.description, "JCS 48, 089")


def test_composite():
    afile = AtfFile(anzu())
    assert_equal(afile.text.texts[0].code, "X002001")
    assert_equal(afile.text.texts[0].description, "SB Anzu 1")
    assert_equal(afile.text.texts[1].code, "Q002770")
    assert_equal(afile.text.texts[1].description, "SB Anzu 2")


def consider_file(name,code,description):
    afile = AtfFile(sample_file(name))
    assert_equal(afile.text.code, code)
    assert_equal(afile.text.description,description)

texts=[
    ['bb','X002002',"BagM Beih. 02, 005"],
    ['bb_2_6','X002004',"BagM Beih. 02, 006"],
    ['bb_2_7','X002005',"BagM Beih. 02, 007"],
    ['bb_2_10','X002006',"BagM Beih. 02, 010"],
    ['bb_2_13','X002013',"BagM Beih. 02, 013"],
    ['bb_2_61','X002061',"BagM Beih. 02, 061"],
    ['bb_2_79','X002079',"BagM Beih. 02, 079"],
    ['bb_2_83','X002083',"Bagm Beih. 02, 083"],
    ['bb_2_96','X002096',"BagM Beih. 02, 096"],
    ['afo','X002003','AfO 14, Taf. VI'],
    ['brm_4_6','P363407','BRM 4, 06']        
    ]

def test_texts():
    for text in texts:
        consider_file(*text)