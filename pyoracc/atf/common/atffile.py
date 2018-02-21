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


from .atflex import AtfLexer
from .atfyacc import AtfParser
from mako.template import Template


class AtfFile(object):

    template = Template("${text.serialize()}")

    def __init__(self, content):
        self.content = content
        if content[-1] != '\n':
            content += "\n"
        lexer = AtfLexer().lexer
        parser = AtfParser().parser
        self.text = parser.parse(content, lexer=lexer)

    def __str__(self):
        return AtfFile.template.render_unicode(**vars(self))

    def serialize(self):
        return AtfFile.template.render_unicode(**vars(self))


def _debug_lex_and_yac_file(infile, debug=0, skipinvalid=False):
    import codecs
    text = codecs.open(infile, encoding='utf-8-sig').read()
    lexer = AtfLexer(debug=debug, skipinvalid=skipinvalid).lexer
    lexer.input(text)
    for tok in lexer:
        print(tok)
    print("Lexed file")
    lexer = AtfLexer().lexer
    parser = AtfParser().parser
    parser.parse(text, lexer=lexer)
    print("Parsed file")
