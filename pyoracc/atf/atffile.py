import sys
import antlr3
from atflex import AtfLexer
#from atfyacc import parser

class AtfFile(object):
  def __init__(self,content):
    self.content=content
    for token in AtfLexer(content).lexer:
      print token
    self.artifact=parse.artifact
