import re

from ply import lex as lex

from pyoracc.atf.common.atflex import AtfLexer


class AtfOraccLexer(AtfLexer):

    def __init__(self, skipinvalid=False, debug=0):
        super(AtfOraccLexer, self).__init__(skipinvalid, debug)
        self.lexer = lex.lex(module=self, reflags=re.MULTILINE, debug=debug)
