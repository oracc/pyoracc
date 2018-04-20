from pyoracc.atf.common.atflex import AtfLexer


class AtfCDLILexer(AtfLexer):

    def __init__(self, skipinvalid, debug, log):
        super(AtfCDLILexer, self).__init__(skipinvalid, debug, log)
