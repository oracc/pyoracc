from mako.template import Template


class Score(object):
    def __init__(self, ttype, mode, word=False):
        self.ttype = ttype
        self.mode = mode
        self.word = word
