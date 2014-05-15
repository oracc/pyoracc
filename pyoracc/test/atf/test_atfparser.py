# -*- coding: utf-8 -*-

from ...artifact import Artifact
from ...atf.atfyacc import AtfParser
from ...atf.atflex import AtfLexer
from nose.tools import assert_in, assert_equal, assert_is_instance
from itertools import izip,repeat
from fixtures import belsunu

class testParser(object):
  def setUp(self):
    self.lexer=AtfLexer().lexer

  def try_parse(self,content,start):
      self.parser=AtfParser(start=start).parser
      return self.parser.parse(content,lexer=self.lexer)

  def test_code(self):
    artifact=self.try_parse("&X001001 = JCS 48, 089\n","code")
    assert_is_instance(artifact,Artifact)
    assert_equal(artifact.description,"JCS 48, 089")
    assert_equal(artifact.code,"X001001")
