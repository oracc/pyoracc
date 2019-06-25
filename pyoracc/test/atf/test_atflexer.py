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


from __future__ import print_function
from itertools import repeat
import pytest
from pyoracc.atf.common.atflex import AtfLexer
from pyoracc import _pyversion
if _pyversion() == 2:
    from itertools import izip_longest as zip_longest
else:
    from itertools import zip_longest


@pytest.fixture
def lexer():
    """AtfLexer instance used by each test."""
    return AtfLexer().lexer


def compare_tokens(lexer, content, expected_types, expected_values=None,
                   expected_lineno=None, expected_lexpos=None):
    lexer.input(content)
    if expected_values is None:
        expected_values = repeat(None)
    if expected_lineno is None:
        expected_lineno = repeat(None)
    if expected_lexpos is None:
        expected_lexpos = repeat(None)
    for e_type, e_value, e_lineno, e_lexpos, token in zip_longest(
            expected_types,
            expected_values,
            expected_lineno,
            expected_lexpos,
            lexer):
        if token is None and e_type is None:
            break
        assert token.type == e_type
        if e_value:
            assert token.value == e_value
        if e_lineno:
            assert token.lineno == e_lineno
        if e_lexpos:
            assert token.lexpos == e_lexpos


def ensure_raises_and_not(lexer, string, nwarnings):
    lexer.input(string)
    with pytest.raises(SyntaxError) as excinfo:
        for i in lexer:
            pass
    # If we allow invalid syntax this should not raise
    lexer = AtfLexer(skipinvalid=True).lexer
    lexer.input(string)
    with pytest.warns(UserWarning) as record:
        for i in lexer:
            pass
    assert len(record) == nwarnings


def test_code(lexer):
    compare_tokens(
        lexer,
        "&X001001 = JCS 48, 089\n",
        ["AMPERSAND", "ID", "EQUALS", "ID", "NEWLINE"],
        [None, "X001001", None, "JCS 48, 089"]
    )


def test_crlf(lexer):
    compare_tokens(
        lexer,
        "&X001001 = JCS 48, 089\r\n" +
        "#project: cams/gkab\n\r",
        ["AMPERSAND", "ID", "EQUALS", "ID", "NEWLINE"] +
        ["PROJECT", "ID", "NEWLINE"]
    )


def test_project(lexer):
    compare_tokens(
        lexer,
        "#project: cams/gkab\n",
        ["PROJECT", "ID", "NEWLINE"],
        [None, "cams/gkab", None]
    )


def test_key(lexer):
    compare_tokens(
        lexer,
        "#key: cdli=ND 02688\n",
        ["KEY", "ID", "EQUALS", "ID", "NEWLINE"],
        [None, "cdli", None, "ND 02688", None]
    )


def test_language_protocol(lexer):
    compare_tokens(
        lexer,
        "#atf: lang akk-x-stdbab\n",
        ["ATF", "LANG", "ID", "NEWLINE"],
        [None, None, "akk-x-stdbab"]
    )


def test_use_unicode(lexer):
    compare_tokens(
        lexer,
        "#atf: use unicode\n",
        ["ATF", "USE", "UNICODE", "NEWLINE"]
    )


def test_use_math(lexer):
    compare_tokens(
        lexer,
        "#atf: use math\n",
        ["ATF", "USE", "MATH", "NEWLINE"]
    )


def test_use_legacy(lexer):
    compare_tokens(
        lexer,
        "#atf: use legacy\n",
        ["ATF", "USE", "LEGACY", "NEWLINE"]
    )


def test_bib(lexer):
    compare_tokens(
        lexer,
        "#bib:  MEE 15 54\n",
        ["BIB", "ID", "NEWLINE"]
    )


def test_bib_long(lexer):
    # not documented but common
    compare_tokens(
        lexer,
        "#bib:  MEE 4 73 = EV a\n",
        ["BIB", "ID", "EQUALS", "ID", "NEWLINE"]
    )


def test_link(lexer):
    compare_tokens(
        lexer,
        "#link: def A = P363716 = TCL 06, 44\n" +
        "@tablet\n",
        ["LINK", "DEF", "ID", "EQUALS", "ID", "EQUALS", "ID", "NEWLINE",
         "TABLET", "NEWLINE"],
        [None, None, "A", None, "P363716", None, "TCL 06, 44"]
    )


def test_link_parallel_slash(lexer):
    compare_tokens(
        lexer,
        "#link: parallel dcclt/obale:P274929 = IM 070209\n" +
        "@tablet\n",
        ["LINK", "PARALLEL", "ID", "EQUALS", "ID", "NEWLINE",
         "TABLET", "NEWLINE"],
        [None, None, "dcclt/obale:P274929", None, "IM 070209"]
    )


def test_link_parallel(lexer):
    compare_tokens(
        lexer,
        "#link: parallel abcd:P363716 = TCL 06, 44\n" +
        "@tablet\n",
        ["LINK", "PARALLEL", "ID", "EQUALS", "ID", "NEWLINE",
         "TABLET", "NEWLINE"],
        [None, None, "abcd:P363716", None, "TCL 06, 44"]
    )


def test_link_reference(lexer):
    compare_tokens(
        lexer,
        "|| A o ii 10\n",
        ["PARBAR", "ID", "ID", "ID", "ID", "NEWLINE"]
    )


def test_link_reference_range(lexer):
    compare_tokens(
        lexer,
        "|| A o ii 10 -  o ii 12 \n",
        ["PARBAR", "ID", "ID", "ID", "ID", "MINUS",
         "ID", "ID", "ID", "NEWLINE"]
    )


def test_link_reference_prime_range(lexer):
    compare_tokens(
        lexer,
        "|| A o ii 10' -  o ii' 12 \n",
        ["PARBAR", "ID", "ID", "ID", "ID", "MINUS",
         "ID", "ID", "ID", "NEWLINE"]
    )


def test_score(lexer):
    compare_tokens(
        lexer,
        "@score matrix parsed word\n",
        ["SCORE", "ID", "ID", "ID", "NEWLINE"]
    )


def test_division_tablet(lexer):
    compare_tokens(
        lexer,
        "@tablet",
        ["TABLET"]
    )


def test_text_linenumber(lexer):
    compare_tokens(
        lexer,
        "1.    [MU] 1.03-KAM {iti}AB GE₆ U₄ 2-KAM",
        ["LINELABEL"] + ['ID'] * 6
    )


def test_lemmatize(lexer):
    compare_tokens(
        lexer,
        "#lem: šatti[year]N; n; Ṭebetu[1]MN; " +
        "mūša[at night]AV; ūm[day]N; n",
        ["LEM"] + ['ID', 'SEMICOLON'] * 5 + ['ID']
    )


def test_loose_dollar(lexer):
    compare_tokens(
        lexer,
        "$ (a loose dollar line)",
        ["DOLLAR", "PARENTHETICALID"],
        [None, "(a loose dollar line)"]
    )


def test_loose_nested_dollar(lexer):
    compare_tokens(
        lexer,
        "$ (a (very) loose dollar line)",
        ["DOLLAR", "PARENTHETICALID"],
        [None, "(a (very) loose dollar line)"]
    )


def test_loose_end_nested_dollar(lexer):
    compare_tokens(
        lexer,
        "$ (a loose dollar line (wow))",
        ["DOLLAR", "PARENTHETICALID"],
        [None, "(a loose dollar line (wow))"]
    )


def test_strict_dollar(lexer):
    compare_tokens(
        lexer,
        "$ reverse blank",
        ["DOLLAR", "REFERENCE", "BLANK"]
    )


def test_translation_intro(lexer):
    compare_tokens(
        lexer,
        "@translation parallel en project",
        ["TRANSLATION", "PARALLEL", "ID", "PROJECT"]
    )


def test_translation_text(lexer):
    compare_tokens(
        lexer,
        "@translation parallel en project\n" +
        "1.    Year 63, Ṭebetu (Month X), night of day 2:^1^",
        ["TRANSLATION", "PARALLEL", "ID", "PROJECT", "NEWLINE",
         "LINELABEL", "ID", "HAT", "ID", "HAT"],
        [None, "parallel", "en", "project", None,
         "1", "Year 63, Ṭebetu (Month X), night of day 2:",
         None, '1', None]
    )


def test_translation_multiline_text(lexer):
    compare_tokens(
        lexer,
        "@translation parallel en project\n" +
        "1.    Year 63, Ṭebetu (Month X)\n" +
        " , night of day 2\n",
        ["TRANSLATION", "PARALLEL", "ID", "PROJECT", "NEWLINE",
         "LINELABEL", "ID", "NEWLINE"],
        [None, "parallel", "en", "project", None,
         "1", "Year 63, Ṭebetu (Month X) , night of day 2", None]
    )


def test_translation_labeled_text(lexer):
    compare_tokens(
        lexer,
        "@translation labeled en project\n" +
        "@label o 4\n" +
        "Then it will be taken for the rites and rituals.\n\n",
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
         "LABEL", "ID", "ID", "NEWLINE",
         "ID", "NEWLINE"],
        [None, "labeled", "en", "project", None,
         None, "o", "4", None,
         'Then it will be taken for the rites and rituals.', None]
    )


def test_translation_labeled_noted_text(lexer):
    compare_tokens(
        lexer,
        "@translation labeled en project\n" +
        "@label r 8\n" +
        "The priest says the gods have performed these actions. ^1^\n\n" +
        "@note ^1^ Parenthesised text follows Neo-Assyrian source\n",
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
         "LABEL", "ID", "ID", "NEWLINE",
         "ID", "HAT", "ID", "HAT", "NEWLINE",
         "NOTE", "HAT", "ID", "HAT", "ID", 'NEWLINE'],
        [None, "labeled", "en", "project", None,
         None, "r", "8", None,
         'The priest says the gods have performed these actions.',
         None, "1", None, None,
         None, None, "1", None,
         "Parenthesised text follows Neo-Assyrian source"]

    )


def test_translation_labeled_dashlabel(lexer):
    compare_tokens(
        lexer,
        "@translation labeled en project\n" +
        "@label o 14-15 - o 20\n" +
        "You strew all (kinds of) seed.\n\n",
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
         "LABEL", "ID", "ID", "MINUS", "ID", "ID", "NEWLINE",
         "ID", "NEWLINE"],
        [None, "labeled", "en", "project", None,
         None, "o", "14-15", None, "o", "20", None]
    )


def test_translation_labeled_atlabel(lexer):
    compare_tokens(
        lexer,
        "@translation labeled en project\n" +
        "@(o 20) You strew all (kinds of) seed.\n" +
        "@(o i 2) No-one will occupy the king of Akkad's throne.\n\n",
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
         "OPENR", "ID", "ID", "CLOSER", "ID", "NEWLINE",
         "OPENR", "ID", "ID", "ID", "CLOSER", "ID", "NEWLINE", ],
        [None, "labeled", "en", "project", None,
         None, "o", "20", None, "You strew all (kinds of) seed.", None,
         None, "o", "i", "2", None,
         "No-one will occupy the king of Akkad's throne.", None, ]
    )


def test_translation_range_label_prime(lexer):
    compare_tokens(
        lexer,
        "@translation labeled en project\n" +
        "@label r 1' - r 2'\n",
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
         "LABEL", "ID", "ID", "MINUS", "ID", "ID", "NEWLINE"],
        [None, "labeled", "en", "project", None,
         None, "r", "1'", None, "r", "2'", None]
    )


def test_translation_label_unicode_suffix(lexer):
    compare_tokens(
        lexer,
        "@translation labeled en project\n" +
        u'@label r A\u2081\n',
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
         "LABEL", "ID", "ID", "NEWLINE"],
        [None, "labeled", "en", "project", None,
         None, "r", u"A\u2081"]
    )


def test_translation_label_unicode_prime(lexer):
    compare_tokens(
        lexer,
        "@translation labeled en project\n" +
        u'@label r 1\u2019\n',
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
         "LABEL", "ID", "ID", "NEWLINE"],
        [None, "labeled", "en", "project", None,
         None, "r", "1'", None]
    )


def test_translation_label_unicode_prime2(lexer):
    compare_tokens(
        lexer,
        "@translation labeled en project\n" +
        u'@label r 1\xb4\n',
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
         "LABEL", "ID", "ID", "NEWLINE"],
        [None, "labeled", "en", "project", None,
         None, "r", "1'", None]
    )


def test_translation_label_unicode_prime3(lexer):
    compare_tokens(
        lexer,
        "@translation labeled en project\n" +
        u'@label r 1\u2032\n',
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
         "LABEL", "ID", "ID", "NEWLINE"],
        [None, "labeled", "en", "project", None,
         None, "r", "1'", None]
    )


def test_translation_label_unicode_prime4(lexer):
    compare_tokens(
        lexer,
        "@translation labeled en project\n" +
        u'@label r 1\u02CA\n',
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
         "LABEL", "ID", "ID", "NEWLINE"],
        [None, "labeled", "en", "project", None,
         None, "r", "1'", None]
    )


def test_translation_range_label_plus(lexer):
    compare_tokens(
        lexer,
        "@translation labeled en project\n" +
        "@label+ o 28\n",
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
         "LABEL", "ID", "ID", "NEWLINE"]
    )


def test_translation_label_long_reference(lexer):
    "Translations can have full surface names rather than single letter"
    compare_tokens(
        lexer,
        "@translation labeled en project\n" +
        "@label obverse 28\n",
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
         "LABEL", "REFERENCE", "ID", "NEWLINE"]
    )


def test_translation_symbols_in_translation(lexer):
    compare_tokens(
        lexer,
        "@translation labeled en project\n" +
        "@label o 1'\n" +
        "[...] ... (zodiacal sign) 8, 10° = (sign) 12, 10°\n\n",
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
         "LABEL", "ID", "ID", "NEWLINE",
         "ID", "NEWLINE"]
    )


def test_translation_ats_in_translation(lexer):
    compare_tokens(
        lexer,
        "@translation labeled en project\n" +
        "@label o 1'\n" +
        "@kupputu (means): affliction (@? and) reduction?@;" +
        " they are ... like cisterns.\n\n",
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
         "LABEL", "ID", "ID", "NEWLINE",
         "ID", "NEWLINE"]
    )


def test_translation_blank_line_begins_translation(lexer):
    # A double newline normally ends a translation paragraph
    # But this is NOT the case at the beginning of a section,
    # Apparently.
    compare_tokens(
        lexer,
        "@translation labeled en project\n" +
        "@label o 16\n" +
        "\n" +
        "@šipir @ṭuhdu @DU means: a message of abundance" +
        " will come triumphantly.\n",
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
         "LABEL", "ID", "ID", "NEWLINE",
         "ID", "NEWLINE"]
    )


def test_translation_blank_line_amid_translation(lexer):
    # A double newline normally ends a translation paragraph
    # But this is NOT the case at the beginning of a section,
    # Apparently.
    compare_tokens(
        lexer,
        "@translation labeled en project\n" +
        "@(4) their [cri]mes [have been forgiven] by the king." +
        " (As to) all [the\n" +
        "\n" +
        "    libe]ls that [have been uttered against me " +
        "in the palace, which] he has\n" +
        "\n" +
        "    heard, [I am not guilty of] any [of them! " +
        "N]ow, should there be a\n",
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
         "OPENR", "ID", "CLOSER", "ID", "NEWLINE",
         "ID", "NEWLINE", "ID", "NEWLINE"]
    )


def test_translation_no_blank_line_in_labeled_translation(lexer):
    # This functionality is expressly forbidden at
    # http://build.oracc.org/doc2/help/editinginatf/translations/index.html
    # But appears is in cm_31_139 anyway
    compare_tokens(
        lexer,
        "@translation labeled en project\n" +
        "@label o 13\n" +
        "@al-@ŋa₂-@ŋa₂ @al-@ŋa₂-@ŋa₂ @šag₄-@ba-@ni" +
        " @nu-@sed-@da (means) he will" +
        "remove (... and) he will place (...); his heart will not rest" +
        "It is said in the textual corpus of the lamentation-priests.\n" +
        "@label o 15\n" +
        "Text\n\n",
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
         "LABEL", "ID", "ID", "NEWLINE",
         "ID", "NEWLINE",
         "LABEL", "ID", "ID", "NEWLINE",
         "ID", "NEWLINE"]
    )


def test_translation_ATlines_in_translation(lexer):
    # @ within Translations mark Foreign
    # http://oracc.museum.upenn.edu/doc/help/editinginatf/translations/index.html
    compare_tokens(
        lexer,
        "@translation labeled en project\n" +
        "@obverse\n" +
        "1'. @MUD (means) trembling. @MUD (means) dark.",
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
         "OBVERSE", "NEWLINE", "ID"]
    )


def test_translation_range_label_periods(lexer):
    compare_tokens(
        lexer,
        "@translation labeled en project\n" +
        "@label t.e. 1\n",
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
         "LABEL", "ID", "ID", "NEWLINE"],
        [None, "labeled", "en", "project", None,
         None, "t.e.", "1"])


def test_interlinear_translation(lexer):
    compare_tokens(
        lexer,
        "@tablet\n" +
        "1'. ⸢x⸣\n" +
        "#tr: English\n",
        ["TABLET", "NEWLINE",
         "LINELABEL", "ID", "NEWLINE",
         "TR", "ID", "NEWLINE"])


def test_multilineinterlinear_translation(lexer):
    compare_tokens(
        lexer,
        "@tablet\n" +
        "1'. ⸢x⸣\n" +
        "#tr: English\n" +
        " on multiple lines\n",
        ["TABLET", "NEWLINE",
         "LINELABEL", "ID", "NEWLINE",
         "TR", "ID", "NEWLINE"])


def test_note_internalflag(lexer):
    compare_tokens(
        lexer,
        "@note Hello James's World",
        ["NOTE", "ID"],
        [None, "Hello James's World"]
    )


def test_note_internalspace(lexer):
    compare_tokens(
        lexer,
        "@note Hello James",
        ["NOTE", "ID"],
        [None, "Hello James"]
    )


def test_note_onechar(lexer):
    compare_tokens(
        lexer,
        "@note H",
        ["NOTE", "ID"],
        [None, "H"]
    )


def test_note_short(lexer):
    compare_tokens(
        lexer,
        "@note I'm",
        ["NOTE", "ID"],
        [None, "I'm"]
    )


def test_division_note(lexer):
    compare_tokens(
        lexer,
        "@note ^1^ A note to the translation.\n",
        ["NOTE", "HAT", "ID", "HAT", "ID", "NEWLINE"],
        [None, None, "1", None, "A note to the translation.", None]
    )


def test_hash_note(lexer):
    compare_tokens(
        lexer,
        "@tablet\n" +
        "@obverse\n" +
        "3.    U₄!-BI? 20* [(ina)] 9.30 ina(DIŠ) MAŠ₂!(BAR)\n" +
        "#note: Note to line.\n",
        ["TABLET", "NEWLINE", "OBVERSE", "NEWLINE",
         "LINELABEL"] + ["ID"] * 6 + ["NEWLINE", "NOTE", "ID", "NEWLINE"]
    )


def test_hash_note_UPPERCASE(lexer):
    # Some files in the corpus such as ctn_4_168.atf
    # Contains #NOTE: even if the line should be #note:
    compare_tokens(
        lexer,
        "@tablet\n" +
        "@obverse\n" +
        "3.    U₄!-BI? 20* [(ina)] 9.30 ina(DIŠ) MAŠ₂!(BAR)\n" +
        "#NOTE: Note to line.\n",
        ["TABLET", "NEWLINE", "OBVERSE", "NEWLINE",
         "LINELABEL"] + ["ID"] * 6 + ["NEWLINE", "NOTE", "ID", "NEWLINE"]
    )


def test_hash_note_multiline(lexer):
    # Notes can be free text until a double-newline.
    line = "a-šar _saḫar.ḫi.a_ bu-bu-su-nu"
    compare_tokens(
        lexer,
        "1. " + line + "\n" +
        "#note: Does this combine with the next line?\n"
        "It should.\n\n",
        ["LINELABEL"] + ["ID"] * len(line.split()) + ["NEWLINE"] +
        ["NOTE", "ID", "NEWLINE"],
        ['1'] + line.split() +
        [None, None, "Does this combine with the next line?\nIt should."]
    )


def test_open_text_with_dots(lexer):
    # This must not come out as a linelabel of Hello.
    compare_tokens(
        lexer,
        "@translation labeled en project\n" +
        "@label o 1\nHello. World\n\n",
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
         "LABEL", "ID", "ID", "NEWLINE",
         "ID", "NEWLINE"]
    )


def test_flagged_object(lexer):
    compare_tokens(
        lexer,
        "@object which is remarkable and broken!#\n",
        ["OBJECT", "ID", "EXCLAIM", "HASH", "NEWLINE"])


def test_comment(lexer):
    compare_tokens(
        lexer,
        "# I've added various things for test purposes\n",
        ['COMMENT', "ID", "NEWLINE"]
    )


def test_nospace_comment(lexer):
    compare_tokens(
        lexer,
        "#I've added various things for test purposes\n",
        ['COMMENT', "ID", "NEWLINE"]
    )


def test_check_comment(lexer):
    compare_tokens(
        lexer,
        "#CHECK: I've added various things for test purposes\n",
        ['CHECK', "ID", "NEWLINE"]
    )


def test_dotline(lexer):
    compare_tokens(
        lexer,
        ". \n",
        ['NEWLINE']
    )


def test_translation_heading(lexer):
    compare_tokens(
        lexer,
        "@translation parallel en project\n" +
        "@h1 A translation heading\n",
        ["TRANSLATION", "PARALLEL", "ID", "PROJECT", "NEWLINE"] +
        ["HEADING", "ID", "NEWLINE"]
    )


def test_heading(lexer):
    compare_tokens(
        lexer,
        "@obverse\n" +
        "@h1 A heading\n",
        ["OBVERSE", "NEWLINE"] +
        ["HEADING", "ID", "NEWLINE"]
    )


def test_double_comment(lexer):
    """Not sure if this is correct; but can't find
    anything in structure or lemmatization doc"""
    compare_tokens(
        lexer,
        "## papān libbi[belly] (already in gloss, same spelling)\n",
        ['COMMENT', 'ID', 'NEWLINE']
    )


def test_ruling(lexer):
    compare_tokens(
        lexer,
        "$ single ruling",
        ["DOLLAR", "SINGLE", "RULING"]
    )


def test_described_object(lexer):
    compare_tokens(
        lexer,
        "@object An object that fits no other category\n",
        ["OBJECT", "ID", "NEWLINE"],
        [None, "An object that fits no other category"]
    )


def test_nested_object(lexer):
    compare_tokens(
        lexer,
        "@tablet\n" +
        "@obverse\n",
        ["TABLET", "NEWLINE", "OBVERSE", "NEWLINE"]
    )


def test_object_line(lexer):
    compare_tokens(
        lexer,
        "@tablet\n" +
        "@obverse\n" +
        "1.    [MU] 1.03-KAM {iti}AB GE₆ U₄ 2-KAM\n"
        "#lem: šatti[year]N; n; Ṭebetu[1]MN; mūša[at night]AV; " +
        "ūm[day]N; n\n",
        ['TABLET', 'NEWLINE',
         "OBVERSE", 'NEWLINE',
         'LINELABEL'] + ['ID'] * 6 + ['NEWLINE', 'LEM'] +
        ['ID', 'SEMICOLON'] * 5 + ['ID', "NEWLINE"]
    )


def test_dot_in_linelabel(lexer):
    compare_tokens(
        lexer,
        "1.1.    [MU]\n",
        ['LINELABEL', 'ID', 'NEWLINE']
    )


def test_score_lines(lexer):
    compare_tokens(
        lexer,
        "@score matrix parsed\n" +
        "1.4′. %n ḫašḫūr [api] lal[laga imḫur-līm?]\n" +
        "#lem: ḫašḫūr[apple (tree)]N; api[reed-bed]N\n\n" +
        "A₁_obv_i_4′: [x x x x x] {ú}la-al-[la-ga? {ú}im-ḫu-ur-lim?]\n" +
        "#lem: u; u; u; u; u; " +
        "+lalangu[(a leguminous vegetable)]N$lallaga\n\n" +
        "e_obv_15′–16′: {giš}ḪAŠḪUR [GIŠ.GI] — // [{ú}IGI-lim]\n" +
        "#lem: +hašhūru[apple (tree)]N$hašhūr; api[reed-bed]N;" +
        " imhur-līm['heals-a-thousand'-plant]N\n\n",
        ['SCORE', 'ID', 'ID', "NEWLINE"] +
        ['LINELABEL'] + ['ID'] * 5 + ['NEWLINE'] +
        ['LEM', 'ID', 'SEMICOLON', 'ID', 'NEWLINE'] +
        ['SCORELABEL'] + ['ID'] * 7 + ['NEWLINE'] +
        ['LEM'] + ['ID', 'SEMICOLON'] * 5 + ['ID', 'NEWLINE'] +
        ['SCORELABEL'] + ['ID'] * 5 + ['NEWLINE'] +
        ['LEM'] + ['ID', 'SEMICOLON'] * 2 + ['ID', 'NEWLINE']
    )


def test_composite(lexer):
    compare_tokens(
        lexer,
        "&Q002769 = SB Anzu 1\n" +
        "@composite\n" +
        "#project: cams/gkab\n" +
        "1.   bi#-in šar da-ad-mi šu-pa-a na-ram {d}ma#-mi\n" +
        "&Q002770 = SB Anzu 2\n" +
        "#project: cams/gkab\n" +
        "1.   bi-riq ur-ha šuk-na a-dan-na\n",
        ["AMPERSAND", "ID", "EQUALS", "ID", "NEWLINE"] +
        ['COMPOSITE', 'NEWLINE'] +
        ["PROJECT", "ID", "NEWLINE"] +
        ["LINELABEL"] + ['ID'] * 6 + ['NEWLINE'] +
        ["AMPERSAND", "ID", "EQUALS", "ID", "NEWLINE"] +
        ["PROJECT", "ID", "NEWLINE"] +
        ["LINELABEL"] + ['ID'] * 4 + ["NEWLINE"]
    )


def test_translated_composite(lexer):
    compare_tokens(
        lexer,
        "&Q002769 = SB Anzu 1\n" +
        "@composite\n" +
        "#project: cams/gkab\n" +
        "1.   bi#-in šar da-ad-mi šu-pa-a na-ram {d}ma#-mi\n" +
        "@translation labeled en project\n" +
        "@(1) English\n"
        "&Q002770 = SB Anzu 2\n" +
        "#project: cams/gkab\n" +
        "1.   bi-riq ur-ha šuk-na a-dan-na\n",
        ["AMPERSAND", "ID", "EQUALS", "ID", "NEWLINE"] +
        ['COMPOSITE', 'NEWLINE'] +
        ["PROJECT", "ID", "NEWLINE"] +
        ["LINELABEL"] + ['ID'] * 6 + ['NEWLINE'] +
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE"] +
        ["OPENR", "ID", "CLOSER", "ID", "NEWLINE"] +
        ["AMPERSAND", "ID", "EQUALS", "ID", "NEWLINE"] +
        ["PROJECT", "ID", "NEWLINE"] +
        ["LINELABEL"] + ['ID'] * 4 + ["NEWLINE"]
    )


def test_equalbrace(lexer):
    compare_tokens(
        lexer,
        "@tablet\n" +
        "@reverse\n" +
        "2'.    ITI# an-ni-u2#\n" +
        "={    ur-hu\n",
        ['TABLET', "NEWLINE"] +
        ["REVERSE", "NEWLINE"] +
        ["LINELABEL"] + ['ID'] * 2 + ["NEWLINE"] +
        ["EQUALBRACE", "ID", "NEWLINE"]
    )


def test_multilingual_interlinear(lexer):
    compare_tokens(
        lexer,
        "@tablet\n" +
        "@obverse\n" +
        "1. dim₃#-me-er# [...]\n" +
        "#lem: diŋir[deity]N; u\n" +
        "== %sb DINGIR-MEŠ GAL#-MEŠ# [...]\n" +
        "#lem: ilū[god]N; rabûtu[great]AJ; u\n" +
        "# ES dim₃-me-er = diŋir\n" +
        "|| A o ii 15\n",
        ['TABLET', "NEWLINE"] +
        ["OBVERSE", "NEWLINE"] +
        ["LINELABEL"] + ['ID'] * 2 + ["NEWLINE"] +
        ["LEM"] + ["ID", "SEMICOLON"] + ["ID"] + ["NEWLINE"] +
        ["MULTILINGUAL", "ID"] + ["ID"] * 3 + ["NEWLINE"] +
        ["LEM"] + ["ID", "SEMICOLON"] * 2 + ["ID"] + ["NEWLINE"] +
        ["COMMENT", "ID", "NEWLINE"] +
        ["PARBAR", "ID", "ID", "ID", "ID", "NEWLINE"]
    )


def test_strict_in_parallel(lexer):
    compare_tokens(
        lexer,
        "@translation parallel en project\n" +
        "$ reverse blank",
        ["TRANSLATION", "PARALLEL", "ID", "PROJECT", "NEWLINE"] +
        ["DOLLAR", "ID"]
    )


def test_query_in_parallel(lexer):
    """"The parallel ID regex was to general and identified ? after
        @obverse as an ID token not a QUERY"""
    compare_tokens(
        lexer,
        "@translation parallel en project\n" +
        "@obverse?",
        ["TRANSLATION", "PARALLEL", "ID", "PROJECT", "NEWLINE"] +
        ["OBVERSE", "QUERY"]
    )


def test_loose_in_labeled(lexer):
    compare_tokens(
        lexer,
        "@translation labeled en project\n" +
        "$ (Break)\n" +
        "@(r 2) I am\n\n",
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE"] +
        ["DOLLAR", "ID", "NEWLINE"] +
        ["OPENR", "ID", "ID", "CLOSER", "ID", "NEWLINE"]
    )


def test_ati_in_translation(lexer):
    compare_tokens(
        lexer,
        "@translation labeled en project\n" +
        "@(r 2) I am\n" +
        "@i{eššēšu-}festival\n",
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE"] +
        ["OPENR", "ID", "ID", "CLOSER", "ID", "NEWLINE"]
    )


def test_blank_after_para_transctrl_windows(lexer):
    """[...] should not exit the para state but did previously
       due to a not as stric regex """
    compare_tokens(
        lexer,
        "@translation labeled en project\r\n" +
        "@(o i 1')\r\n" +
        "[...]\r\n\r\n" +
        "@(o i 2')\r\n" +
        "[... you put] inside [his] ears [and the evil] " +
        "afflicting his head [will be eradicated].\r\n\r\n",
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE"] +
        ["OPENR", "ID", "ID", "ID", "CLOSER"] +
        ["ID", "NEWLINE"] +
        ["OPENR", "ID", "ID", "ID", "CLOSER"] +
        ["ID", "NEWLINE"]
    )


def test_blank_after_para_transctrl(lexer):
    """[...] should not exit the para state but did previously
       due to a not as stric regex """
    compare_tokens(
        lexer,
        "@translation labeled en project\n" +
        "@(o i 1)\n" +
        "[(If) in] Tašritu (month VII), on day 1, " +
        "a solar eclipse takes place: [...].\n\n" +
        "@(o i 2)\n" +
        "[...], on day 7, a solar eclipse takes place: [...].\n\n",
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE"] +
        ["OPENR", "ID", "ID", "ID", "CLOSER"] +
        ["ID", "NEWLINE"] +
        ["OPENR", "ID", "ID", "ID", "CLOSER"] +
        ["ID", "NEWLINE"]
    )


def test_strict_in_labelled_parallel(lexer):
    compare_tokens(
        lexer,
        "@translation labeled en project\n" +
        "$ reverse blank",
        ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE"] +
        ["DOLLAR", "ID"]
    )


def test_strict_as_loose_in_translation(lexer):
    compare_tokens(
        lexer,
        "@translation parallel en project\n" +
        "$ Continued in text no. 2\n",
        ["TRANSLATION", "PARALLEL", "ID", "PROJECT", "NEWLINE"] +
        ["DOLLAR", "ID", "NEWLINE"]
    )


def test_punctuated_translation(lexer):
    compare_tokens(
        lexer,
        "@translation parallel en project\n" +
        "1. 'What is going on?', said the King!\n",
        ["TRANSLATION", "PARALLEL", "ID", "PROJECT", "NEWLINE"] +
        ["LINELABEL", "ID", "NEWLINE"],
        [None, None, "en", None, None] +
        ["1", "'What is going on?', said the King!", None]
    )


def test_translation_note(lexer):
    compare_tokens(
        lexer,
        "@translation parallel en project\n" +
        "@reverse\n" +
        "#note: reverse uninscribed\n",
        ["TRANSLATION", "PARALLEL", "ID", "PROJECT", "NEWLINE"] +
        ["REVERSE", "NEWLINE"] +
        ["NOTE", "ID", "NEWLINE"]
    )


def test_equals_in_translation_note(lexer):
    compare_tokens(
        lexer,
        "@translation parallel en project\n" +
        "@reverse\n" +
        '#note: The CAD translation šarriru = "humble",\n',
        ["TRANSLATION", "PARALLEL", "ID", "PROJECT", "NEWLINE"] +
        ["REVERSE", "NEWLINE"] +
        ["NOTE", "ID", "NEWLINE"]
        )


def test_note_ended_by_strucuture(lexer):
    compare_tokens(
        lexer,
        "@translation parallel en project\n" +
        "@obverse\n" +
        '#note: The CAD translation šarriru = "humble",\n' +
        '@reverse',
        ["TRANSLATION", "PARALLEL", "ID", "PROJECT", "NEWLINE"] +
        ["OBVERSE", "NEWLINE"] +
        ["NOTE", "ID", "NEWLINE"] +
        ["REVERSE"]
    )


@pytest.mark.parametrize('line_label', [
    "1",
    "2'",
    u"3\u2019",
    u"4\u2032",
    u"5\u02CA",
    u"6\xb4"
])
def test_note_ended_by_line(lexer, line_label):
    'Notes can be free text until the next line label.'
    # Sample text.
    line1 = u"a-šar _saḫar.ḫi.a_ bu-bu-su-nu"
    line2 = u"a-kal-ši-na ṭi-id-di"
    # Generate the successive line numbers in the same style.
    label1 = line_label
    next_label = int(label1[:1]) + 1
    if _pyversion() == 2:
        label2 = unicode(next_label) + label1[1:]
    else:
        label2 = str(next_label) + label1[1:]
    compare_tokens(
        lexer,
        label1 + ". " + line1 + "\n" +
        "#note: Does this combine with the next line?\n" +
        label2 + ". " + line2 + "\n",
        ["LINELABEL"] + ["ID"] * len(line1.split()) + ["NEWLINE"] +
        ["NOTE", "ID", "NEWLINE"] +
        ["LINELABEL"] + ["ID"] * len(line2.split()) + ["NEWLINE"],
        [label1] + line1.split() +
        [None, None, "Does this combine with the next line?", None] +
        [label2] + line2.split() + [None]
    )


def test_milestone(lexer):
    compare_tokens(
        lexer,
        "@tablet\n" +
        "@obverse\n" +
        "@m=locator catchline\n" +
        "16'. si-i-ia-a-a-ku\n",
        ["TABLET", "NEWLINE",
         "OBVERSE", "NEWLINE",
         "M", "EQUALS", "ID", "NEWLINE",
         "LINELABEL", "ID", "NEWLINE"]
    )


def test_include(lexer):
    compare_tokens(
        lexer,
        "@tablet\n" +
        "@obverse\n" +
        "@include dcclt:P229061 = MSL 07, 197 V02, 210 V11\n",
        ["TABLET", "NEWLINE",
         "OBVERSE", "NEWLINE",
         "INCLUDE", "ID", 'EQUALS', 'ID', "NEWLINE"]
    )


def test_double_newline_and_lexpos(lexer):
    compare_tokens(
        lexer,
        "@obverse\n" +
        "\n" +
        "#note:\n",
        ["OBVERSE", "NEWLINE", "NOTE", "NEWLINE"],
        ["obverse", "\n\n", "note", "\n"],
        [1, 1, 3, 3],
        [1, 8, 11, 16])


def test_blankline_with_tab_inadsorb(lexer):
    compare_tokens(
        lexer,
        "# ES mu-lu = lu₂, ša₃-ab = šag\n" +
        "	\n" +
        "7. keš₂-da",
        ["COMMENT", "ID", "NEWLINE", "LINELABEL", "ID"],
        ["#", "ES mu-lu = lu₂, ša₃-ab = šag", "\n\t\n", '7', "keš₂-da"])


def test_invalid_at_raises_syntax_error(lexer):
    string = u"@obversel\n"
    ensure_raises_and_not(lexer, string, nwarnings=1)


def test_invalid_hash_raises_syntax_error(lexer):
    string = u"#lems: Ṣalbatanu[Mars]CN\n"
    ensure_raises_and_not(lexer, string, nwarnings=2)


def test_invalid_id_syntax_error(lexer):
    string = u"Ṣalbatanu[Mars]CN\n"
    ensure_raises_and_not(lexer, string, nwarnings=1)


def test_resolve_keyword_no_extra():
    '''Test that resolve_keyword works correcty when extra is not passes
    This never happes in actual code. Hench this test'''
    mylexer = AtfLexer()
    result = mylexer.resolve_keyword('obverse',
                                     mylexer.structures)
    assert result == 'OBVERSE'
