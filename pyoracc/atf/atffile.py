import sys
import antlr3
from atflex import AtfLexer
#from atfyacc import parser

class AtfFile(object):
  def __init__(self,content):
    self.content=content
    lexer=AtfLexer().lexer
    lexer.input(content)
    for token in lexer:
      print token
    self.artifact=parse.artifact
