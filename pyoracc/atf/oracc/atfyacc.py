from pyoracc.atf.common.atfyacc import AtfParser
from ply import yacc as yacc


class AtfOraccParser(AtfParser):

    tokens = AtfParser.tokens
    precedence = AtfParser.precedence

    def __init__(self, tabmodule='pyoracc.atf.parsetab', debug=0):
        super(AtfOraccParser, self).__init__(tabmodule)
        self.parser = yacc.yacc(module=self, tabmodule=tabmodule, debug=debug)