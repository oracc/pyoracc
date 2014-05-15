# -*- coding: utf-8 -*-

from unittest import TestCase

from ...model.text import Text
from ...model.oraccobject import OraccObject
from ...model.oraccnamedobject import OraccNamedObject
from ...atf.atfyacc import AtfParser
from ...atf.atflex import AtfLexer
from nose.tools import assert_in, assert_equal, assert_is_instance
from itertools import izip,repeat
from fixtures import belsunu

class testParser(TestCase):
  def setUp(self):
    self.lexer=AtfLexer().lexer

  def try_parse(self,content):
      self.parser=AtfParser().parser
      return self.parser.parse(content,lexer=self.lexer)

  def test_code(self):
    text=self.try_parse("&X001001 = JCS 48, 089")
    assert_is_instance(text,Text)
    assert_equal(text.description,"JCS 48, 089")
    assert_equal(text.code,"X001001")

  def test_text_project(self):
    text=self.try_parse(
      "&X001001 = JCS 48, 089\n"+
      "#project: cams/gkab\n"
    )
    assert_is_instance(text,Text)
    assert_equal(text.code,"X001001")
    assert_equal(text.project,"cams/gkab")

  def test_text_language(self):
    text=self.try_parse(
      "&X001001 = JCS 48, 089\n"+
      "#atf: lang akk-x-stdbab"
    )
    assert_is_instance(text,Text)
    assert_equal(text.code,"X001001")
    assert_equal(text.language,"akk-x-stdbab")

  def test_text_protocol_language(self):
    text=self.try_parse(
      "&X001001 = JCS 48, 089\n"+
      "#project: cams/gkab\n"+
      "#atf: lang akk-x-stdbab"
    )
    assert_is_instance(text,Text)
    assert_equal(text.code,"X001001")
    assert_equal(text.project,"cams/gkab")
    assert_equal(text.language,"akk-x-stdbab")

  def test_simple_object(self):
    obj=self.try_parse(
      "@tablet\n"
    )
    assert_is_instance(obj,OraccObject)
    assert_equal(obj.objecttype,"tablet")


  def test_generic_object(self):
    obj=self.try_parse(
      "@object That fits no other category\n"
    )
    assert_is_instance(obj,OraccNamedObject)
    assert_equal(obj.objecttype,"object")
    assert_equal(obj.name,"That fits no other category")
