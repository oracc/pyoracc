# -*- coding: utf-8 -*-
from unittest import TestCase, skip
from ...atf.atflex import AtfLexer
from nose.tools import assert_in, assert_equal
from itertools import izip_longest, repeat


class testLexer(TestCase):
    def setUp(self):
        self.lexer = AtfLexer().lexer

    def compare_tokens(self, content, expected_types, expected_values=None):
        self.lexer.input(content)
        if expected_values is None:
            expected_values = repeat(None)
        for expected_type, expected_value, token in izip_longest(
                expected_types, expected_values, self.lexer):
            #print token, expected_type
            if token is None and expected_type is None:
                break  # The end-condition on the
                       # self.lexer iterable seems broken
            assert_equal(token.type, expected_type)
            if expected_value:
                #print token.value, expected_value
                assert_equal(token.value, expected_value)

    def test_code(self):
        self.compare_tokens(
            "&X001001 = JCS 48, 089\n",
            ["AMPERSAND", "ID", "EQUALS", "ID", "NEWLINE"],
            [None, "X001001", None, "JCS 48, 089"]
        )

    def test_project(self):
        self.compare_tokens(
            "#project: cams/gkab\n",
            ["PROJECT", "ID", "NEWLINE"],
            [None, "cams/gkab", None]
        )

    def test_language_protocol(self):
        self.compare_tokens(
            "#atf: lang akk-x-stdbab\n",
            ["ATF", "LANG", "ID", "NEWLINE"],
            [None, None, "akk-x-stdbab"]
        )

    def test_use_unicode(self):
        self.compare_tokens(
            "#atf: use unicode\n",
            ["ATF", "USE", "UNICODE", "NEWLINE"]
        )

    def test_use_math(self):
        self.compare_tokens(
            "#atf: use math\n",
            ["ATF", "USE", "MATH", "NEWLINE"]
        )

    def test_link(self):
        self.compare_tokens(
            "#link: def A = P363716 = TCL 06, 44\n" +
            "@tablet\n",
            ["LINK", "DEF", "ID", "EQUALS", "ID", "EQUALS", "ID", "NEWLINE",
            "TABLET", "NEWLINE"],
            [None, None, "A", None, "P363716", None, "TCL 06, 44"]
        )

    def test_link_reference(self):
        self.compare_tokens(
            "|| A o ii 10\n",
            ["PARBAR", "ID", "ID", "ID", "ID", "NEWLINE"]
        )

    def test_link_reference_range(self):
        self.compare_tokens(
            "|| A o ii 10 -  o ii 12 \n",
            ["PARBAR", "ID", "ID", "ID", "ID", "MINUS",
            "ID", "ID", "ID", "NEWLINE"]
        )

    def test_link_reference_prime_range(self):
        self.compare_tokens(
            "|| A o ii 10' -  o ii' 12 \n",
            ["PARBAR", "ID", "ID", "ID", "ID", "MINUS",
            "ID", "ID", "ID", "NEWLINE"]
        )

    def test_division_tablet(self):
        self.compare_tokens(
            "@tablet",
            ["TABLET"]
        )

    def test_text_linenumber(self):
        self.compare_tokens(
            "1.    [MU] 1.03-KAM {iti}AB GE₆ U₄ 2-KAM",
            ["LINELABEL"] + ['ID'] * 6
        )

    def test_lemmatize(self):
        self.compare_tokens(
            "#lem: šatti[year]N; n; Ṭebetu[1]MN; " +
            "mūša[at night]AV; ūm[day]N; n",
            ["LEM"] + ['ID', 'SEMICOLON'] * 5 + ['ID']
        )

    def test_loose_dollar(self):
        self.compare_tokens(
            "$ (a loose dollar line)",
            ["DOLLAR", "PARENTHETICALID"],
            [None, "(a loose dollar line)"]
        )

    def test_strict_dollar(self):
        self.compare_tokens(
            "$ reverse blank",
            ["DOLLAR", "REFERENCE", "BLANK"]
        )

    def test_translation_intro(self):
        self.compare_tokens(
            "@translation parallel en project",
            ["TRANSLATION", "PARALLEL", "ID", "PROJECT"]
        )

    def test_translation_text(self):
        self.compare_tokens(
            "@translation parallel en project\n" +
            "1.    Year 63, Ṭebetu (Month X), night of day 2:^1^",
            ["TRANSLATION", "PARALLEL", "ID", "PROJECT", "NEWLINE",
             "LINELABEL", "ID", "HAT", "ID", "HAT"],
            [None, "parallel", "en", "project", None,
             "1", "Year 63, Ṭebetu (Month X), night of day 2:",
             None, '1', None]
        )

    def test_translation_labeled_text(self):
        self.compare_tokens(
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

    def test_translation_labeled_noted_text(self):
        self.compare_tokens(
            "@translation labeled en project\n" +
            "@label r 8\n" +
            "The priest says the gods have performed these actions. ^1^\n\n" +
            "@note ^1^ Parenthesised text follows Neo-Assyrian source\n",
            ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
             "LABEL", "ID", "ID", "NEWLINE",
             "ID", "HAT","ID","HAT", "NEWLINE",
             "NOTE","HAT","ID","HAT","ID",'NEWLINE'],
            [None, "labeled", "en", "project", None,
             None, "r", "8", None,
             'The priest says the gods have performed these actions.', None, "1", None,None,
             None, None, "1", None, "Parenthesised text follows Neo-Assyrian source"]

        )

    def test_translation_labeled_dashlabel(self):
        self.compare_tokens(
            "@translation labeled en project\n" +
            "@label o 14-15 - o 20\n" +
            "You strew all (kinds of) seed.\n\n",
            ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
             "LABEL", "ID", "ID",  "MINUS", "ID", "ID", "NEWLINE", 
             "ID", "NEWLINE"],
            [None, "labeled", "en", "project", None,
             None, "o", "14-15", None, "o", "20", None]
        )

    def test_translation_labeled_atlabel(self):
        self.compare_tokens(
            "@translation labeled en project\n" +
            "@(o 20) You strew all (kinds of) seed.\n" +
            "@(o i 2) No-one will occupy the king of Akkad's throne.\n\n",
            ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
             "OPENR","ID", "ID", "CLOSER","ID","NEWLINE", 
             "OPENR","ID", "ID","ID","CLOSER","ID","NEWLINE",],
            [None, "labeled", "en", "project", None,
             None, "o", "20", None, "You strew all (kinds of) seed.", None,
             None, "o", "i", "2", None, "No-one will occupy the king of Akkad's throne.", None,]
        )

    def test_translation_range_label_prime(self):
        self.compare_tokens(
            "@translation labeled en project\n" +
            "@label r 1' - r 2'\n",
            ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
             "LABEL", "ID", "ID", "MINUS", "ID", "ID", "NEWLINE"],
            [None, "labeled", "en", "project", None,
             None, "r", "1'", None, "r", "2'", None]
        )

    def test_translation_range_label_plus(self):
        self.compare_tokens(
            "@translation labeled en project\n" +
            "@label+ o 28\n",
            ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
             "LABEL", "ID", "ID", "NEWLINE"]
        )

    def test_translation_symbols_in_translation(self):
        self.compare_tokens(
            "@translation labeled en project\n" +
            "@label o 1'\n" +
            "[...] ... (zodiacal sign) 8, 10° = (sign) 12, 10°\n\n",
            ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
             "LABEL", "ID", "ID", "NEWLINE",
             "ID","NEWLINE"]
        )

    def test_translation_ats_in_translation(self):
        self.compare_tokens(
            "@translation labeled en project\n" +
            "@label o 1'\n" +
            "@kupputu (means): affliction (@? and) reduction?@; they are ... like cisterns.\n\n",
            ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
             "LABEL", "ID", "ID", "NEWLINE",
             "ID","NEWLINE"]
        )

    def test_translation_no_blank_line_in_labeled_translation(self):
        # This functionality is expressly forbidden at 
        # http://build.oracc.org/doc2/help/editinginatf/translations/index.html
        # But appears is in cm_31_139 anyway
        self.compare_tokens(
            "@translation labeled en project\n" +
            "@label o 13\n" +
            "@al-@ŋa₂-@ŋa₂ @al-@ŋa₂-@ŋa₂ @šag₄-@ba-@ni @nu-@sed-@da (means) he will" +
            "remove (... and) he will place (...); his heart will not rest"+
            "It is said in the textual corpus of the lamentation-priests.\n"+
            "@label o 15\n"+
            "Text\n\n",
            ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
             "LABEL", "ID", "ID", "NEWLINE",
             "ID","NEWLINE",
             "LABEL","ID","ID","NEWLINE",
             "ID","NEWLINE"]
        )

    def test_translation_range_label_periods(self):
        self.compare_tokens(
            "@translation labeled en project\n" +
            "@label t.e. 1\n",
            ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
             "LABEL", "ID", "ID", "NEWLINE"],
            [None, "labeled", "en", "project", None,
             None, "t.e.", "1"])

    def test_note_internalflag(self):
        self.compare_tokens(
            "@note Hello James's World",
            ["NOTE", "ID"],
            [None, "Hello James's World"]
        )

    def test_note_internalspace(self):
        self.compare_tokens(
            "@note Hello James",
            ["NOTE", "ID"],
            [None, "Hello James"]
        )

    def test_note_onechar(self):
        self.compare_tokens(
            "@note H",
            ["NOTE", "ID"],
            [None, "H"]
        )

    def test_note_short(self):
        self.compare_tokens(
            "@note I'm",
            ["NOTE", "ID"],
            [None, "I'm"]
        )

    def test_division_note(self):
        self.compare_tokens(
            "@note ^1^ A note to the translation.\n",
            ["NOTE", "HAT", "ID", "HAT", "ID", "NEWLINE"],
            [None, None, "1", None, "A note to the translation.", None]
        )

    def test_hash_note(self):
        self.compare_tokens(
            "@tablet\n" +
            "@obverse\n" +
            "3.    U₄!-BI? 20* [(ina)] 9.30 ina(DIŠ) MAŠ₂!(BAR)\n" +
            "#note: Note to line.\n",
            ["TABLET", "NEWLINE", "OBVERSE", "NEWLINE",
             "LINELABEL"] + ["ID"] * 6 + ["NEWLINE", "NOTE", "ID", "NEWLINE"]
        )

    def test_open_text_with_dots(self):
        # This must not come out as a linelabel of Hello.
        self.compare_tokens(
            "@translation labeled en project\n" +
            "@label o 1\nHello. World\n\n",
            ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE",
            "LABEL", "ID", "ID", "NEWLINE",
            "ID", "NEWLINE"]
        )

    def test_flagged_object(self):
        self.compare_tokens("@object which is remarkable and broken!#\n",
                            ["OBJECT", "ID", "EXCLAIM", "HASH", "NEWLINE"])

    def test_comment(self):
        self.compare_tokens(
            "# I've added various things for test purposes\n",
            ['NEWLINE']
        )

    def test_dotline(self):
        self.compare_tokens(
            ". \n",
            ['NEWLINE']
        )

    def test_translation_heading(self):
        self.compare_tokens(
            "@translation parallel en project\n" +
            "@h1 A translation heading\n",
            ["TRANSLATION", "PARALLEL", "ID", "PROJECT", "NEWLINE"] + 
            ["HEADING","ID","NEWLINE"]
        )

    def test_heading(self):
        self.compare_tokens(
            "@obverse\n" +
            "@h1 A heading\n",
            ["OBVERSE", "NEWLINE"] + 
            ["HEADING","ID","NEWLINE"] 
    )

    def test_double_comment(self):
        """Not sure if this is correct; but can't find 
        anything in structure or lemmatization doc"""
        self.compare_tokens(
            "## papān libbi[belly] (already in gloss, same spelling)\n",
            ['NEWLINE']
        )

    def test_ruling(self):
        self.compare_tokens(
            "$ single ruling",
            ["DOLLAR", "SINGLE", "RULING"]
        )

    def test_described_object(self):
        self.compare_tokens(
            "@object An object that fits no other category\n",
            ["OBJECT", "ID", "NEWLINE"],
            [None, "An object that fits no other category"]
        )

    def test_nested_object(self):
        self.compare_tokens(
            "@tablet\n" +
            "@obverse\n",
            ["TABLET", "NEWLINE", "OBVERSE", "NEWLINE"]
        )

    def test_object_line(self):
        self.compare_tokens(
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

    def test_composite(self):
        self.compare_tokens(
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

    def test_multilingual_interlinear(self):
        self.compare_tokens(
            "@tablet\n" +
            "@obverse\n" +
            "1. dim₃#-me-er# [...]\n" +
            "#lem: diŋir[deity]N; u\n" +
            "== %sb DINGIR-MEŠ GAL#-MEŠ# [...]\n" +
            "#lem: ilū[god]N; rabûtu[great]AJ; u\n" +
            "# ES dim₃-me-er = diŋir\n" +
            "|| A o ii 15\n",
            ['TABLET',"NEWLINE"] +
            ["OBVERSE","NEWLINE"] +
            ["LINELABEL"] + ['ID']*2 + ["NEWLINE"] +
            ["LEM"] + ["ID","SEMICOLON"] + ["ID"] + ["NEWLINE"] +
            ["MULTILINGUAL","ID"]+["ID"]*3 + ["NEWLINE"] +
            ["LEM"] + ["ID","SEMICOLON"]*2 + ["ID"] + ["NEWLINE"] +
            ["NEWLINE"] +
            ["PARBAR", "ID", "ID", "ID", "ID", "NEWLINE"]
        )

    def test_strict_in_parallel(self):
        self.compare_tokens(
            "@translation parallel en project\n" +
            "$ reverse blank",
             ["TRANSLATION", "PARALLEL", "ID", "PROJECT", "NEWLINE"]+
             ["DOLLAR", "REFERENCE", "BLANK"]
        )


    def test_strict_in_labelled_parallel(self):
        self.compare_tokens(
            "@translation labeled en project\n" +
            "$ reverse blank",
             ["TRANSLATION", "LABELED", "ID", "PROJECT", "NEWLINE"]+
             ["DOLLAR", "REFERENCE", "BLANK"]
    )

    def test_punctuated_translation(self):
        self.compare_tokens(
            "@translation parallel en project\n" +
            "1. 'What is going on?', said the King!\n",
             ["TRANSLATION", "PARALLEL", "ID", "PROJECT", "NEWLINE"] +
             ["LINELABEL","ID","NEWLINE"],
             [None, None, "en", None, None] +
             ["1","'What is going on?', said the King!",None]
        )

    def test_translation_note(self):
        self.compare_tokens(
            "@translation parallel en project\n" +
            "@reverse\n" +
            "#note: reverse uninscribed\n",
            ["TRANSLATION", "PARALLEL", "ID", "PROJECT", "NEWLINE"] +
            ["REVERSE","NEWLINE"] +
            ["NOTE","ID","NEWLINE"]
        )