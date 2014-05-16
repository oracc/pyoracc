import ply.yacc as yacc
from atflex import AtfLexer
from ..model.text import Text
from ..model.oraccobject import OraccObject
from ..model.oraccnamedobject import OraccNamedObject
from ..model.line import Line
from ..model.ruling import Ruling
from ..model.note import Note

class AtfParser(object):
  tokens=AtfLexer.tokens
  def __init__(self):
    self.parser=yacc.yacc(module=self)


  def p_document(self,p):
    "document : text"
    p[0]=p[1]

  def p_codeline(self,p):
    "code : AMPERSAND ID EQUALS ID"
    p[0]=Text()
    p[0].code=p[2]
    p[0].description=p[4]

  def p_project(self,p):
    "project : PROJECT ID"
    p[0]=p[2]

  def p_text_project(self,p):
    "text : text project"
    p[0]=p[1]
    p[0].project=p[2]

  def p_code(self,p):
    "text : code"
    p[0]=p[1]

  def p_unicode(self,p):
    "unicode : ATF USE UNICODE"

  def p_math(self,p):
    "math : ATF USE MATH"

  def p_language_protoocol(self,p):
    "language_protocol : ATF LANG ID"
    p[0]=p[3]

  def p_text_math(self,p):
    "text : text math"

  def p_text_unicode(self,p):
    "text : text unicode"

  def p_text_language(self,p):
    "text : text language_protocol"
    p[0]=p[1]
    p[0].language=p[2]

  def p_object_nolabel(self,p):
    '''object : TABLET
              | ENVELOPE
              | PRISM
              | BULLA'''
    p[0]=OraccObject(p[1])

  def p_surface_nolabel(self,p):
    '''surface : OBVERSE
              | REVERSE
              | LEFT
              | RIGHT
              | TOP
              | BOTTOM
              | CATCHLINE
              | COLOPHON
              | DATE
              | SIGNATURES
              | SIGNATURE
              | SUMMARY
              | WITNESSES'''
    p[0]=OraccObject(p[1])


  def p_object_label(self,p):
    '''object : FRAGMENT ID
                 | OBJECT ID
                 | FACE SINGLEID
                 | SURFACE ID
                 | EDGE ID
                 | COLUMN NUMBER
                 | SEAL NUMBER
                 | H NUMBER'''
    p[0]=OraccNamedObject(p[1],p[2])

  def p_surface_label(self,p):
    '''surface : FACE SINGLEID
                 | SURFACE ID
                 | EDGE ID
                 | COLUMN NUMBER
                 | SEAL NUMBER
                 | H NUMBER'''
    p[0]=OraccNamedObject(p[1],p[2])

  # WE DO NOT YET HANDLE @M=DIVSION lines.

  def p_debug_object(self,p):
    """document : object"""
    p[0]=p[1]

  def p_text_object(self,p):
    """text : text object"""
    p[0]=p[1]
    p[0].children.append(p[2])

  def p_object_surface(self,p):
    "object : object surface"
    p[0]=p[1]
    p[0].children.append(p[2])

  def p_linelabel(self,p):
    "line : LINELABEL ID"
    p[0]=Line(p[1])
    p[0].words.append(p[2])

  def p_line_id(self,p):
    "line : line ID"
    p[0]=p[1]
    p[0].words.append(p[2])

  def p_lemma_list(self,p):
    "lemma_list : LEM ID"
    p[0]=[p[2]]

  def p_lemma_id(self,p):
    "lemma_list : lemma_list SEMICOLON ID"
    p[0]=p[1]
    p[0].append(p[3])

  def p_line_lemmas(self,p):
    "line : line lemma_list"
    p[0]=p[1]
    p[1].lemmas=p[2]

  def p_surface_line(self,p):
    "surface : surface line"
    p[0]=p[1]
    p[0].children.append(p[2])

  def p_ruling(self,p):
    """ruling : DOLLAR SINGLE RULING
              | DOLLAR DOUBLE RULING
              | DOLLAR TRIPLE RULING
    """
    counts={
      'single':1,
      'double':2,
      'triple':3,
    }
    p[0]=Ruling(counts[p[2]])

  def p_surface_ruling(self,p):
    "surface : surface ruling"
    p[0]=p[1]
    p[0].children.append(p[2])

  def p_note(self,p):
    "note : NOTE ID"
    p[0]=p[2]

  def p_line_note(self,p):
    "line : line note"
    p[0]=p[1]
    p[0].notes.append(p[2])
