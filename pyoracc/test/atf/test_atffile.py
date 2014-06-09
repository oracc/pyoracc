from ...atf.atffile import AtfFile
from nose.tools import assert_in, assert_equal

from ..fixtures import anzu, belsunu


def test_create():
    afile = AtfFile(belsunu())
    assert_equal(afile.text.code, "X001001")
    assert_equal(afile.text.description, "JCS 48, 089")

def test_composite():
    afile = AtfFile(anzu())
    assert_equal(afile.text.texts[0].code, "Q002769")
    assert_equal(afile.text.texts[0].description, "SB Anzu 1")
    assert_equal(afile.text.texts[1].code, "Q002770")
    assert_equal(afile.text.texts[1].description, "SB Anzu 2")
