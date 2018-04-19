from pyoracc.atf.common.atfyacc import AtfParser


class AtfOraccParser(AtfParser):

    tokens = AtfParser.tokens
    precedence = AtfParser.precedence

    def __init__(self, debug, log):
        super(AtfOraccParser, self).__init__(debug, log)
