from ...atf.atffile import AtfFile
from nose.tools import assert_in, assert_equal

from fixtures import belsunu
def test_create():
  afile=AtfFile(belsunu())
  assert_equal(afile.text.code, "X001001")
  assert_equal(afile.text.description, "JCS 48, 089")
