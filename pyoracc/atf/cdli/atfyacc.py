from pyoracc.atf.common.atfyacc import AtfParser
from pyoracc.model.state import State
from pyoracc.model.text import Text
from ply import yacc as yacc


class AtfCDLIParser(AtfParser):
    tokens = AtfParser.tokens
    precedence = AtfParser.precedence

    def __init__(self, debug, log):
        super(AtfCDLIParser, self).__init__(debug, log)
    #      self.parser = yacc.yacc(module=self, tabmodule='pyoracc.atf.parsetab', debug=debug, debuglog=log)

    def p_document(self, p):
        """document : text
                    | object
                    | composite"""
        p[0] = p[1]

    def p_linkreference_label(self, p):
        """link_reference : link_reference ID
                          | link_reference COMMA ID
                          | link_reference REFERENCE"""
        p[0] = p[1]
        p[0].label.append(list(p)[-1])

    def p_simple_dollar(self, p):
        """simple_dollar_statement : DOLLAR ID newline
                                   | DOLLAR state newline
                                   | DOLLAR REFERENCE ID newline"""
        # print(p[2])
        p[0] = State(p[2])

    #def p_version_protoocol(self, p):
     #   "version_protocol : VERSION ID newline"
     #   p[0] = p[2]

    #def p_text_version(self, p):
    #    "text : text version_protocol"
     #   p[0] = p[1]
      #  p[0].version = p[2]
