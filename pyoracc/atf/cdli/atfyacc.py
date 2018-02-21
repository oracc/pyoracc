from pyoracc.atf.common.atfyacc import AtfParser
from pyoracc.model.text import Text
from ply import yacc as yacc


class AtfCDLIParser(AtfParser):

    tokens = AtfParser.tokens
    precedence = AtfParser.precedence

    def __init__(self, tabmodule='pyoracc.atf.parsetab'):
        super(AtfCDLIParser, self).__init__(tabmodule)
        self.parser = yacc.yacc(module=self, tabmodule=tabmodule)

    def p_document(self, p):
        """document : text
                    | object
                    | composite"""
        p[0] = p[1]

    def p_codeline(self, p):
        "text_statement : AMPERSAND ID EQUALS ID newline"
        p[0] = Text()
        p[0].code = p[2]
        p[0].description = p[4]