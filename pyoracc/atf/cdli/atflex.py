import re
from ply import lex

from pyoracc.atf.common.atflex import AtfLexer


class AtfCDLILexer(AtfLexer):

    def __init__(self, skipinvalid, debug, log):
        super(AtfCDLILexer, self).__init__(skipinvalid, debug, log)
        #self.lexer = lex.lex(module=self, reflags=re.MULTILINE, debug=debug, debuglog=log)