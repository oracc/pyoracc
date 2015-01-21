# -*- coding: utf-8 -*-

from unittest import TestCase

from nose.tools import assert_equal  # @UnresolvedImport

from pyoracc.atf.atffile import AtfFile
from pyoracc.test.fixtures import belsunu

from ...atf.atflex import AtfLexer
from ...atf.atfyacc import AtfParser


class testSerializer(TestCase):
    
    def setUp(self):
        """
        Initialize lexer and parser.
        """
        self.lexer = AtfLexer().lexer
        self.parser =  AtfParser().parser

    def parse_str(self, content):
        """
        Parse a given string.
        """
        if content[-1] != '\n':
            content += "\n"
        return self.parser.parse(content, lexer=self.lexer)

    def test_code_from_string(self):
        """
        Parse a given text code and check if serializing works for the code/description case
        """
        text = self.parse_str("&X001001 = JCS 48, 089\n")
        serialized_text = text.__str__()
        assert_equal(serialized_text.strip()+"\n", "&X001001 = JCS 48, 089\n")

    def test_code_from_file(self):
        """
        Parse an ATF file and serialize text.
        Check file's first line and serialization coincide.
        """
        belsunu_content = belsunu()
        belsunu_first_line = belsunu_content.partition("\n")[0]
        afile = AtfFile(belsunu_content)
        serialized_text = afile.text.__str__()
        assert_equal(serialized_text.strip(), belsunu_first_line)