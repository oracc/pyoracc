import sys
from atflex import AtfLexer
from atfyacc import AtfParser


class AtfFile(object):
    def __init__(self, content):
        self.content = content
        if content[-1] != '\n':
            content+="\n"
        lexer = AtfLexer().lexer
        parser = AtfParser().parser
        self.text = parser.parse(content, lexer=lexer)
