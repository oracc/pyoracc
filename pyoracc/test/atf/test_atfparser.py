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

  def try_parse(self,content,start=None):
      self.parser=AtfParser(start=start).parser
      return self.parser.parse(content,lexer=self.lexer)

  def test_code(self):
    artifact=self.try_parse("&X001001 = JCS 48, 089\n")
    assert_is_instance(artifact,Artifact)
    assert_equal(artifact.description,"JCS 48, 089")
    assert_equal(artifact.code,"X001001")

  def test_artifact_project(self):
    artifact=self.try_parse(
      "&X001001 = JCS 48, 089\n"+
      "#project: cams/gkab\n"
    )
    assert_is_instance(artifact,Artifact)
    assert_equal(artifact.code,"X001001")
    assert_equal(artifact.project,"cams/gkab")

  def test_artifact_language(self):
    artifact=self.try_parse(
      "&X001001 = JCS 48, 089\n"+
      "#atf: lang akk-x-stdbab\n"
    )
    assert_is_instance(artifact,Artifact)
    assert_equal(artifact.code,"X001001")
    assert_equal(artifact.language,"akk-x-stdbab")

  def test_artifact_protocol_language(self):
    artifact=self.try_parse(
      "&X001001 = JCS 48, 089\n"+
      "#project: cams/gkab\n"+
      "#atf: lang akk-x-stdbab\n"
    )
    assert_is_instance(artifact,Artifact)
    assert_equal(artifact.code,"X001001")
    assert_equal(artifact.project,"cams/gkab")
    assert_equal(artifact.language,"akk-x-stdbab")
