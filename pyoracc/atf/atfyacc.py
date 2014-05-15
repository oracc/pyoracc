import ply.yacc as yacc
from atflex import AtfLexer
from ..artifact import Artifact

class AtfParser(object):
  tokens=AtfLexer.tokens
  def __init__(self,start=None):
    self.parser=yacc.yacc(module=self,start=start)


  def p_document(self,p):
    "document : artifact"
    p[0]=p[1]

  def p_codeline(self,p):
    "code : CODE ID NEWLINE"
    p[0]=Artifact()
    p[0].code=p[1]
    p[0].description=p[2]

  def p_project(self,p):
    "project : PROJECT ID NEWLINE"
    p[0]=p[2]

  def p_artifact(self,p):
    "artifact : artifact project"
    p[0]=p[1]
    p[0].project=p[2]

  def p_code(self,p):
    "artifact : code"
    p[0]=p[1]
