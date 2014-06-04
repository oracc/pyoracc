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
      "&X001001 = JCS 48, 089\n",
      ["AMPERSAND","ID","EQUALS","ID","NEWLINE"],
      [None,"X001001",None,"JCS 48, 089"]
    )

  def test_project(self):
    self.compare_tokens(
      "#project: cams/gkab\n",
      ['HASH',"PROJECT","ID","NEWLINE"],
      [None,None,"cams/gkab",None]
    )

  def test_language_protocol(self):
    self.compare_tokens(
      "#atf: lang akk-x-stdbab\n",
      ["HASH","ATF","LANG","ID","NEWLINE"],
      [None,None,None,"akk-x-stdbab"]
    )

  def test_use_unicode(self):
    self.compare_tokens(
      "#atf: use unicode",
      ["HASH","ATF","USE","UNICODE","NEWLINE"]
    )

  def test_use_unicode(self):
    self.compare_tokens(
      "#atf: use math",
      ["HASH","ATF","USE","MATH","NEWLINE"]
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
      ["HASH","LEM"]+['ID','SEMICOLON']*5+['ID']
    )

  def test_loose_dollar(self):
    self.compare_tokens(
      "$ (a loose dollar line)",
      ["DOLLAR","PARENTHETICALID"],
      [None,"(a loose dollar line)"]
    )

  def test_strict_dollar(self):
    self.compare_tokens(
      "$ reverse blank",
      ["DOLLAR","REFERENCE","BLANK"]
    )

  def test_translation_intro(self):
    self.compare_tokens(
      "@translation parallel en project",
      ["TRANSLATION","ID","ID","PROJECT"]
    )

  def test_translation_text(self):
    self.compare_tokens(
      "@translation parallel en project\n"+
      "1.	Year 63, Ṭebetu (Month X), night of day 2:^1^",
      ["TRANSLATION","ID","ID","PROJECT","NEWLINE","LINELABEL","ID","HAT","ID","HAT"],
      [None,"parallel","en","project",None,
       "1","Year 63, Ṭebetu (Month X), night of day 2:",None,'1',None]
    )

  def test_note_internalflag(self):
    self.compare_tokens(
    "@note Hello James's World",
    ["NOTE","ID"],
    [None,"Hello James's World"]
    )

  def test_note_internalspace(self):
    self.compare_tokens(
    "@note Hello James",
    ["NOTE","ID"],
    [None,"Hello James"]
    )

  def test_note_onechar(self):
    self.compare_tokens(
    "@note H",
    ["NOTE","ID"],
    [None,"H"]
    )

  def test_note_short(self):
    self.compare_tokens(
    "@note I'm",
    ["NOTE","ID"],
    [None,"I'm"]
    )

  def test_division_note(self):
    self.compare_tokens(
      "@note ^1^ A note to the translation.",
      ["NOTE","HAT","ID","HAT","ID","NEWLINE"],
      [None,"1",None,"A note to the translation."]
    )

  def test_division_note(self):
    self.compare_tokens(
      "@tablet\n"+
      "@obverse\n"+
      "3.	U₄!-BI? 20* [(ina)] 9.30 ina(DIŠ) MAŠ₂!(BAR)\n"+
      "#note: Note to line.\n",
      ["TABLET","NEWLINE","OBVERSE","NEWLINE",
      "LINELABEL"]+["ID"]*6+["NEWLINE","HASH","NOTE","ID","NEWLINE"]
    )

  def test_flagged_object(self):
    self.compare_tokens("@object which is remarkable and broken!#\n",
    ["OBJECT","ID","EXCLAIM","HASH"])

  def test_comment(self):
    self.compare_tokens(
      "# I've added various things for test purposes\n",
      []
    )

  def test_ruling(self):
    self.compare_tokens(
      "$ single ruling",
      ["DOLLAR","SINGLE","RULING"]
    )

  def test_described_object(self):
    self.compare_tokens(
      "@object An object that fits no other category\n",
      ["OBJECT","ID","NEWLINE"],
      [None,"An object that fits no other category"]
    )

  def test_nested_object(self):
    self.compare_tokens(
      "@tablet\n"+
      "@obverse\n",
      ["TABLET","NEWLINE","OBVERSE","NEWLINE"]
    )

  def test_object_line(self):
    self.compare_tokens(
      "@tablet\n"+
      "@obverse\n"+
      "1.	[MU] 1.03-KAM {iti}AB GE₆ U₄ 2-KAM\n"
      "#lem: šatti[year]N; n; Ṭebetu[1]MN; mūša[at night]AV; ūm[day]N; n\n",
      ['TABLET','NEWLINE',
       "OBVERSE",'NEWLINE',
       'LINELABEL']+['ID']*6+['NEWLINE','HASH','LEM']+['ID','SEMICOLON']*5+['ID',"NEWLINE"]
    )
