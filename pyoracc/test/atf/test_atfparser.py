# -*- coding: utf-8 -*-

from unittest import TestCase

from ...model.text import Text
from ...model.translation import Translation
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
      "@obverse\n"
    )
    assert_is_instance(obj.children[0],OraccObject)
    assert_equal(obj.children[0].objecttype,"obverse")

  def test_triple_substructure(self):
    art=self.try_parse(
      "&X001001 = My Text\n"+
      "@tablet\n"+
      "@obverse\n"
    )
    assert_is_instance(art.children[0],OraccObject)
    assert_is_instance(art.children[0].children[0],OraccObject)
    assert_equal(art.children[0].children[0].objecttype,"obverse")

  def test_line(self):
    art=self.try_parse(
    "@tablet\n"+
    "@obverse\n"+
    "1.	[MU] 1.03-KAM {iti}AB GE₆ U₄ 2-KAM\n"
    ##lem: šatti[year]N; n; Ṭebetu[1]MN; mūša[at night]AV; ūm[day]N; n
    )
    assert_equal(len(art.children[0].children[0].words),6)

  def test_line_lemmas(self):
    art=self.try_parse(
    "@tablet\n"+
    "@obverse\n"+
    "1.	[MU] 1.03-KAM {iti}AB GE₆ U₄ 2-KAM\n"
    "#lem: šatti[year]N; n; Ṭebetu[1]MN; mūša[at night]AV; ūm[day]N; n\n"
    )
    assert_equal(len(art.children[0].children[0].words),6)
    assert_equal(len(art.children[0].children[0].lemmas),6)

  def test_ruling(self):
    art=self.try_parse(
    "@tablet\n"+
    "@obverse\n"+
    "$ triple ruling\n"
    )
    assert_equal(art.children[0].children[0].count,3)

  def test_comment(self):
    art=self.try_parse(
    "@tablet\n"+
    "@obverse\n"+
    "# A comment\n"
    )
    assert_equal(len(art.children[0].children),0)

  def test_note(self):
    art=self.try_parse(
    "@tablet\n"+
    "@obverse\n"+
    "3.	U₄!-BI? 20* [(ina)] 9.30 ina(DIŠ) MAŠ₂!(BAR)\n"+
    "#note: Note to line.\n"
    )
    assert_equal(art.children[0].children[0].notes[0].content,
                "Note to line."
    )

  def test_loose_dollar(self):
    art=self.try_parse(
    "@tablet\n"+
    "@obverse\n"+
    "3.	U₄!-BI? 20* [(ina)] 9.30 ina(DIŠ) MAŠ₂!(BAR)\n"+
    "$ (something loose)\n"
    )
    assert_equal(art.children[0].children[1].loose,
                "(something loose)"
    )

  def test_strict_dollar_simple(self):
    art=self.try_parse(
    "@tablet\n"+
    "@obverse\n"+
    "$case blank\n"
    )
    assert_equal(art.children[0].children[0].state,"blank")
    assert_equal(art.children[0].children[0].scope,"case")

  def test_strict_dollar_plural_difficult(self):
    art=self.try_parse(
    "@tablet\n"+
    "@obverse\n"+
    "$5-7 lines blank\n"
    )
    assert_equal(art.children[0].children[0].state,"blank")
    assert_equal(art.children[0].children[0].scope,"lines")
    assert_equal(art.children[0].children[0].extent,"5-7")

  def test_strict_dollar_singular_difficult(self):
    art=self.try_parse(
    "@tablet\n"+
    "@obverse\n"+
    "$rest of bulla blank\n"
    )
    assert_equal(art.children[0].children[0].state,"blank")
    assert_equal(art.children[0].children[0].scope,"bulla")
    assert_equal(art.children[0].children[0].extent,"rest of")

  def test_strict_dollar_plural_qualified(self):
    art=self.try_parse(
    "@tablet\n"+
    "@obverse\n"+
    "$at most 5 columns blank\n"
    )
    assert_equal(art.children[0].children[0].state,"blank")
    assert_equal(art.children[0].children[0].scope,"columns")
    assert_equal(art.children[0].children[0].extent,"5")
    assert_equal(art.children[0].children[0].qualification,"at most")

  def test_strict_dollar_labelled(self):
    art=self.try_parse(
    "@tablet\n"+
    "@obverse\n"+
    "$rest of column 1 blank\n"
    )
    assert_equal(art.children[0].children[0].state,"blank")
    assert_equal(art.children[0].children[0].scope,"column 1")
    assert_equal(art.children[0].children[0].extent,"rest of")

  def test_translation_intro(self):
    art=self.try_parse(
      "@tablet\n"+
      "@translation parallel en project\n"
    )
    assert_is_instance(art.children[0],Translation)

  def test_translation_text(self):
    art=self.try_parse(
      "@tablet\n"+
      "@translation parallel en project\n"+
      "@obverse\n"
      "1.	Year 63, Ṭebetu (Month X), night of day 2\n"
    )
    assert_is_instance(art.children[0],Translation)
    assert_equal(art.children[0].children[0].children[0].label,'1')
    assert_equal(art.children[0].children[0].children[0].words[0],
      "Year 63, Ṭebetu (Month X), night of day 2")

  def test_translation_links(self):
    art=self.try_parse(
      "@tablet\n"+
      "@translation parallel en project\n"+
      "@obverse\n"
      "1.	Year 63, Ṭebetu (Month X), night of day 2:^1^\n\n"
      "@note ^1^ A note to the translation.\n"
    )
    assert_is_instance(art.children[0],Translation)
    assert_equal(art.children[0].children[0].children[0].label,'1')
    assert_equal(art.children[0].children[0].children[0].words[0],
      "Year 63, Ṭebetu (Month X), night of day 2:")
    assert_equal(art.children[0].children[0].children[0].references[0],
      "1")
    assert_equal(art.children[0].children[0].children[0].notes[0].references[0],
      "1")
