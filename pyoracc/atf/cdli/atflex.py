import re

from ply import lex as lex

from pyoracc.atf.common.atflex import AtfLexer


class AtfCDLILexer(AtfLexer):

    def __init__(self, skipinvalid=False, debug=0):
        super(AtfCDLILexer, self).__init__(skipinvalid, debug)
        self.lexer = lex.lex(module=self, reflags=re.MULTILINE, debug=debug)
