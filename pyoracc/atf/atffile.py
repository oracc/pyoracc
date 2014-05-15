import sys
import antlr3
from atflex import AtfLexer
from atfyacc import AtfParser

class AtfFile(object):
  def __init__(self,content):
    self.content=content
    lexer=AtfLexer().lexer
    parser=AtfParser().parser
    self.artifact=parser.parse(content,lexer=lexer)
