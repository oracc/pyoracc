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
    text=self.try_parse("&X001001 = JCS 48, 089\n")
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
      "#atf: lang akk-x-stdbab\n"
    )
    assert_is_instance(text,Text)
    assert_equal(text.code,"X001001")
    assert_equal(text.language,"akk-x-stdbab")

  def test_text_protocol_language(self):
    text=self.try_parse(
      "&X001001 = JCS 48, 089\n"+
      "#project: cams/gkab\n"+
      "#atf: lang akk-x-stdbab\n"
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

  def test_substructure(self):
    obj=self.try_parse(
      "@tablet\n"+
      "@obverse"
    )
    assert_is_instance(obj.children[0],OraccObject)
    assert_equal(obj.children[0].objecttype,"obverse")

  def test_triple_substructure(self):
    art=self.try_parse(
      "&X001001 = My Text\n"+
      "@tablet\n"+
      "@obverse"
    )
    assert_is_instance(art.children[0],OraccObject)
    assert_is_instance(art.children[0].children[0],OraccObject)
    assert_equal(art.children[0].children[0].objecttype,"obverse")

  def test_line(self):
    art=self.try_parse(
    "@tablet\n"+
    "@obverse\n"+
    "1.	[MU] 1.03-KAM {iti}AB GE₆ U₄ 2-KAM"
    ##lem: šatti[year]N; n; Ṭebetu[1]MN; mūša[at night]AV; ūm[day]N; n
    )
    assert_equal(len(art.children[0].children[0].words),6)

  def test_line_lemmas(self):
    art=self.try_parse(
    "@tablet\n"+
    "@obverse\n"+
    "1.	[MU] 1.03-KAM {iti}AB GE₆ U₄ 2-KAM\n"
    "#lem: šatti[year]N; n; Ṭebetu[1]MN; mūša[at night]AV; ūm[day]N; n"
    )
    assert_equal(len(art.children[0].children[0].words),6)
    assert_equal(len(art.children[0].children[0].lemmas),6)

  def test_ruling(self):
    art=self.try_parse(
    "@tablet\n"+
    "@obverse\n"+
    "$ triple ruling"
    )
    assert_equal(art.children[0].children[0].count,3)

  def test_comment(self):
    art=self.try_parse(
    "@tablet\n"+
    "@obverse\n"+
    "# A comment"
    )
    assert_equal(len(art.children[0].children),0)

  def test_note(self):
    art=self.try_parse(
    "@tablet\n"+
    "@obverse\n"+
    "3.	U₄!-BI? 20* [(ina)] 9.30 ina(DIŠ) MAŠ₂!(BAR)\n"+
    "#note: Note to line."
    )
    assert_equal(art.children[0].children[0].notes[0],
                "Note to line."
    )
