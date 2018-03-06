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

import codecs
import sys
from pyoracc.atf.cdli.atflex import AtfCDLILexer
from pyoracc.atf.cdli.atfyacc import AtfCDLIParser
from pyoracc.atf.common.atflex import AtfLexer
from pyoracc.atf.common.atfyacc import AtfParser
from pyoracc.atf.oracc.atflex import AtfOraccLexer
from pyoracc.atf.oracc.atfyacc import AtfOraccParser
from mako.template import Template


class AtfFile(object):

    template = Template("${text.serialize()}")

    def __init__(self, content, atftype='oracc'):
        self.content = content
        self.type = atftype
        if content[-1] != '\n':
            content += "\n"
        if atftype == 'cdli':
            lexer = AtfCDLILexer().lexer
            parser = AtfCDLIParser().parser
        elif atftype == 'oracc':
            lexer = AtfOraccLexer().lexer
            parser = AtfOraccParser().parser
        else:
            lexer = AtfLexer().lexer
            parser = AtfParser().parser
        self.text = parser.parse(content, lexer=lexer)

    def __str__(self):
        return AtfFile.template.render_unicode(**vars(self))

    def serialize(self):
        return AtfFile.template.render_unicode(**vars(self))


def _debug_lex_and_yac_file(atftype, infile, debug=0, skipinvalid=False):
    text = codecs.open(infile, encoding='utf-8-sig').read()

    if not (atftype == "cdli" or atftype == "oracc"):
        print "Select either \"cdli\" or \"oracc\""
        return

    # CDLI Code
    if atftype == "cdli":
        lexer = AtfCDLILexer(debug=debug, skipinvalid=skipinvalid).lexer
        lexer.input(text)
        #for tok in lexer:
        #    print(tok)
        print("Lexed file")
        lexer = AtfCDLILexer(debug=0).lexer
        parser = AtfCDLIParser(debug=debug).parser

    if atftype == "oracc":
        lexer = AtfOraccLexer(debug=debug, skipinvalid=skipinvalid).lexer
        lexer.input(text)
        #for tok in lexer:
        #    print(tok)
        print("Lexed file")
        lexer = AtfOraccLexer(debug=0).lexer
        parser = AtfOraccParser(debug=debug).parser

    parser.parse(text, lexer=lexer)
    print("Parsed file")


if __name__ == "__main__":
    _debug_lex_and_yac_file(sys.argv[1], sys.argv[2], sys.argv[3])
