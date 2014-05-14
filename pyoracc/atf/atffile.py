import sys
import antlr3
from antlr_generated.atfLexer import *
from antlr_generated.atfParser import *

class AtfFile(object):
  def __init__(self,content):
    self.content=content
    lexx = atfLexer(antlr3.StringStream(content))
    parse = atfParser(antlr3.CommonTokenStream(lexx))
    parse.startRule()
    self.artifact=parse.artifact
