# -*- coding: utf-8 -*-

from unittest import TestCase, skip

from ...model.text import Text
from ...model.line import Line
from ...model.state import State
from ...model.translation import Translation
from ...model.link import Link
from ...model.link_reference import LinkReference
from ...model.oraccobject import OraccObject
from ...model.oraccnamedobject import OraccNamedObject
from ...model.multilingual import Multilingual
from ...model.composite import Composite
from ...atf.atfyacc import AtfParser
from ...atf.atflex import AtfLexer
from nose.tools import assert_in, assert_equal, assert_is_instance
from itertools import izip, repeat


class testParser(TestCase):
    def setUp(self):
        self.lexer = AtfLexer().lexer

    def try_parse(self, content):
        self.parser = AtfParser().parser
        return self.parser.parse(content, lexer=self.lexer)

    def test_code(self):
        text = self.try_parse("&X001001 = JCS 48, 089\n")
        assert_is_instance(text, Text)
        assert_equal(text.description, "JCS 48, 089")
        assert_equal(text.code, "X001001")

    def test_text_project(self):
        text = self.try_parse(
            "&X001001 = JCS 48, 089\n" +
            "#project: cams/gkab\n"
        )
        assert_is_instance(text, Text)
        assert_equal(text.code, "X001001")
        assert_equal(text.project, "cams/gkab")

    def test_text_language(self):
        text = self.try_parse(
            "&X001001 = JCS 48, 089\n" +
            "#atf: lang akk-x-stdbab\n"
        )
        assert_is_instance(text, Text)
        assert_equal(text.code, "X001001")
        assert_equal(text.language, "akk-x-stdbab")

    @skip("No support for key protocol")
    def test_key_protocol(self):
        text = self.try_parse(
            "&X001001 = JCS 48, 089\n" +
            "#key: cdli=ND 02688\n"
        )
        # No assertion, we're not parsing keys yet
        assert False

    @skip("No support for mylines protocol")
    def test_mylines_protocol(self):
        text = self.try_parse(
            "&X001001 = JCS 48, 089\n" +
            "#atf: use mylines\n"
        )
        # No assertion, we're not parsing mylines yet
        assert False

    @skip("No support for lexical protocol")
    def test_lexical_protocol(self):
        text = self.try_parse(
            "&X001001 = JCS 48, 089\n" +
            "#atf: use lexical\n"
        )
        # No assertion, we're not parsing keys yet
        assert False

    def test_text_protocol_language(self):
        text = self.try_parse(
            "&X001001 = JCS 48, 089\n" +
            "#project: cams/gkab\n" +
            "#atf: lang akk-x-stdbab\n"
        )
        assert_is_instance(text, Text)
        assert_equal(text.code, "X001001")
        assert_equal(text.project, "cams/gkab")
        assert_equal(text.language, "akk-x-stdbab")

    def test_simple_object(self):
        obj = self.try_parse(
            "@tablet\n"
        )
        assert_is_instance(obj, OraccObject)
        assert_equal(obj.objecttype, "tablet")

    def test_generic_object(self):
        obj = self.try_parse(
            "@object That fits no other category\n"
        )
        assert_is_instance(obj, OraccNamedObject)
        assert_equal(obj.objecttype, "object")
        assert_equal(obj.name, "That fits no other category")

    def test_flagged_object(self):
        obj = self.try_parse(
            "@object which is remarkable and broken!#\n"
        )
        assert_is_instance(obj, OraccNamedObject)
        assert_equal(obj.objecttype, "object")
        assert_equal(obj.name, "which is remarkable and broken")
        assert(obj.broken)
        assert(obj.remarkable)
        assert(not obj.collated)

    def test_flagged_object(self):
        obj = self.try_parse(
            "@tablet\n@column 2'*\n"
        )
        assert_is_instance(obj.children[0], OraccNamedObject)
        assert_equal(obj.children[0].objecttype, "column")
        assert_equal(obj.children[0].name, "2'")
        assert(obj.children[0].collated)
        assert(not obj.children[0].broken)

    def test_substructure(self):
        obj = self.try_parse(
            "@tablet\n" +
            "@obverse\n"
        )
        assert_is_instance(obj.children[0], OraccObject)
        assert_equal(obj.children[0].objecttype, "obverse")

    def test_triple_substructure(self):
        art = self.try_parse(
            "&X001001 = My Text\n" +
            "@tablet\n" +
            "@obverse\n"
        )
        assert_is_instance(art, Text)
        assert_is_instance(art.children[0], OraccObject)
        assert_is_instance(art.children[0].children[0], OraccObject)
        assert_equal(art.children[0].children[0].objecttype, "obverse")

    def test_two_surfaces(self):
        art = self.try_parse(
            "&X001001 = My Text\n" +
            "@tablet\n" +
            "@obverse\n" +
            "@reverse\n"
        )
        assert_is_instance(art, Text)
        assert_is_instance(art.children[0], OraccObject)
        assert_is_instance(art.children[0].children[0], OraccObject)
        assert_equal(art.children[0].children[0].objecttype, "obverse")
        assert_equal(art.children[0].children[1].objecttype, "reverse")

    def test_two_inscribed_surfaces(self):
        art = self.try_parse(
            "&X001001 = My Text\n" +
            "@tablet\n" +
            "@obverse\n" +
            "1. line one\n" +
            "@reverse\n" +
            "2. line two\n"
        )
        assert_is_instance(art, Text)
        assert_is_instance(art.children[0], OraccObject)
        assert_is_instance(art.children[0].children[0], OraccObject)
        assert_equal(art.children[0].children[0].objecttype, "obverse")
        assert_equal(art.children[0].children[1].objecttype, "reverse")
        assert_is_instance(art.children[0].children[0].children[0], Line)
        assert_is_instance(art.children[0].children[1].children[0], Line)

    def test_complex_substructure(self):
        art = self.try_parse(
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
        assert_is_instance(art, Text)
        tablet = art.children[0]
        assert_is_instance(tablet, OraccObject)
        case = art.children[1]
        assert_equal(len(art.children), 2)
        obverse = tablet.children[0]
        assert_is_instance(obverse, OraccObject)
        reverse = tablet.children[1]
        assert_equal(len(tablet.children), 2)
        caseobverse = case.children[0]
        assert_equal(len(case.children), 1)
        lines = (obverse.children[:] +
                 reverse.children[:] +
                 caseobverse.children[:])
        assert_equal(len(lines), 4)
        assert_equal(lines[1].lemmas[1], "two")
        assert_equal(lines[2].notes[0].content, "Note to line three")


    def test_complex_substructure_2(self):
        art = self.try_parse(
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
        assert_is_instance(art, Text)
        tablet = art.children[0]
        assert_is_instance(tablet, OraccObject)
        assert_equal(len(art.children), 1)
        obverse = tablet.children[0]
        assert_is_instance(obverse, OraccObject)
        reverse = tablet.children[2]
        assert_equal(len(tablet.children), 4)
        bottom = tablet.children[1] 
        # Is this wrong -- should tops and bottoms 
        # really be a lower nesting level?
        translation = tablet.children[3]
        lines = (obverse.children[:] +
                 bottom.children[:] +
                 reverse.children[:])
        assert_equal(len(lines), 4)
        assert_equal(lines[1].lemmas[1], "two")
        assert_equal(lines[3].notes[0].content, "Note to line four")
        assert_is_instance(translation,Translation)

    def test_line(self):
        art = self.try_parse(
            "@tablet\n" +
            "@obverse\n" +
            "1.    [MU] 1.03-KAM {iti}AB GE₆ U₄ 2-KAM\n"
        )
        assert_equal(len(art.children[0].children[0].words), 6)

    def test_line_lemmas(self):
        art = self.try_parse(
            "@tablet\n" +
            "@obverse\n" +
            "1.    [MU] 1.03-KAM {iti}AB GE₆ U₄ 2-KAM\n"
            "#lem: šatti[year]N; n; Ṭebetu[1]MN; " +
            "mūša[at night]AV; ūm[day]N; n\n"
        )
        assert_equal(len(art.children[0].children[0].words), 6)
        assert_equal(len(art.children[0].children[0].lemmas), 6)

    def test_ruling(self):
        art = self.try_parse(
            "@tablet\n" +
            "@obverse\n" +
            "$ triple ruling\n"
        )
        assert_equal(art.children[0].children[0].count, 3)

    def test_uncounted_ruling(self):
        art = self.try_parse(
            "@tablet\n" +
            "@obverse\n" +
            "$ ruling\n"
        )
        assert_equal(art.children[0].children[0].count, 1)

    def test_line_ruling(self):
        art = self.try_parse(
            "@tablet\n" +
            "@obverse\n" +
            "$ double line ruling\n"
        )
        assert_equal(art.children[0].children[0].count, 2)

    def test_ruling_on_object_no_surface(self):
        art = self.try_parse(
            "@tablet\n" +
            "$ single ruling\n",
        )
        # Should default to an obverse surface
        assert_equal(art.children[0].objecttype,"obverse")
        assert_equal(art.children[0].children[0].count, 1)

    def test_ruling_on_labeled_translation(self):
        art = self.try_parse(
            "@tablet\n" +
            "@translation labeled en project\n" +
            "$ single ruling\n" +
            "@label 1\n" +
            "Some content\n\n"
        )
        # Should default to an obverse surface
        assert_equal(art.children[0].children[0].count, 1)

    def test_comment(self):
        art = self.try_parse(
            "@tablet\n" +
            "@obverse\n" +
            "# A comment\n"
        )
        assert_equal(len(art.children[0].children), 0)

    def test_note(self):
        art = self.try_parse(
            "@tablet\n" +
            "@obverse\n" +
            "3.    U₄!-BI? 20* [(ina)] 9.30 ina(DIŠ) MAŠ₂!(BAR)\n" +
            "#note: Note to line.\n"
        )
        assert_equal(art.children[0].children[0].notes[0].content,
                     "Note to line."
                     )

    def test_surface_note(self):
        art = self.try_parse(
            "@tablet\n" +
            "@obverse\n" +
            "#note: Note to surface.\n"
        )
        assert_equal(art.children[0].children[0].content,
                     "Note to surface.")

    def test_loose_dollar(self):
        art = self.try_parse(
            "@tablet\n" +
            "@obverse\n" +
            "3.    U₄!-BI? 20* [(ina)] 9.30 ina(DIŠ) MAŠ₂!(BAR)\n" +
            "$ (something loose)\n"
        )
        assert_equal(art.children[0].children[1].loose,
                     "(something loose)"
                     )

    def test_strict_dollar_simple(self):
        art = self.try_parse(
            "@tablet\n" +
            "@obverse\n" +
            "$case blank\n"
        )
        assert_equal(art.children[0].children[0].state, "blank")
        assert_equal(art.children[0].children[0].scope, "case")

    def test_strict_dollar_plural_difficult(self):
        art = self.try_parse(
            "@tablet\n" +
            "@obverse\n" +
            "$5-7 lines blank\n"
        )
        assert_equal(art.children[0].children[0].state, "blank")
        assert_equal(art.children[0].children[0].scope, "lines")
        assert_equal(art.children[0].children[0].extent, "5-7")

    def test_strict_dollar_in_lines(self):
        art = self.try_parse(
            "@tablet\n" +
            "@obverse\n" +
            "48.   lip#-tar-rik ina at-ma-ni šu-bat ki#-[iṣ-ṣi]\n" +
            "$ 3 lines broken\n" +
            "53.   ta#-[mit] iq#-bu-šu DINGIR an-[na i-pu-ul]\n"
        )
        content = art.children[0].children
        assert_is_instance(content[0], Line)
        assert_is_instance(content[2], Line)
        assert_equal(content[1].state, "broken")
        assert_equal(content[1].scope, "lines")
        assert_equal(content[1].extent, "3")

    def test_strict_dollar_singular_difficult(self):
        art = self.try_parse(
            "@tablet\n" +
            "@obverse\n" +
            "$rest of bulla blank\n"
        )
        assert_equal(art.children[0].children[0].state, "blank")
        assert_equal(art.children[0].children[0].scope, "bulla")
        assert_equal(art.children[0].children[0].extent, "rest of")

    def test_strict_dollar_plural_qualified(self):
        art = self.try_parse(
            "@tablet\n" +
            "@obverse\n" +
            "$at most 5 columns blank\n"
        )
        assert_equal(art.children[0].children[0].state, "blank")
        assert_equal(art.children[0].children[0].scope, "columns")
        assert_equal(art.children[0].children[0].extent, "5")
        assert_equal(art.children[0].children[0].qualification, "at most")

    def test_strict_dollar_labelled(self):
        art = self.try_parse(
            "@tablet\n" +
            "@obverse\n" +
            "$rest of column 1 blank\n"
        )
        assert_equal(art.children[0].children[0].state, "blank")
        assert_equal(art.children[0].children[0].scope, "column 1")
        assert_equal(art.children[0].children[0].extent, "rest of")

    def test_strict_dollar_no_scope(self):
        art = self.try_parse(
            "@tablet\n" +
            "@obverse\n" +
            "$rest blank\n"
        )
        assert_equal(art.children[0].children[0].state, "blank")
        assert_equal(art.children[0].children[0].scope, None)
        assert_equal(art.children[0].children[0].extent, "rest")
   
    def test_strict_dollar_singular_exception(self):
        art = self.try_parse(
            "@tablet\n" +
            "@obverse\n" +
            "$ 1 line traces\n"
        )
        dollar=art.children[0].children[0]
        assert_equal(dollar.state, "traces")
        assert_equal(dollar.scope, "line")
        assert_equal(dollar.extent, "1")

    def test_strict_dollar_start_of_exception(self):
        art = self.try_parse(
            "@tablet\n" +
            "@obverse\n" +
            "$ start of column missing\n",
        )
        assert_equal(art.children[0].children[0].state, "missing")
        assert_equal(art.children[0].children[0].scope, "column")
        assert_equal(art.children[0].children[0].extent, "start of")

    def test_strict_dollar_start_of_exception(self):
        art = self.try_parse(
            "@tablet\n" +
            "@obverse\n" +
            "$ Lacuna\n",
        )
        assert_equal(art.children[0].children[0].state, "Lacuna")
        assert_equal(art.children[0].children[0].scope, None)
        assert_equal(art.children[0].children[0].extent, None)

    def test_translation_intro(self):
        art = self.try_parse(
            "@tablet\n" +
            "@translation parallel en project\n"
        )
        assert_is_instance(art.children[0], Translation)

    def test_translation_text(self):
        art = self.try_parse(
            "@tablet\n" +
            "@translation parallel en project\n" +
            "@obverse\n"
            "1.    Year 63, Ṭebetu (Month X), night of day 2\n"
        )
        assert_is_instance(art.children[0], Translation)
        assert_equal(art.children[0].children[0].children[0].label, '1')
        assert_equal(art.children[0].children[0].children[0].words[0],
                     "Year 63, Ṭebetu (Month X), night of day 2")

    def test_translation_eneded(self):
        art = self.try_parse(
            "@tablet\n" +
            "@translation labeled en project\n" +
            "@(1) Year 63, Ṭebetu (Month X), night of day 2\n" +
            "@end translation\n"
        )
        assert_is_instance(art.children[0], Translation)
        assert_equal(art.children[0].children[0].label.label, ['1'])
        assert_equal(art.children[0].children[0].words[0],
                     "Year 63, Ṭebetu (Month X), night of day 2")

    def test_translation_labeled_text(self):
        art = self.try_parse(
            "@tablet\n" +
            "@translation labeled en project\n" +
            "@label o 4\n"
            "Then it will be taken for the rites and rituals.\n\n"
        )
        assert_is_instance(art.children[0], Translation)
        assert_equal(art.children[0].children[0].label.label, ['o','4'])
        assert_equal(art.children[0].children[0].words[0],
                     "Then it will be taken for the rites and rituals.")

    def test_translation_labeled_text2(self):
        art = self.try_parse(
            "@tablet\n" +
            "@translation labeled en project\n" +
            "@label o 2 - o 3\n" +
            "an expert will carefully inspect an ungelded bull.\n\n")
        assert_is_instance(art.children[0], Translation)
        assert_equal(art.children[0].children[0].label.label, ['o', '2'])
        assert_equal(art.children[0].children[0].label.rangelabel, ['o', '3'])
        assert_equal(art.children[0].children[0].words[0],
                     "an expert will carefully inspect an ungelded bull.")

    def test_translation_label_plus(self):
        art = self.try_parse(
            "@tablet\n" +
            "@translation labeled en project\n" +
            "@label+ o 28\n" +
            "You extinguish the fire on the altar with beer\n\n"
        )
        assert(art.children[0].children[0].label.plus)

    def test_translation_labeled_dashlabel(self):
        art = self.try_parse(
            "@tablet\n" +
            "@translation labeled en project\n" +
            "@label o 14-15 - o 20\n" +
            "You strew all (kinds of) seed.\n\n",
        )
        assert_is_instance(art.children[0], Translation)
        assert_equal(art.children[0].children[0].label.label, ['o', '14-15'])
        assert_equal(art.children[0].children[0].label.rangelabel, ['o', '20'])
        assert_equal(art.children[0].children[0].words[0],
                     "You strew all (kinds of) seed.")

    def test_translation_labeled_noted_text(self):
        art = self.try_parse(
            "@tablet\n" +
            "@translation labeled en project\n" +
            "@label r 8\n" +
            "The priest says the gods have performed these actions. ^1^\n\n" +
            "@note ^1^ Parenthesised text follows Neo-Assyrian source\n"
        )
        assert_is_instance(art.children[0], Translation)
        assert_equal(art.children[0].children[0].label.label, ['r', '8'])
        assert_equal(art.children[0].children[0].words[0],
                     "The priest says the gods have performed these actions.")
        assert_equal(art.children[0].children[0].references[0],
                     "1")
        assert_equal(art.children[0].children[0].notes[0].references[0],
                     "1")
        assert_equal(art.children[0].children[0].notes[0].content,
                     "Parenthesised text follows Neo-Assyrian source")

    def test_translation_links(self):
        art = self.try_parse(
            "@tablet\n" +
            "@translation parallel en project\n" +
            "@obverse\n"
            "1.    Year 63, Ṭebetu (Month X), night of day 2:^1^\n\n"
            "@note ^1^ A note to the translation.\n"
        )
        assert_is_instance(art.children[0], Translation)
        assert_equal(art.children[0].children[0].children[0].label, '1')
        assert_equal(art.children[0].children[0].children[0].words[0],
                     "Year 63, Ṭebetu (Month X), night of day 2:")
        assert_equal(art.children[0].children[0].children[0].references[0],
                     "1")
        assert_equal(art.children[0].children[0]
                        .children[0].notes[0].references[0],
                     "1")

    def test_translation_poundnote(self):
        art = self.try_parse(
            "@tablet\n" +
            "@translation parallel en project\n" +
            "@obverse\n"
            "1.    Year 63, Ṭebetu (Month X), night of day 2\n"
            "#note: A note to the translation.\n"
        )
        assert_equal(art.children[0].children[0]
                        .children[0].notes[0].content,
                     "A note to the translation.")

    def test_translation_labeled_atlabel(self):
        art = self.try_parse(
            "@tablet\n" +
            "@translation labeled en project\n" +
            "@(o 20) You strew all (kinds of) seed.\n" +
            "@(o i 2) No-one will occupy the king of Akkad's throne.\n")
        l1= art.children[0].children[0]
        assert_equal(l1.label.label,["o","20"])
        assert_equal(l1.words[0],
                     "You strew all (kinds of) seed.")
        l2= art.children[0].children[1]
        assert_equal(l2.label.label,["o","i","2"])
        assert_equal(l2.words[0],
                     "No-one will occupy the king of Akkad's throne.")

    def test_default_surface(self):
        text = self.try_parse(
            "&Q002769 = SB Anzu 1\n" +
            "@tablet\n" +
            "1.   bi#-in šar da-ad-mi šu-pa-a na-ram {d}ma#-mi\n"
        )
        assert_equal(text.children[0].objecttype, "tablet")
        assert_equal(text.children[0].children[0].objecttype, "obverse")

    def test_default_object(self):
        text = self.try_parse(
            "&Q002769 = SB Anzu 1\n" +
            "@obverse\n" +
            "1.   bi#-in šar da-ad-mi šu-pa-a na-ram {d}ma#-mi\n"
        )
        assert_equal(text.children[0].objecttype, "tablet")
        assert_equal(text.children[0].children[0].objecttype, "obverse")

    def test_default_object_surface(self):
        text = self.try_parse(
            "&Q002769 = SB Anzu 1\n" +
            "1.   bi#-in šar da-ad-mi šu-pa-a na-ram {d}ma#-mi\n"
        )
        assert_equal(text.children[0].objecttype, "tablet")
        assert_equal(text.children[0].children[0].objecttype, "obverse")

    def test_default_object_surface_dollar(self):
        text = self.try_parse(
            "&Q002769 = SB Anzu 1\n" +
            "$ 5 lines broken\n"
        )
        assert_equal(text.children[0].objecttype, "tablet")
        assert_equal(text.children[0].children[0].objecttype, "obverse")
        assert_is_instance(text.children[0].children[0].children[0], State)

    def test_default_surface_dollar(self):
        text = self.try_parse(
            "&Q002769 = SB Anzu 1\n" +
            "@tablet\n" +
            "$ 5 lines broken\n"
        )
        assert_equal(text.children[0].objecttype, "tablet")
        assert_equal(text.children[0].children[0].objecttype, "obverse")
        assert_is_instance(text.children[0].children[0].children[0], State)

    def test_default_object_dollar(self):
        text = self.try_parse(
            "&Q002769 = SB Anzu 1\n" +
            "@obverse\n" +
            "$ 5 lines broken\n"
        )
        assert_equal(text.children[0].objecttype, "tablet")
        assert_equal(text.children[0].children[0].objecttype, "obverse")
        assert_is_instance(text.children[0].children[0].children[0], State)

    def test_composite(self):
        composite = self.try_parse(
            "&Q002769 = SB Anzu 1\n" +
            "@composite\n" +
            "#project: cams/gkab\n" +
            "1.   bi#-in šar da-ad-mi šu-pa-a na-ram {d}ma#-mi\n" +
            "&Q002770 = SB Anzu 2\n" +
            "#project: cams/gkab\n" +
            "1.   bi-riq ur-ha šuk-na a-dan-na\n"
        )
        assert_is_instance(composite, Composite)
        assert_is_instance(composite.texts[0], Text)
        assert_is_instance(composite.texts[1], Text)

    def test_implicit_composite(self):
        composite = self.try_parse(
            "&Q002769 = SB Anzu 1\n" +
            "#project: cams/gkab\n" +
            "1.   bi#-in šar da-ad-mi šu-pa-a na-ram {d}ma#-mi\n" +
            "&Q002770 = SB Anzu 2\n" +
            "#project: cams/gkab\n" +
            "1.   bi-riq ur-ha šuk-na a-dan-na\n"
        )
        assert_is_instance(composite, Composite)
        assert_is_instance(composite.texts[0], Text)
        assert_is_instance(composite.texts[1], Text)

    def test_translated_composite(self):
        composite = self.try_parse(
            "&Q002769 = SB Anzu 1\n" +
            "#project: cams/gkab\n" +
            "1.   bi#-in šar da-ad-mi šu-pa-a na-ram {d}ma#-mi\n" +
            "@translation labeled en project\n"
            "@(1) This is English\n\n\n"
            "&Q002770 = SB Anzu 2\n" +
            "#project: cams/gkab\n" +
            "1.   bi-riq ur-ha šuk-na a-dan-na\n"
        )
        assert_is_instance(composite, Composite)
        assert_is_instance(composite.texts[0], Text)
        assert_is_instance(composite.texts[1], Text)

    def test_link_declaration(self):
        text = self.try_parse(
            "&Q002769 = SB Anzu 1\n" +
            "#link: def A = P363716 = TCL 06, 44\n" +
            "@tablet\n" +
            "1. Some text\n"
        )
        link = text.links[0]
        assert_is_instance(link, Link)
        assert_equal(link.label, "A")
        assert_equal(link.code, "P363716")
        assert_equal(link.description, "TCL 06, 44")

    def test_link_reference_simple(self):
        text = self.try_parse(
            "@tablet\n" +
            "1. Some text\n" +
            ">>A Tab.I, 102\n" +
            "2. Some more text\n"
        )
        link = text.children[0].children[0].links[0]
        assert_is_instance(link, LinkReference)
        assert_equal(link.target, "A")
        assert_equal(link.operator, ">>")
        assert_equal(link.label, ["Tab.I", "102"])

    def test_link_reference_comma(self):
        text = self.try_parse(
            "@tablet\n" +
            "1. Some text\n" +
            "|| A o ii 10\n" +
            "2. Some more text\n"
        )
        link = text.children[0].children[0].links[0]
        assert_is_instance(link, LinkReference)
        assert_equal(link.target, "A")
        assert_equal(link.operator, "||")
        assert_equal(link.label, ["o", "ii", "10"])

    def test_link_reference_range(self):
        text = self.try_parse(
            "@tablet\n" +
            "1. Some text\n" +
            ">> A o ii 10 - o ii 15\n" +
            "2. Some more text\n"
        )
        link = text.children[0].children[0].links[0]
        assert_equal(link.target, "A")
        assert_equal(link.operator, ">>")
        assert_equal(link.label, ["o", "ii", "10"])
        assert_equal(link.rangelabel, ["o", "ii", "15"])

    def test_multilingual_interlinear(self):
        text=self.try_parse(
            "@tablet\n" +
            "@obverse\n" +
            "1. dim₃#-me-er# [...]\n" +
            "#lem: diŋir[deity]N; u\n" +
            "== %sb DINGIR-MEŠ GAL#-MEŠ# [...]\n" +
            "#lem: ilū[god]N; rabûtu[great]AJ; u\n" +
            "# ES dim₃-me-er = diŋir\n" +
            "|| A o ii 15\n")
        multilingual=text.children[0].children[0]
        assert_is_instance(multilingual, Multilingual)
        assert_equal(len(multilingual.lines),2)
        assert_equal(len(multilingual.lines[None].words),2)
        assert_equal(len(multilingual.lines[None].lemmas),2)
        assert_equal(len(multilingual.lines["sb"].words),3)
        assert_equal(len(multilingual.lines["sb"].lemmas),3)


    def test_translation_heading(self):
        text=self.try_parse(
            "@tablet\n" +
            "@translation parallel en project\n" +
            "@h1 A translation heading\n"
        )
        assert_equal(len(text.children[0].children),1)
        assert_equal(text.children[0].children[0].objecttype,'h1')

    def test_heading(self):
        text=self.try_parse(
            "@tablet\n" +
            "@h1 A heading\n"
        )
        assert_equal(text.children[0].objecttype,'h1')
