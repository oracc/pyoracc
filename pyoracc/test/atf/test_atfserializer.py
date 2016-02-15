# -*- coding: utf-8 -*-
import codecs
from unittest import TestCase, skip
import pytest

from pyoracc.atf.atffile import AtfFile
from pyoracc.test.fixtures import belsunu, output_filepath

from ...atf.atflex import AtfLexer
from ...atf.atfyacc import AtfParser
from pyoracc.model.line import Line


class testSerializer(TestCase):

    def setUp(self):
        """
        Initialize lexer and parser.
        """
        self.lexer = AtfLexer().lexer
        self.parser = AtfParser().parser

    def parse(self, any_str):
        """
        Parse input string, could be just a line or a whole file content.
        """
        parsed = AtfFile(any_str)
        return parsed

    def serialize(self, any_object):
        """
        Serialize input object, from a simple lemma to a whole AtfFile object.
        """
        serialized = any_object.serialize()
        return serialized

    def parse_then_serialize(self, any_str):
        """
        Shorthand for testing serialization.
        """
        return self.serialize(self.parse(any_str))

    def open_file(self, filename):
        """
        Open serialized file and output contents
        """
        return codecs.open(filename, "r", "utf-8").read()

    def save_file(self, content, filename):
        """
        Write serialized file on disk
        """
        serialized_file = codecs.open(filename, "w", "utf-8")
        serialized_file.write(content)
        serialized_file.close()

    def test_belsunu_serializer(self):
        """
        Parse belsunu.atf, then serialize, parse again, serialize again,
        compare.
        Comparing serialized output with input file would bring up differences
        that might not be significant (white spaces, newlines, etc).
        The solution is to parse again the serialized file, serialize again,
        then compare the two serializations.
        """
        serialized_1 = self.parse_then_serialize(belsunu())
        self.save_file(serialized_1, output_filepath("belsunu.atf"))
        serialized_2 = self.parse_then_serialize(serialized_1)
        assert serialized_1 == serialized_2

    @pytest.mark.xfail
    def test_line_word(self):
        """
        Get a sample word with unicode chars and check serialization is
        correct.
        """
        line = Line("1")
        line.words.append(u"\u2086")
        line_ser = line.serialize()
        assert line_ser == "1.\t" + u"\u2086"

    def test_line_words(self):
        """
        Get a sample line of words with unicode chars and test serialization.
        1. [MU] 1.03-KAM {iti}AB GE₆ U₄ 2-KAM
        """
        atf_file = AtfFile(belsunu())
        uline = atf_file.text.children[0].children[0].children[0]
        uwords = uline.words
        gold = [u'[MU]', u'1.03-KAM', u'{iti}AB', u'GE\u2086', u'U\u2084',
                u'2-KAM']
        assert uwords == gold

    def test_line_lemmas(self):
        """
        Get a sample line of lemmas with unicode chars and test serialization.
        šatti[year]N; n; Ṭebetu[1]MN; mūša[at night]AV; ūm[day]N; n
        """
        atf_file = AtfFile(belsunu())
        uline = atf_file.text.children[0].children[0].children[0]
        ulemmas = uline.lemmas
        gold = [u' \u0161atti[year]N', u'n', u'\u1e6cebetu[1]MN',
                u'm\u016b\u0161a[at night]AV', u'\u016bm[day]N', u'n']
        assert ulemmas == gold


# TODO: Build list of atf files for testing and make a test to go through the
# list of test and try serializing each of them.
    @pytest.mark.xfail
    def test_text_code_and_description(self):
        """
        Check if serializing works for the code/description case - first line
        of ATF texts.
        Note the parser always returns an AtfFile object, even when it's not
        ATF-compliant.
        """
        atf = self.parse("&X001001 = JCS 48, 089\n")
        serialized = self.serialize(atf)
        assert serialized.strip()+"\n" == "&X001001 = JCS 48, 089\n"

    @pytest.mark.xfail
    def test_text_project(self):
        """
        Check if serializing works for the project lines.
        Note the parser always returns an AtfFile object, even when it's not
        ATF-compliant.
        """
        serialized = self.parse_then_serialize("#project: cams/gkab\n")
        assert serialized.strip()+"\n" == "#project: cams/gkab\n"

    @skip("test_text_language is not implemented yet")
    def test_text_language(self):
        pass

    @skip("test_text_protocols is not implemented yet")
    def test_text_protocols(self):
        pass
