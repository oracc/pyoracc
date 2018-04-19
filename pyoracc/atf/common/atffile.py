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

import codecs
import sys
import logging

from pyoracc.atf.cdli.atflex import AtfCDLILexer
from pyoracc.atf.cdli.atfyacc import AtfCDLIParser
from pyoracc.atf.common.atflex import AtfLexer
from pyoracc.atf.common.atfyacc import AtfParser
from pyoracc.atf.oracc.atflex import AtfOraccLexer
from pyoracc.atf.oracc.atfyacc import AtfOraccParser
from mako.template import Template

logging.basicConfig(
    level=logging.DEBUG,
    filename="parselog.txt",
    filemode="w",
    format="%(filename)10s:%(lineno)4d:%(message)s"
)

log = logging.getLogger()

consoleHandler = logging.StreamHandler()
log.addHandler(consoleHandler)


class AtfFile(object):
    template = Template("${text.serialize()}")

    def __init__(self, content, atftype='oracc', debug=False):
        skipinvalid = False
        if content[-1] != '\n':
            content += "\n"
        if atftype == 'cdli':
            lexer = AtfCDLILexer(debug=debug, skipinvalid=skipinvalid,
                                 log=log).lexer
            parser = AtfCDLIParser(debug=debug, log=log).parser
        elif atftype == 'oracc':
            lexer = AtfOraccLexer(debug=debug, skipinvalid=skipinvalid,
                                  log=log).lexer
            parser = AtfOraccParser(debug=debug, log=log).parser
        else:
            lexer = AtfLexer(debug=debug, skipinvalid=skipinvalid,
                             log=log).lexer
            parser = AtfParser(debug=debug, log=log).parser
        if debug:
            self.text = parser.parse(content, lexer=lexer, debug=log)
        else:
            self.text = parser.parse(content, lexer=lexer)

    def __str__(self):
        return AtfFile.template.render_unicode(**vars(self))

    def serialize(self):
        return AtfFile.template.render_unicode(**vars(self))


def check_atf(infile, atftype, verbose=False):
    content = codecs.open(infile,
                          encoding='utf-8-sig').read()
    AtfFile(content, atftype, verbose)


if __name__ == "__main__":
    check_atf(infile=sys.argv[1], atftype=sys.argv[2],
              verbose=(sys.argv[3] == "True"))
