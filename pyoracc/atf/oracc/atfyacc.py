from pyoracc.atf.common.atfyacc import AtfParser
from ply import yacc as yacc


class AtfOraccParser(AtfParser):

    tokens = AtfParser.tokens
    precedence = AtfParser.precedence

    def __init__(self, debug, log):
        super(AtfOraccParser, self).__init__(debug, log)
