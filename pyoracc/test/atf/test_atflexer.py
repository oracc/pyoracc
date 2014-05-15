# -*- coding: utf-8 -*-
from unittest import TestCase
from ...atf.atflex import AtfLexer
from nose.tools import assert_in, assert_equal
from itertools import izip,repeat
from fixtures import belsunu

class testLexer(TestCase):
  def setUp(self):
    self.lexer=AtfLexer().lexer

  def compare_tokens(self,content,expected_types,expected_values=None):
    self.lexer.input(content)
    if expected_values==None:
      expected_values=repeat(None)
    for token,expected_type,expected_value in izip(self.lexer,
        expected_types,
        expected_values):
      assert_equal(token.type,expected_type)
      if expected_value:
        assert_equal(token.value,expected_value)

  def test_code(self):
    self.compare_tokens(
      "&X001001 = JCS 48, 089",
      ["CODE","ID"],
      ["X001001","JCS 48, 089"]
    )

  def test_project(self):
    self.compare_tokens(
      "#project: cams/gkab",
      ["PROJECT","ID"],
      [None,"cams/gkab"]
    )

  def test_language_protocol(self):
    self.compare_tokens(
      "#atf: lang akk-x-stdbab",
      ["ATF","LANG","ID"],
      [None,None,"akk-x-stdbab"]
    )

  def test_use_unicode(self):
    self.compare_tokens(
      "#atf: use unicode",
      ["ATF","USE","UNICODE"]
    )

  def test_use_unicode(self):
    self.compare_tokens(
      "#atf: use math",
      ["ATF","USE","MATH"]
    )

  def test_division_tablet(self):
    self.compare_tokens(
      "@tablet",
      ["TABLET"]
    )

  def test_text_linenumber(self):
    self.compare_tokens(
      "1.	[MU] 1.03-KAM {iti}AB GE₆ U₄ 2-KAM",
      ["LINELABEL"]+['ID']*6
    )

  def test_lemmatize(self):
    self.compare_tokens(
      "#lem: šatti[year]N; n; Ṭebetu[1]MN; mūša[at night]AV; ūm[day]N; n",
      ["LEM"]+['ID','ENDLEMMA']*5+['ID']
    )

  def test_loose_dollar(self):
    self.compare_tokens(
      "$ (a loose dollar line)",
      ["DOLLAR","LOOSE"],
      [None,"a loose dollar line"]
    )

  def test_strict_dollar(self):
    self.compare_tokens(
      "$ reverse blank",
      ["DOLLAR","REVERSE","BLANK"]
    )

  def test_translation_intro(self):
    self.compare_tokens(
      "@translation parallel en project",
      ["TRANSLATION","ID","ID","ID"]
    )

  def test_translation_text(self):
    self.compare_tokens(
      "@translation parallel en project\n"+
      "1.	Year 63, Ṭebetu (Month X), night of day 2:^1^",
      ["TRANSLATION","ID","ID","ID","NEWLINE","LINELABEL","ID"],
      [None,"parallel","en","project",None,"1","Year 63, Ṭebetu (Month X), night of day 2:^1^"]
    )

  def test_division_note(self):
    self.compare_tokens(
      "@note ^1^ A note to the translation.",
      ["NOTE","NOTEREF","ID"],
      [None,"1","A note to the translation."]
    )

  def test_comment(self):
    self.compare_tokens(
      "# I've added various things for test purposes",
      ["COMMENT","ID"],
      [None,"I've added various things for test purposes"]
    )

  def test_ruling(self):
    self.compare_tokens(
      "$ single ruling",
      ["DOLLAR","SINGLE","RULING"]
    )
