import ply.yacc as yacc
from atflex import AtfLexer
from ..model.text import Text
from ..model.oraccobject import OraccObject
from ..model.oraccnamedobject import OraccNamedObject

class AtfParser(object):
  tokens=AtfLexer.tokens
  def __init__(self):
    self.parser=yacc.yacc(module=self)


  def p_document(self,p):
    "document : text"
    p[0]=p[1]

  def p_codeline(self,p):
    "code : CODE ID NEWLINE"
    p[0]=Text()
    p[0].code=p[1]
    p[0].description=p[2]

  def p_project(self,p):
    "project : PROJECT ID NEWLINE"
    p[0]=p[2]

  def p_text_project(self,p):
    "text : text project"
    p[0]=p[1]
    p[0].project=p[2]

  def p_code(self,p):
    "text : code"
    p[0]=p[1]

  def p_unicode(self,p):
    "unicode : ATF USE UNICODE NEWLINE"

  def p_math(self,p):
    "math : ATF USE MATH NEWLINE"

  def p_language_protoocol(self,p):
    "language_protocol : ATF LANG ID NEWLINE"
    p[0]=p[3]

  def p_text_math(self,p):
    "text : text math"

  def p_text_unicode(self,p):
    "text : text unicode"

  def p_text_language(self,p):
    "text : text language_protocol"
    p[0]=p[1]
    p[0].language=p[2]

  def p_structure_nolabel(self,p):
    '''structure : TABLET NEWLINE
              | ENVELOPE NEWLINE
              | PRISM NEWLINE
              | BULLA NEWLINE'''
    p[0]=OraccObject(p[1])

  def p_structure_label(self,p):
    '''structure : FRAGMENT ID NEWLINE | OBJECT ID NEWLINE'''
    p[0]=OraccNamedObject(p[1],p[2])

  def p_debug_object(self,p):
    """document : structure"""
    p[0]=p[1]
