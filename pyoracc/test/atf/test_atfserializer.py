# -*- coding: utf-8 -*-
import codecs
from unittest import TestCase

from nose.tools import assert_equal  # @UnresolvedImport

from pyoracc.atf.atffile import AtfFile
from pyoracc.test.fixtures import belsunu, output_filepath

from ...atf.atflex import AtfLexer
from ...atf.atfyacc import AtfParser


class testSerializer(TestCase):
    
    def setUp(self):
        """
        Initialize lexer and parser.
        """
        self.lexer = AtfLexer().lexer
        self.parser =  AtfParser().parser
        
    def parse(self, any_str):
        """
        Parse input string, could be just a line or a whole file content.
        """
        return AtfFile(any_str)
    
    def serialize(self, any_object):
        """
        Serialize input object, from a simple lemma to a whole AtfFile object.
        """
        return any_object.__str__()
    
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
        Parse belsunu.atf, then serialize, parse again, serialize again, compare. 
        Comparing serialized output with input file would bring up differences that might not be significant (white spaces, newlines, etc).
        The solution is to parse again the serialized file, serialize again, then compare the two serializations.
        """
        serialized_1 = self.parse_then_serialize(belsunu())
        serialized_2 = self.parse_then_serialize(serialized_1)
        self.save_file(serialized_1, output_filepath("belsunu.atf"))
        assert_equal(serialized_1, serialized_2)
        
    def test_text_code_and_description(self):
        """
        Check if serializing works for the code/description case - first line of ATF texts.
        Note the parser always returns an AtfFile object, even when it's not ATF-compliant.
        """
        atf = self.parse("&X001001 = JCS 48, 089\n")
        serialized = self.serialize(atf)
        assert_equal(serialized.strip()+"\n", "&X001001 = JCS 48, 089\n")
        
#     def test_text_project(self):
#         """
#         Check if serializing works for the project lines.
#         Note the parser always returns an AtfFile object, even when it's not ATF-compliant.
#         """
#         serialized = self.parse_then_serialize("#project: cams/gkab\n")
#         assert_equal(serialized.strip()+"\n", "#project: cams/gkab\n")
# 
#     def test_text_language(self):
#     
#     def test_text_protocols(self):
    
        
        
        