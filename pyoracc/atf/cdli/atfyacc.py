from pyoracc.model.milestone import Milestone

from pyoracc.model.oraccobject import OraccObject

from pyoracc.atf.common.atfyacc import AtfParser
from pyoracc.model.state import State
from pyoracc.model.text import Text


class AtfCDLIParser(AtfParser):
    tokens = AtfParser.tokens
    precedence = AtfParser.precedence

    def __init__(self, debug, log):
        super(AtfCDLIParser, self).__init__(debug, log)

    def p_document(self, p):
        """document : text
                    | object
                    | composite"""
        p[0] = p[1]

    def p_linkreference_label(self, p):
        """link_reference : link_reference ID
                          | link_reference COMMA ID
                          | link_reference REFERENCE
                          | link_reference ID QUERY"""
        p[0] = p[1]
        p[0].label.append(list(p)[-1])

    def p_simple_dollar(self, p):
        """simple_dollar_statement : DOLLAR ID newline
                                   | DOLLAR state newline
                                   | DOLLAR REFERENCE ID newline"""
        # print(p[2])
        p[0] = State(p[2])

    # to remove later
    def p_version_protoocol(self, p):
        """version_protocol : VERSION ID newline"""
        p[0] = p[2]

    # to remove later
    def p_text_version(self, p):
        """text : text version_protocol"""
        p[0] = p[1]
        p[0].version = p[2]

    def p_codeline(self, p):
        """text_statement : AMPERSAND ID EQUALS ID newline
                            | AMPERSAND ID EQUALS ID QUERY newline """
        p[0] = Text()
        p[0].code = p[2]
        p[0].description = p[4]

    def p_surface_nolabel(self, p):
        '''surface_specifier  : OBVERSE
                              | REVERSE
                              | LEFT
                              | RIGHT
                              | TOP
                              | BOTTOM
                              | EDGE'''
        p[0] = OraccObject(p[1])

    def p_milestone_brief(self, p):
        """milestone_name : CATCHLINE
                          | COLOPHON
                          | DATE
                          | SIGNATURES
                          | SIGNATURE
                          | SUMMARY
                          | WITNESSES"""
        p[0] = Milestone(p[1])
