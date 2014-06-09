from __future__ import print_function
import sys
import os
from ..atf.atffile import AtfFile


class Corpus(object):
    def __init__(self, pattern="*.atf", **kwargs):
        self.texts = []
        self.failures = 0
        self.successes = 0
        if 'source' in kwargs:
            for dirpath,_,files in os.walk(kwargs['source']):
                for file in files:
                    try:
                        path=os.path.join(dirpath,file)
                        print("Parsing file", path)
                        self.texts.append(AtfFile(open(path).read()))
                        self.successes += 1
                    except SyntaxError:
                        self.texts.append(None)
                        self.failures += 1


if __name__ == '__main__':
    corpus=Corpus(source = sys.argv[1])
    print("Succeeded with ", corpus.successes, " out of ",
          corpus.failures + corpus.successes)
