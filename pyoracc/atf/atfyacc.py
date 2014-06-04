import ply.yacc as yacc
from atflex import AtfLexer
from ..model.text import Text
from ..model.oraccobject import OraccObject
from ..model.oraccnamedobject import OraccNamedObject
from ..model.line import Line
from ..model.ruling import Ruling
from ..model.note import Note
from ..model.state import State
from ..model.translation import Translation

class AtfParser(object):
  tokens=AtfLexer.tokens
  def __init__(self):
    self.parser=yacc.yacc(module=self)


  def p_document(self,p):
    """document : text
                | object"""
    p[0]=p[1]

  def p_codeline(self,p):
    "text_statement : AMPERSAND ID EQUALS ID newline_sequence"
    p[0]=Text()
    p[0].code=p[2]
    p[0].description=p[4]

  def p_project_statement(self,p):
    "project_statement : HASH PROJECT ID newline_sequence"
    p[0]=p[3]

  def p_project(self,p):
    "project : project_statement"
    p[0]=p[1]

  def p_text_project(self,p):
    "text : text project"
    p[0]=p[1]
    p[0].project=p[2]

  def p_code(self,p):
    "text : text_statement"
    p[0]=p[1]

  def p_unicode(self,p):
    "unicode : HASH ATF USE UNICODE newline_sequence"

  def p_math(self,p):
    "math : HASH ATF USE MATH newline_sequence"

  def p_language_protoocol(self,p):
    "language_protocol : HASH ATF LANG ID newline_sequence"
    p[0]=p[4]

  def p_text_math(self,p):
    "text : text math"
    p[0]=p[1]

  def p_text_unicode(self,p):
    "text : text unicode"
    p[0]=p[1]

  def p_text_language(self,p):
    "text : text language_protocol"
    p[0]=p[1]
    p[0].language=p[2]

  def p_text_object(self,p):
    """text : text object %prec COMPOSITION"""
    p[0]=p[1]
    p[0].children.append(p[2])


  def p_object_statement(self,p):
    "object_statement : AT object_specifier newline_sequence"
    if len(p[2])==2:
      p[0]=OraccNamedObject(*p[2])
    else:
      p[0]=OraccObject(*p[2])

  def p_object_nolabel(self,p):
    '''object_specifier : TABLET
                        | ENVELOPE
                        | PRISM
                        | BULLA'''
    p[0]=(p[1],)


  def p_object_label(self,p):
    '''object_specifier : FRAGMENT ID
                        | OBJECT ID'''
    p[0]=(p[1],p[2])

  def p_object(self,p):
    "object : object_statement"
    p[0]=p[1]

  def p_object_surface(self,p):
    """object : object surface %prec COMPOSITION
              | object translation %prec COMPOSITION """
    p[0]=p[1]
    p[0].children.append(p[2])

  def p_surface_decl(self,p):
    "surface_statement : AT surface_specifier newline_sequence"
    if len(p[2])==2:
      p[0]=OraccNamedObject(*p[2])
    else:
      p[0]=OraccObject(*p[2])

  def p_surface_nolabel(self,p):
    '''surface_specifier  : OBVERSE
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
    p[0]=(p[1],)

  def p_surface_label(self,p):
    '''surface_specifier : FACE SINGLEID
                         | SURFACE ID
                         | EDGE ID
                         | COLUMN NUMBER
                         | SEAL NUMBER
                         | H NUMBER'''
    p[0]=(p[1],p[2])

  def p_surface(self,p):
    "surface : surface_statement"
    p[0]=p[1]

  def p_surface_line(self,p):
    """surface : surface line %prec COMPOSITION
               | surface ruling %prec COMPOSITION
               | surface loose_dollar_statement %prec COMPOSITION
               | surface strict_dollar_statement %prec COMPOSITION """
    p[0]=p[1]
    p[0].children.append(p[2])

  # WE DO NOT YET HANDLE @M=DIVSION lines.

  def p_linelabel(self,p):
    "line_sequence : LINELABEL ID"
    p[0]=Line(p[1])
    p[0].words.append(p[2])



  def p_line_id(self,p):
    "line_sequence : line_sequence ID"
    p[0]=p[1]
    p[0].words.append(p[2])

  def p_line_reference(self,p):
    "line_sequence : line_sequence reference"
    p[0]=p[1]
    p[0].references.append(p[2])

  def p_line_statement(self,p):
    "line_statement : line_sequence newline_sequence"
    p[0]=p[1]

  def p_line(self,p):
    "line : line_statement"
    p[0]=p[1]

  def p_line_lemmas(self,p):
    "line : line lemma_statement %prec COMPOSITION "
    p[0]=p[1]
    p[0].lemmas=p[2]

  def p_line_note(self,p):
    "line : line note_statement %prec COMPOSITION"
    p[0]=p[1]
    p[0].notes.append(p[2])

  def p_lemma_list(self,p):
    "lemma_list : HASH LEM ID"
    p[0]=[p[2]]

  def p_lemma_id(self,p):
    "lemma_list : lemma_list SEMICOLON ID"
    p[0]=p[1]
    p[0].append(p[3])

  def p_lemma_statement(self,p):
    "lemma_statement : lemma_list newline_sequence"
    p[0]=p[1]

  def p_ruling(self,p):
    """ruling : DOLLAR SINGLE RULING newline_sequence
              | DOLLAR DOUBLE RULING newline_sequence
              | DOLLAR TRIPLE RULING newline_sequence
    """
    counts={
      'single':1,
      'double':2,
      'triple':3,
    }
    p[0]=Ruling(counts[p[2]])

  def p_note(self,p):
    """note_statement : HASH note_sequence newline_sequence
                      | AT note_sequence newline_sequence"""
    p[0]=p[2]

  def p_note_sequence(self,p):
    """note_sequence : NOTE"""
    p[0]=Note()

  def p_note_sequence_content(self,p):
    """note_sequence : note_sequence ID"""
    p[0]=p[1]
    p[0].content+=p[2]

  def p_note_sequence_link(self,p):
    """note_sequence : note_sequence reference"""
    p[0]=p[1]
    p[0].references.append(p[2])

  def p_reference(self,p):
    "reference : HAT ID HAT"
    p[0]=p[2]

  def p_newline_sequence(self,p):
    """newline_sequence : NEWLINE
                        | newline_sequence NEWLINE"""

  def p_loose_dollar(self,p):
    "loose_dollar_statement : DOLLAR PARENTHETICALID newline_sequence"
    p[0]=State(loose=p[2])

  def p_strict_dollar_statement(self,p):
    "strict_dollar_statement : DOLLAR state_description newline_sequence"
    p[0]=p[2]

  def p_state_description(self,p):
    """state_description : plural_state_description
                         | singular_state_description"""
    p[0]=p[1]

  def p_plural_state_description(self,p):
    """plural_state_description : plural_quantifier plural_scope state
                                | NUMBER plural_scope state
                                | RANGE plural_scope state"""
    p[0]=State(p[3],p[2],p[1])

  def p_qualified_state_description(self,p):
    "plural_state_description : qualification plural_state_description"
    p[0]=p[2]
    p[0].qualification=p[1]

  def p_singular_state_description(self,p):
    """singular_state_description : singular_scope state
                                  | object_specifier state
                                  | surface_specifier state"""
    p[0]=State(p[2]," ".join(p[1]))

  def p_partial_state_description(self,p):
    "singular_state_description : partial_quantifier singular_state_description"
    p[0]=p[2]
    p[0].extent=p[1]

  def p_state(self,p):
    """state : BLANK
             | BROKEN
             | EFFACED
             | ILLEGIBLE
             | MISSING
             | TRACES"""
    p[0]=p[1]

  def p_plural_quantifier(self,p):
    """plural_quantifier : SEVERAL
                         | SOME"""

  def p_singular_scope(self,p):
    """singular_scope : LINE
                      | CASE"""
    p[0]=[p[1]]

  def p_plural_scope(self,p):
    """plural_scope : COLUMNS
                    | LINES
                    | CASES"""
    p[0]=p[1]

  def p_partial_quantifier(self,p):
    """partial_quantifier : REST OF
                          | START OF
                          | BEGINNING OF
                          | MIDDLE OF
                          | END OF"""
    p[0]=" ".join(p[1:])

  def p_qualification(self,p):
    """qualification : ATWORD LEAST
                     | ATWORD MOST
                     | ABOUT"""
    p[0]=" ".join(p[1:])

  def p_translation_statement(self,p):
    "translation_statement : AT translation_declaration newline_sequence"
    p[0]=p[2]

  def p_translation_declaration(self,p):
    "translation_declaration : TRANSLATION"
    p[0]=Translation()

  # This is a placeholder, translation grammar is more complex
  def p_translation_info(self,p):
    "translation_declaration : translation_declaration ID"
    p[0]=p[1] # We ignore the 'parallel en project'

  def p_translation(self,p):
    "translation : translation_statement"
    p[0]=p[1]

  def p_translation_surface(self,p):
    "translation : translation surface"
    p[0]=p[1]
    p[0].children.append(p[2])

  # There is a potential shift-reduce error in the following sample:

  """
  &X=Something
  @tablet
  @obverse
  """

  # where text(object(surface)) could be read as text(object) . surface
  # These need to be resolved by making the potential declaration of a new
  # child entity take precedence over composition of an object into its parent

  precedence = (
    ('nonassoc','COMPOSITION'),
    ('nonassoc','HASH'),
    ('nonassoc','AT'),
  )
