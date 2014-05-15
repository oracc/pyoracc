import ply.yacc as yacc
from atflex import AtfLexer
from ..artifact import Artifact

class AtfParser(object):
  tokens=AtfLexer.tokens
  def __init__(self):
    self.parser=yacc.yacc(module=self)


  def p_document(self,p):
    "document : codeline"
    p[0]=p[1]

  def p_codeline(self,p):
    "codeline : CODE ID NEWLINE"
    p[0]=Artifact()
    p[0].code=p[1]
    p[0].description=p[2]
