# -*- coding: utf-8 -*-
'''
Copyright 2015, 2016 University College London.

This file is part of PyORACC.

PyORACC is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyORACC is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyORACC. If not, see <http://www.gnu.org/licenses/>.
'''


import pytest

from pyoracc.atf.common.atflex import AtfLexer
from pyoracc.atf.common.atfyacc import AtfParser
from ...model.comment import Comment
from ...model.composite import Composite
from ...model.line import Line
from ...model.link import Link
from ...model.link_reference import LinkReference
from ...model.milestone import Milestone
from ...model.multilingual import Multilingual
from ...model.oraccnamedobject import OraccNamedObject
from ...model.oraccobject import OraccObject
from ...model.ruling import Ruling
from ...model.score import Score
from ...model.state import State
from ...model.text import Text
from ...model.translation import Translation


def try_parse(content):
    if content[-1] != '\n':
        content += "\n"
    lexer = AtfLexer().lexer
    parser = AtfParser().parser
    return parser.parse(content, lexer=lexer)


def test_code():
    text = try_parse("&X001001 = JCS 48, 089\n")
    assert isinstance(text, Text)
    assert text.description == "JCS 48, 089"
    assert text.code == "X001001"


def test_text_project():
    text = try_parse(
        "&X001001 = JCS 48, 089\n" +
        "#project: cams/gkab\n"
    )
    assert isinstance(text, Text)
    assert text.code == "X001001"
    assert text.project == "cams/gkab"


def test_text_language():
    text = try_parse(
        "&X001001 = JCS 48, 089\n" +
        "#atf: lang akk-x-stdbab\n"
    )
    assert isinstance(text, Text)
    assert text.code == "X001001"
    assert text.language == "akk-x-stdbab"


@pytest.mark.skip('Parser has no support for the key protocol.')
def test_key_protocol():
    text = try_parse(
        "&X001001 = JCS 48, 089\n" +
        "#key: cdli=ND 02688\n"
    )
    assert isinstance(text, Text)


@pytest.mark.skip('Parser has no support for the key protocol.')
def test_double_equals_in_key_protocol():
    text = try_parse(
        "&X001001 = JCS 48, 089\n" +
        "#key: musno=Ki 1904-10-9,049 = BM 099020\n"
    )
    assert isinstance(text, Text)


@pytest.mark.skip('Parser has no support for the key protocol.')
def test_many_equals_in_key_protocol():
    text = try_parse(
        "&X001001 = JCS 48, 089\n" +
        "#key: musno=VAT 10433 (= Ass 04691 = NARGD 30)\n"
    )
    assert isinstance(text, Text)


@pytest.mark.skip('Parser has no support for the key protocol.')
def test_empty_key_in_key_protocol():
    text = try_parse(
        "&X001001 = JCS 48, 089\n" +
        "#key: date=\n"
    )
    assert isinstance(text, Text)


@pytest.mark.skip('Parser has no support for the mylines protocol.')
def test_mylines_protocol():
    text = try_parse(
        "&X001001 = JCS 48, 089\n" +
        "#atf: use mylines\n"
    )
    assert isinstance(text, Text)


@pytest.mark.skip('Parser has no support for the lexical protocol.')
def test_lexical_protocol():
    text = try_parse(
        "&X001001 = JCS 48, 089\n" +
        "#atf: use lexical\n"
    )
    assert isinstance(text, Text)


@pytest.mark.skip('Parser has no support for the lemmatizer protocol.')
def test_lemmatizer_protocol():
    text = try_parse(
        "&X001001 = JCS 48, 089\n" +
        "#lemmatizer: sparse do sv sn eq tx\n"
    )
    assert isinstance(text, Text)


def test_text_protocol_language():
    text = try_parse(
        "&X001001 = JCS 48, 089\n" +
        "#project: cams/gkab\n" +
        "#atf: lang akk-x-stdbab\n"
    )
    assert isinstance(text, Text)
    assert text.code == "X001001"
    assert text.project == "cams/gkab"
    assert text.language == "akk-x-stdbab"


@pytest.mark.parametrize('mode', [
    'matrix parsed word',
    'matrix parsed',
    'matrix unparsed',
    'synoptic parsed',
    'synoptic unparsed',
])
def test_score(mode):
    obj = try_parse(
        "&Q004184 = MB Boghazkoy Anti-witchcraft Text 1 [CMAwRo 1.1]\n" +
        "@score " + mode + "\n" +
        "#project: cmawro\n"
    )
    assert isinstance(obj, Text)
    assert isinstance(obj.score, Score)
    keys = mode.split()
    expected_type = 'matrix' if 'matrix' in keys else 'synoptic'
    expected_mode = 'parsed' if 'parsed' in keys else 'unparsed'
    expected_word = 'word' in keys
    assert obj.score.ttype == expected_type
    assert obj.score.mode == expected_mode
    assert obj.score.word == expected_word


def test_simple_object():
    obj = try_parse(
        "@tablet\n"
    )
    assert isinstance(obj, OraccObject)
    assert obj.objecttype == "tablet"


def test_generic_object():
    obj = try_parse(
        "@object That fits no other category\n"
    )
    assert isinstance(obj, OraccNamedObject)
    assert obj.objecttype == "object"
    assert obj.name == "That fits no other category"


def test_flagged_object_broken_remark():
    obj = try_parse(
        "@object which is remarkable and broken!#\n"
    )
    assert isinstance(obj, OraccNamedObject)
    assert obj.objecttype == "object"
    assert obj.name == "which is remarkable and broken"
    assert(obj.broken)
    assert(obj.remarkable)
    assert(not obj.collated)


def test_flagged_object_collated():
    obj = try_parse(
        "@tablet\n@column 2'*\n"
    )
    assert isinstance(obj.children[0], OraccNamedObject)
    assert obj.children[0].objecttype == "column"
    assert obj.children[0].name == "2'"
    assert(obj.children[0].collated)
    assert(not obj.children[0].broken)


def test_substructure():
    obj = try_parse(
        "@tablet\n" +
        "@obverse\n"
    )
    assert isinstance(obj.children[0], OraccObject)
    assert obj.children[0].objecttype == "obverse"


def test_substructure_sealing():
    obj = try_parse(
        "@sealings\n" +
        "@top\n"
    )
    assert isinstance(obj, OraccObject)
    assert obj.objecttype == "sealings"
    assert isinstance(obj.children[0], OraccObject)
    assert obj.children[0].objecttype == "top"


def test_triple_substructure():
    art = try_parse(
        "&X001001 = My Text\n" +
        "@tablet\n" +
        "@obverse\n"
    )
    assert isinstance(art, Text)
    assert isinstance(art.children[0], OraccObject)
    assert isinstance(art.children[0].children[0], OraccObject)
    assert art.children[0].children[0].objecttype == "obverse"


def test_two_surfaces():
    art = try_parse(
        "&X001001 = My Text\n" +
        "@tablet\n" +
        "@obverse\n" +
        "@reverse\n"
    )
    assert isinstance(art, Text)
    assert isinstance(art.children[0], OraccObject)
    assert isinstance(art.children[0].children[0], OraccObject)
    assert art.children[0].children[0].objecttype == "obverse"
    assert art.children[0].children[1].objecttype == "reverse"


def test_two_inscribed_surfaces():
    art = try_parse(
        "&X001001 = My Text\n" +
        "@tablet\n" +
        "@obverse\n" +
        "1. line one\n" +
        "@reverse\n" +
        "2. line two\n"
    )
    assert isinstance(art, Text)
    assert isinstance(art.children[0], OraccObject)
    assert isinstance(art.children[0].children[0], OraccObject)
    assert art.children[0].children[0].objecttype == "obverse"
    assert art.children[0].children[1].objecttype == "reverse"
    assert isinstance(art.children[0].children[0].children[0], Line)
    assert isinstance(art.children[0].children[1].children[0], Line)


def test_score_simple():
    art = try_parse(
        "&X001001 = My Text\n" +
        "@score matrix parsed\n" +
        "@tablet\n" +
        "@obverse\n" +
        "1. line one\n" +
        "A₁_obv_i_4′: line one again\n"
    )
    assert isinstance(art, Text)
    assert isinstance(art.score, Score)
    assert isinstance(art.children[0], OraccObject)
    assert isinstance(art.children[0].children[0], OraccObject)
    assert art.children[0].children[0].objecttype == "obverse"
    assert isinstance(art.children[0].children[0].children[0], Line)
    assert isinstance(art.children[0].children[0].children[1], Line)
    assert art.children[0].children[0].children[1].words == \
        'line one again'.split()


def test_complex_substructure():
    art = try_parse(
        "&X001001 = My Text\n" +
        "@tablet\n" +
        "@obverse\n" +
        "1. Line one\n" +
        "2. Line two\n" +
        "#lem: line; two\n"
        "@reverse\n" +
        "3. Line three\n" +
        "#lem: line; three\n" +
        "#note: Note to line three\n" +
        "@object case\n" +
        "@obverse\n" +
        "4. Line four\n"
    )
    assert isinstance(art, Text)
    tablet = art.children[0]
    assert isinstance(tablet, OraccObject)
    case = art.children[1]
    assert len(art.children) == 2
    obverse = tablet.children[0]
    assert isinstance(obverse, OraccObject)
    reverse = tablet.children[1]
    assert len(tablet.children) == 2
    caseobverse = case.children[0]
    assert len(case.children) == 1
    lines = (obverse.children[:] +
             reverse.children[:] +
             caseobverse.children[:])
    assert len(lines) == 4
    assert lines[1].lemmas[1] == "two"
    assert lines[2].notes[0].content == "Note to line three"


def test_complex_substructure_2():
    art = try_parse(
        "&X001001 = My Text\n" +
        "@obverse\n" +
        "1. Line one\n" +
        "2. Line two\n" +
        "#lem: line; two\n" +
        "@bottom\n" +
        "3. Line three)\n" +
        "@reverse\n" +
        "4. Line four\n" +
        "#lem: line; three\n" +
        "#note: Note to line four\n" +
        "@translation labeled en project\n" +
        "@(1) Line one\n\n"
    )
    assert isinstance(art, Text)
    tablet = art.children[0]
    assert isinstance(tablet, OraccObject)
    assert len(art.children) == 1
    obverse = tablet.children[0]
    assert isinstance(obverse, OraccObject)
    reverse = tablet.children[2]
    assert len(tablet.children) == 4
    bottom = tablet.children[1]
    # Is this wrong -- should tops and bottoms
    # really be a lower nesting level?
    translation = tablet.children[3]
    lines = (obverse.children[:] +
             bottom.children[:] +
             reverse.children[:])
    assert len(lines) == 4
    assert lines[1].lemmas[1] == "two"
    assert lines[3].notes[0].content == "Note to line four"
    assert isinstance(translation, Translation)


def test_line():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "1.    [MU] 1.03-KAM {iti}AB GE₆ U₄ 2-KAM\n"
    )
    assert len(art.children[0].children[0].words) == 6


@pytest.mark.skip("Parser has no support for the '={' annotation.")
def test_line_equalsbrace():
    # This seems to be used to mark interlinear glosses
    # in the original text.
    art = try_parse(
        "@tablet\n" +
        "@reverse\n" +
        "2'.    ITI# an-ni-u2#\n" +
        "={    ur-hu\n"
    )
    assert isinstance(art, OraccObject)
    assert len(art.children[0].children[0].words) == 2


def test_line_lemmas():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "1.    [MU] 1.03-KAM {iti}AB GE₆ U₄ 2-KAM\n"
        "#lem: šatti[year]N; n; Ṭebetu[1]MN; " +
        "mūša[at night]AV; ūm[day]N; n\n"
    )
    assert len(art.children[0].children[0].words) == 6
    assert len(art.children[0].children[0].lemmas) == 6


def test_empty_lemma():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "1.    [MU] 1.03-KAM {iti}AB GE₆ U₄ 2-KAM\n"
        "#lem: šatti[year]N; ; Ṭebetu[1]MN; " +
        "mūša[at night]AV; ūm[day]N; n\n"
    )
    assert len(art.children[0].children[0].words) == 6
    assert len(art.children[0].children[0].lemmas) == 6


def test_ruling():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "$ triple ruling\n"
    )
    assert art.children[0].children[0].count == 3


def test_flagged_ruling():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "$ ruling!\n"
    )
    assert art.children[0].children[0].remarkable is True


def test_uncounted_ruling():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "$ ruling\n"
    )
    assert art.children[0].children[0].count == 1


def test_line_ruling():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "$ double line ruling\n"
    )
    assert art.children[0].children[0].count == 2


def test_ruling_on_object_no_surface():
    art = try_parse(
        "@tablet\n" +
        "$ single ruling\n",
    )
    # Should default to an obverse surface
    assert art.children[0].objecttype == "obverse"
    assert art.children[0].children[0].count == 1


def test_link_on_surface_not_line():
    art = try_parse(
        "@tablet\n" +
        "4'. zal-bi a-ri-[a]\n" +
        "$single ruling\n" +
        ">> A Seg.2, 33\n"
    )
    obverse = art.children[0]
    assert isinstance(obverse.children[0], Line)
    assert isinstance(obverse.children[1], Ruling)
    assert isinstance(obverse.children[2], LinkReference)


def test_ruling_on_labeled_translation():
    art = try_parse(
        "@tablet\n" +
        "@translation labeled en project\n" +
        "$ single ruling\n" +
        "@label 1\n" +
        "Some content\n\n"
    )
    # Should default to an obverse surface
    assert isinstance(art.children[0].children[0], State)


def test_comment():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "# A comment\n"
    )
    assert isinstance(art.children[0].children[0], Comment)


def test_check():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "#CHECK: A worry\n"
    )
    comment = art.children[0].children[0]
    assert isinstance(comment, Comment)
    assert comment.check is True


def test_note():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "3.    U₄!-BI? 20* [(ina)] 9.30 ina(DIŠ) MAŠ₂!(BAR)\n" +
        "#note: Note to line.\n"
    )
    assert art.children[0].children[0].notes[0].content == "Note to line."


def test_surface_note():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "#note: Note to surface.\n"
    )
    assert art.children[0].children[0].content == "Note to surface."


def test_dollar_unquantified_reverse():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "3.    U₄!-BI? 20* [(ina)] 9.30 ina(DIŠ) MAŠ₂!(BAR)\n" +
        "$ missing lines\n"
    )
    assert art.children[0].children[1].state == "missing"
    assert art.children[0].children[1].scope == "lines"


def test_dollar_unquantified():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "3.    U₄!-BI? 20* [(ina)] 9.30 ina(DIŠ) MAŠ₂!(BAR)\n" +
        "$ columns broken\n"
    )
    assert art.children[0].children[1].state == "broken"
    assert art.children[0].children[1].scope == "columns"


def test_loose_dollar():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "3.    U₄!-BI? 20* [(ina)] 9.30 ina(DIŠ) MAŠ₂!(BAR)\n" +
        "$ (something loose)\n"
    )
    assert art.children[0].children[1].loose == "(something loose)"


def test_strict_dollar_single_reverse():
    """Test that reverse $ line is working correctly as in
        p_state_singular_desc"""
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "$ blank line\n"
    )
    assert art.children[0].children[0].state == "blank"
    assert art.children[0].children[0].scope == "line"


def test_strict_dollar_simple():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "$case blank\n"
    )
    assert art.children[0].children[0].state == "blank"
    assert art.children[0].children[0].scope == "case"


def test_strict_dollar_simple_space():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "$space blank\n"
    )
    assert art.children[0].children[0].state == "blank"
    assert art.children[0].children[0].scope == "space"


def test_strict_dollar_plural_difficult():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "$5-7 lines blank\n"
    )
    assert art.children[0].children[0].state == "blank"
    assert art.children[0].children[0].scope == "lines"
    assert art.children[0].children[0].extent == "5-7"


def test_strict_dollar_in_lines():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "48.   lip#-tar-rik ina at-ma-ni šu-bat ki#-[iṣ-ṣi]\n" +
        "$ 3 lines broken\n" +
        "53.   ta#-[mit] iq#-bu-šu DINGIR an-[na i-pu-ul]\n"
    )
    content = art.children[0].children
    assert isinstance(content[0], Line)
    assert isinstance(content[2], Line)
    assert content[1].state == "broken"
    assert content[1].scope == "lines"
    assert content[1].extent == "3"


def test_strict_dollar_singular_difficult():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "$rest of bulla blank\n"
    )
    assert art.children[0].children[0].state == "blank"
    assert art.children[0].children[0].scope == "bulla"
    assert art.children[0].children[0].extent == "rest of"


def test_strict_dollar_plural_qualified():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "$at most 5 columns blank\n"
    )
    assert art.children[0].children[0].state == "blank"
    assert art.children[0].children[0].scope == "columns"
    assert art.children[0].children[0].extent == "5"
    assert art.children[0].children[0].qualification == "at most"


def test_strict_dollar_labelled():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "$rest of column 1 blank\n"
    )
    assert art.children[0].children[0].state == "blank"
    assert art.children[0].children[0].scope == "column 1"
    assert art.children[0].children[0].extent == "rest of"


def test_strict_dollar_no_scope():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "$rest blank\n"
    )
    assert art.children[0].children[0].state == "blank"
    assert art.children[0].children[0].scope is None
    assert art.children[0].children[0].extent == "rest"


def test_strict_dollar_singular_exception():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "$ 1 line traces\n"
    )
    dollar = art.children[0].children[0]
    assert dollar.state == "traces"
    assert dollar.scope == "line"
    assert dollar.extent == "1"


def test_strict_dollar_start_of_exception():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "$ start of column missing\n",
    )
    assert art.children[0].children[0].state == "missing"
    assert art.children[0].children[0].scope == "column"
    assert art.children[0].children[0].extent == "start of"


def test_strict_dollar_lacuna_exception():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "$ Lacuna\n",
    )
    assert art.children[0].children[0].state == "Lacuna"
    assert art.children[0].children[0].scope is None
    assert art.children[0].children[0].extent is None


def test_strict_dollar_simple_exception():
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "$ broken\n",
    )
    assert art.children[0].children[0].state == "broken"
    assert art.children[0].children[0].scope is None
    assert art.children[0].children[0].extent is None


@pytest.mark.xfail
def test_loose_recovery():
    # Users often put a loose dollar without the brackets
    # We should define a parser fallback to accommodate this
    # And recover.
    art = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "$ traces of 2 erased lines\n" +
        "1. Hello\n",
    )
    assert art.children[0].children[0].label == '1'


def test_strict_as_loose_in_translation():
    art = try_parse(
        "@tablet\n" +
        "@translation parallel en project\n" +
        "$ Continued in text no. 2\n"
    )
    assert isinstance(art.children[0].children[0], State)


def test_translation_intro():
    art = try_parse(
        "@tablet\n" +
        "@translation parallel en project\n"
    )
    assert isinstance(art.children[0], Translation)


def test_translation_text():
    art = try_parse(
        "@tablet\n" +
        "@translation parallel en project\n" +
        "@obverse\n"
        "1.    Year 63, Ṭebetu (Month X), night of day 2\n"
    )
    assert isinstance(art.children[0], Translation)
    assert art.children[0].children[0].children[0].label == '1'
    assert art.children[0].children[0].children[0].words[0] == \
        "Year 63, Ṭebetu (Month X), night of day 2"


def test_translation_eneded():
    art = try_parse(
        "@tablet\n" +
        "@translation labeled en project\n" +
        "@(1) Year 63, Ṭebetu (Month X), night of day 2\n" +
        "@end translation\n"
    )
    assert isinstance(art.children[0], Translation)
    assert art.children[0].children[0].label.label == ['1']
    assert art.children[0].children[0].words[0] == \
        "Year 63, Ṭebetu (Month X), night of day 2"


def test_translation_labeled_text():
    art = try_parse(
        "@tablet\n" +
        "@translation labeled en project\n" +
        "@label o 4\n"
        "Then it will be taken for the rites and rituals.\n\n"
    )
    assert isinstance(art.children[0], Translation)
    assert art.children[0].children[0].label.label == ['o', '4']
    assert art.children[0].children[0].words[0] == \
        "Then it will be taken for the rites and rituals."


def test_translation_labeled_long():
    art = try_parse(
        "@tablet\n" +
        "@translation labeled en project\n" +
        "@label obverse 4\n"
        "Then it will be taken for the rites and rituals.\n\n"
    )
    assert isinstance(art.children[0], Translation)
    assert art.children[0].children[0].label.label == ['obverse', '4']
    assert art.children[0].children[0].words[0] == \
        "Then it will be taken for the rites and rituals."


def test_translation_labeled_text2():
    art = try_parse(
        "@tablet\n" +
        "@translation labeled en project\n" +
        "@label o 2 - o 3\n" +
        "an expert will carefully inspect an ungelded bull.\n\n")
    assert isinstance(art.children[0], Translation)
    assert art.children[0].children[0].label.label == ['o', '2']
    assert art.children[0].children[0].label.rangelabel == ['o', '3']
    assert art.children[0].children[0].words[0] == \
        "an expert will carefully inspect an ungelded bull."


def test_translation_label_plus():
    art = try_parse(
        "@tablet\n" +
        "@translation labeled en project\n" +
        "@label+ o 28\n" +
        "You extinguish the fire on the altar with beer\n\n"
    )
    assert(art.children[0].children[0].label.plus)


def test_translation_labeled_dashlabel():
    art = try_parse(
        "@tablet\n" +
        "@translation labeled en project\n" +
        "@label o 14-15 - o 20\n" +
        "You strew all (kinds of) seed.\n\n",
    )
    assert isinstance(art.children[0], Translation)
    assert art.children[0].children[0].label.label == ['o', '14-15']
    assert art.children[0].children[0].label.rangelabel == ['o', '20']
    assert art.children[0].children[0].words[0] == \
        "You strew all (kinds of) seed."


def test_translation_labeled_noted_text():
    art = try_parse(
        "@tablet\n" +
        "@translation labeled en project\n" +
        "@label r 8\n" +
        "The priest says the gods have performed these actions. ^1^\n\n" +
        "@note ^1^ Parenthesised text follows Neo-Assyrian source\n"
    )
    assert isinstance(art.children[0], Translation)
    assert art.children[0].children[0].label.label == ['r', '8']
    assert art.children[0].children[0].words[0] == \
        "The priest says the gods have performed these actions."
    assert art.children[0].children[0].references[0] == "1"
    assert art.children[0].children[0].notes[0].references[0] == "1"
    assert art.children[0].children[0].notes[0].content == \
        "Parenthesised text follows Neo-Assyrian source"


def test_translation_links():
    art = try_parse(
        "@tablet\n" +
        "@translation parallel en project\n" +
        "@obverse\n"
        "1.    Year 63, Ṭebetu (Month X), night of day 2:^1^\n\n"
        "@note ^1^ A note to the translation.\n"
    )
    assert isinstance(art.children[0], Translation)
    assert art.children[0].children[0].children[0].label == '1'
    assert art.children[0].children[0].children[0].words[0] == \
        "Year 63, Ṭebetu (Month X), night of day 2:"
    assert art.children[0].children[0].children[0].references[0] == "1"
    assert \
        art.children[0].children[0].children[0].notes[0].references[0] == \
        "1"


def test_translation_poundnote():
    art = try_parse(
        "@tablet\n" +
        "@translation parallel en project\n" +
        "@obverse\n"
        "1.    Year 63, Ṭebetu (Month X), night of day 2\n"
        "#note: A note to the translation.\n"
    )
    assert art.children[0].children[0].children[0].notes[0].content == \
        "A note to the translation."


def test_translation_labeled_atlabel():
    art = try_parse(
        "@tablet\n" +
        "@translation labeled en project\n" +
        "@(o 20) You strew all (kinds of) seed.\n" +
        "@(o i 2) No-one will occupy the king of Akkad's throne.\n")
    l1 = art.children[0].children[0]
    assert l1.label.label == ["o", "20"]
    assert l1.words[0] == "You strew all (kinds of) seed."
    l2 = art.children[0].children[1]
    assert l2.label.label == ["o", "i", "2"]
    assert l2.words[0] == "No-one will occupy the king of Akkad's throne."


def test_translation_labeled_multiline_atlabel():
    art = try_parse(
        "@tablet\n" +
        "@translation labeled en project\n" +
        "@(o 20) He fled like a fox to the land\n" +
        "Elam.\n")
    l1 = art.children[0].children[0]
    assert l1.label.label == ["o", "20"]
    assert "\n".join(l1.words) == "He fled like a fox to the land\nElam."


def test_default_surface():
    text = try_parse(
        "&Q002769 = SB Anzu 1\n" +
        "@tablet\n" +
        "1.   bi#-in šar da-ad-mi šu-pa-a na-ram {d}ma#-mi\n"
    )
    assert text.children[0].objecttype == "tablet"
    assert text.children[0].children[0].objecttype == "obverse"


def test_default_object():
    text = try_parse(
        "&Q002769 = SB Anzu 1\n" +
        "@obverse\n" +
        "1.   bi#-in šar da-ad-mi šu-pa-a na-ram {d}ma#-mi\n"
    )
    assert text.children[0].objecttype == "tablet"
    assert text.children[0].children[0].objecttype == "obverse"


def test_default_object_surface():
    text = try_parse(
        "&Q002769 = SB Anzu 1\n" +
        "1.   bi#-in šar da-ad-mi šu-pa-a na-ram {d}ma#-mi\n"
    )
    assert text.children[0].objecttype == "tablet"
    assert text.children[0].children[0].objecttype == "obverse"


def test_default_object_surface_dollar():
    text = try_parse(
        "&Q002769 = SB Anzu 1\n" +
        "$ 5 lines broken\n"
    )
    assert text.children[0].objecttype == "tablet"
    assert text.children[0].children[0].objecttype == "obverse"
    assert isinstance(text.children[0].children[0].children[0], State)


def test_default_surface_dollar():
    text = try_parse(
        "&Q002769 = SB Anzu 1\n" +
        "@tablet\n" +
        "$ 5 lines broken\n"
    )
    assert text.children[0].objecttype == "tablet"
    assert text.children[0].children[0].objecttype == "obverse"
    assert isinstance(text.children[0].children[0].children[0], State)


def test_default_object_dollar():
    text = try_parse(
        "&Q002769 = SB Anzu 1\n" +
        "@obverse\n" +
        "$ 5 lines broken\n"
    )
    assert text.children[0].objecttype == "tablet"
    assert text.children[0].children[0].objecttype == "obverse"
    assert isinstance(text.children[0].children[0].children[0], State)


def test_composite():
    composite = try_parse(
        "&Q002769 = SB Anzu 1\n" +
        "@composite\n" +
        "#project: cams/gkab\n" +
        "1.   bi#-in šar da-ad-mi šu-pa-a na-ram {d}ma#-mi\n" +
        "&Q002770 = SB Anzu 2\n" +
        "#project: cams/gkab\n" +
        "1.   bi-riq ur-ha šuk-na a-dan-na\n"
    )
    assert isinstance(composite, Composite)
    assert isinstance(composite.texts[0], Text)
    assert isinstance(composite.texts[1], Text)


def test_implicit_composite():
    composite = try_parse(
        "&Q002769 = SB Anzu 1\n" +
        "#project: cams/gkab\n" +
        "1.   bi#-in šar da-ad-mi šu-pa-a na-ram {d}ma#-mi\n" +
        "&Q002770 = SB Anzu 2\n" +
        "#project: cams/gkab\n" +
        "1.   bi-riq ur-ha šuk-na a-dan-na\n"
    )
    assert isinstance(composite, Composite)
    assert isinstance(composite.texts[0], Text)
    assert isinstance(composite.texts[1], Text)


def test_translated_composite():
    composite = try_parse(
        "&Q002769 = SB Anzu 1\n" +
        "#project: cams/gkab\n" +
        "1.   bi#-in šar da-ad-mi šu-pa-a na-ram {d}ma#-mi\n" +
        "@translation labeled en project\n"
        "@(1) This is English\n\n\n"
        "&Q002770 = SB Anzu 2\n" +
        "#project: cams/gkab\n" +
        "1.   bi-riq ur-ha šuk-na a-dan-na\n"
    )
    assert isinstance(composite, Composite)
    assert isinstance(composite.texts[0], Text)
    assert isinstance(composite.texts[1], Text)


def test_link_declaration():
    text = try_parse(
        "&Q002769 = SB Anzu 1\n" +
        "#link: def A = P363716 = TCL 06, 44\n" +
        "@tablet\n" +
        "1. Some text\n"
    )
    link = text.links[0]
    assert isinstance(link, Link)
    assert link.label == "A"
    assert link.code == "P363716"
    assert link.description == "TCL 06, 44"


def test_link_source():
    text = try_parse(
        "&Q002769 = SB Anzu 1\n" +
        "#link: source rinap/sources:P345512 = BM 078223\n" +
        "@tablet\n" +
        "1. Some text\n"
    )
    link = text.links[0]
    assert isinstance(link, Link)
    assert link.label is None
    assert link.code == "rinap/sources:P345512"
    assert link.description == "BM 078223"


def test_link_declaration_parallel():
    text = try_parse(
        "&Q002769 = SB Anzu 1\n" +
        "#link: parallel abcd:P363716 = TCL 06, 44\n" +
        "@tablet\n" +
        "1. Some text\n"
    )
    link = text.links[0]
    assert isinstance(link, Link)
    assert link.label is None
    assert link.code == "abcd:P363716"
    assert link.description == "TCL 06, 44"


def test_link_reference_simple():
    text = try_parse(
        "@tablet\n" +
        "1. Some text\n" +
        ">>A Tab.I, 102\n" +
        "2. Some more text\n"
    )
    link = text.children[0].children[0].links[0]
    assert isinstance(link, LinkReference)
    assert link.target == "A"
    assert link.operator == ">>"
    assert link.label == ["Tab.I", "102"]


def test_link_reference_comma():
    text = try_parse(
        "@tablet\n" +
        "1. Some text\n" +
        "|| A o ii 10\n" +
        "2. Some more text\n"
    )
    link = text.children[0].children[0].links[0]
    assert isinstance(link, LinkReference)
    assert link.target == "A"
    assert link.operator == "||"
    assert link.label == ["o", "ii", "10"]


def test_link_reference_range():
    text = try_parse(
        "@tablet\n" +
        "1. Some text\n" +
        ">> A o ii 10 - o ii 15\n" +
        "2. Some more text\n"
    )
    line = text.children[0].children[0]
    assert isinstance(line, Line)
    link = line.links[0]
    assert link.target == "A"
    assert link.operator == ">>"
    assert link.label == ["o", "ii", "10"]
    assert link.rangelabel == ["o", "ii", "15"]


def test_multilingual_interlinear():
    text = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "1. dim₃#-me-er# [...]\n" +
        "#lem: diŋir[deity]N; u\n" +
        "== %sb DINGIR-MEŠ GAL#-MEŠ# [...]\n" +
        "#lem: ilū[god]N; rabûtu[great]AJ; u\n" +
        "# ES dim₃-me-er = diŋir\n" +
        "|| A o ii 15\n")
    multilingual = text.children[0].children[0]
    assert isinstance(multilingual, Multilingual)
    assert len(multilingual.lines) == 2
    assert len(multilingual.lines[None].words) == 2
    assert len(multilingual.lines[None].lemmas) == 2
    assert len(multilingual.lines["sb"].words) == 3
    assert len(multilingual.lines["sb"].lemmas) == 3


def test_interlinear_translation():
    text = try_parse(
        "@tablet\n" +
        "1'. ⸢x⸣\n" +
        "#tr: English\n"
    )
    line = text.children[0].children[0]
    assert line.translation == "English"


def test_interlinear_empty():
    text = try_parse(
        "@tablet\n" +
        "1'. ⸢x⸣\n" +
        "#tr: \n"
    )
    line = text.children[0].children[0]
    assert line.translation == ""


def test_interlinear_multiline():
    text = try_parse(
        "@tablet\n" +
        "1'. ⸢x⸣\n" +
        "#tr: English\n" +
        " more"
    )
    line = text.children[0].children[0]
    assert line.translation == "English more"


def test_interlinear_ends_document():
    text = try_parse(
        "@tablet\n" +
        "1'. ⸢x⸣\n" +
        "#tr: English"
    )
    line = text.children[0].children[0]
    assert line.translation == "English"


def test_translation_heading():
    text = try_parse(
        "@tablet\n" +
        "@translation parallel en project\n" +
        "@h1 A translation heading\n"
    )
    assert len(text.children[0].children) == 1
    assert text.children[0].children[0].objecttype == 'h1'


def test_heading():
    text = try_parse(
        "@tablet\n" +
        "@h1 A heading\n"
    )
    assert text.children[0].objecttype == 'h1'


def test_milestone():
    text = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "@m=locator catchline\n" +
        "16'. si-i-ia-a-a-ku\n",
    )
    assert isinstance(text.children[0].children[0], Milestone)
    assert isinstance(text.children[0].children[1], Line)


def test_colophon():
    text = try_parse(
        "@tablet\n" +
        "@obverse\n" +
        "@colophon\n" +
        "16'. si-i-ia-a-a-ku\n",
    )
    assert isinstance(text.children[0].children[0], Milestone)
    assert isinstance(text.children[0].children[1], Line)


def test_include():
    text = try_parse(
        "&X001001 = My Text\n" +
        "@include dcclt:P229061 = MSL 07, 197 V02, 210 V11\n"
    )
    assert text.links[0].label == "Include"
    assert text.links[0].code == "dcclt:P229061"
    assert text.links[0].description == "MSL 07, 197 V02, 210 V11"
