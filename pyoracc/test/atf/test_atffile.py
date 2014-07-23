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


def test_bb_2():
    afile = AtfFile(sample_file("bb"))
    assert_equal(afile.text.code, "X002002")
    assert_equal(afile.text.description, "BagM Beih. 02, 005")

def test_bb_2_6():
    afile = AtfFile(sample_file("bb_2_6"))
    assert_equal(afile.text.code, "X002004")
    assert_equal(afile.text.description, "BagM Beih. 02, 006")

def test_bb_2_7():
    afile = AtfFile(sample_file("bb_2_7"))
    assert_equal(afile.text.code, "X002005")
    assert_equal(afile.text.description, "BagM Beih. 02, 007")

def test_bb_2_10():
    afile = AtfFile(sample_file("bb_2_10"))
    assert_equal(afile.text.code, "X002006")
    assert_equal(afile.text.description, "BagM Beih. 02, 010")

def test_bb_2_13():
    afile = AtfFile(sample_file("bb_2_13"))
    assert_equal(afile.text.code, "X002013")
    assert_equal(afile.text.description, "BagM Beih. 02, 013")


def test_afo():
    afile = AtfFile(sample_file("afo"))
    assert_equal(afile.text.code, "X002003")
