'''
Copyright 2015, 2016 University College London.

This file is part of PyORACC.

PyORACC is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyORACC is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyORACC. If not, see <http://www.gnu.org/licenses/>.
'''

from __future__ import print_function
import sys
import os
import codecs
from pyoracc.atf.common.atffile import AtfFile


class Corpus(object):
    def __init__(self, **kwargs):
        self.texts = []
        self.failures = 0
        self.successes = 0
        self.atftype = kwargs['atftype']
        self.source = kwargs['source']
        if 'source' in kwargs:
            for dirpath, _, files in os.walk(self.source):
                for file in files:
                    if file.endswith('.atf'):
                        try:
                            path = os.path.join(dirpath, file)
                            print("Parsing file", path, "... ", end="")
                            content = codecs.open(path,
                                                  encoding='utf-8-sig').read()
                            self.texts.append(AtfFile(content, self.atftype))

                            self.successes += 1
                            print("OK")
                        except (SyntaxError, IndexError, AttributeError,
                                UnicodeDecodeError) as e:
                            self.texts.append(None)
                            self.failures += 1
                            print("Failed with message: '{}'".format(e))


if __name__ == '__main__':
    try:
        corpus = Corpus(source=sys.argv[1], atftype=sys.argv[2])
        print()
        print("Failed with ", corpus.failures, " out of ",
              corpus.failures + corpus.successes, "(",
              corpus.failures * 100.0 / (corpus.failures + corpus.successes),
              "%)")
    except IndexError:
        print("Input both atffile type and file source like 'python  -m "
              "pyoracc.model.corpus cdli ./pyoracc/test/data'")
