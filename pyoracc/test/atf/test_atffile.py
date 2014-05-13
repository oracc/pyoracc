from ...atf.atffile import AtfFile
from nose.tools import assert_in

from fixtures import belsunu
def test_create():
  afile=AtfFile(belsunu())
  assert_in("X001001",afile.content)
