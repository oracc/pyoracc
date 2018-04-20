from pyoracc.atf.common.atflex import AtfLexer


class AtfOraccLexer(AtfLexer):

    def __init__(self, skipinvalid, debug, log):
        super(AtfOraccLexer, self).__init__(skipinvalid, debug, log)
