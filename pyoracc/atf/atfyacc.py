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
    "project_statement : PROJECT ID newline_sequence"
    p[0]=p[2]

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
    "unicode : ATF USE UNICODE newline_sequence"

  def p_math(self,p):
    "math : ATF USE MATH newline_sequence"

  def p_language_protoocol(self,p):
    "language_protocol : ATF LANG ID newline_sequence"
    p[0]=p[3]

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
    """text : text object"""
    p[0]=p[1]
    p[0].children.append(p[2])


  def p_object_statement(self,p):
    """object_statement : object_specifier newline_sequence"""
    p[0]=p[1]

  def p_object_flag_broken(self,p):
    "object_specifier : object_specifier HASH"
    p[0]=p[1]
    p[0].broken=True

  def p_object_flag_remarkable(self,p):
    "object_specifier : object_specifier EXCLAIM"
    p[0]=p[1]
    p[0].remarkable=True

  def p_object_flag_prime(self,p):
    "object_specifier : object_specifier PRIME"
    p[0]=p[1]
    p[0].prime=True

  def p_object_flag_query(self,p):
    "object_specifier : object_specifier QUERY"
    p[0]=p[1]
    p[0].query=True

  def p_object_flag_collated(self,p):
    "object_specifier : object_specifier STAR"
    p[0]=p[1]
    p[0].collated=True

  # These MUST be kept as a separate parse rule,
  # as the same keywords also occur
  # in strict dollar lines
  def p_object_nolabel(self,p):
    '''object_specifier : TABLET
                        | ENVELOPE
                        | PRISM
                        | BULLA'''
    p[0]=OraccObject(p[1])


  def p_object_label(self,p):
    '''object_specifier : FRAGMENT ID
                        | OBJECT ID'''
    p[0]=OraccNamedObject(p[1],p[2])


  def p_object(self,p):
    "object : object_statement"
    p[0]=p[1]

  def p_object_surface(self,p):
    """object : object surface
              | object translation %prec TRANSLATIONEND """
    p[0]=p[1]
    p[0].children.append(p[2])

  def p_surface_statement(self,p):
    "surface_statement : surface_specifier newline_sequence"
    p[0]=p[1]

  def p_surface_flag_broken(self,p):
    "surface_specifier : surface_specifier HASH"
    p[0]=p[1]
    p[0].broken=True

  def p_surface_flag_remarkable(self,p):
    "surface_specifier : surface_specifier EXCLAIM"
    p[0]=p[1]
    p[0].remarkable=True

  def p_surface_flag_prime(self,p):
    "surface_specifier : surface_specifier PRIME"
    p[0]=p[1]
    p[0].prime=True

  def p_surface_flag_query(self,p):
    "surface_specifier : surface_specifier QUERY"
    p[0]=p[1]
    p[0].query=True

  def p_surface_flag_collated(self,p):
    "surface_specifier : surface_specifier STAR"
    p[0]=p[1]
    p[0].collated=True

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
    p[0]=OraccObject(p[1])

  def p_surface_label(self,p):
    '''surface_specifier : FACE SINGLEID
                         | SURFACE ID
                         | EDGE ID
                         | COLUMN NUMBER
                         | SEAL NUMBER
                         | H NUMBER'''
    p[0]=OraccNamedObject(p[1],p[2])

  def p_surface(self,p):
    "surface : surface_statement"
    p[0]=p[1]

  def p_surface_line(self,p):
    """surface : surface line
               | surface ruling
               | surface loose_dollar_statement
               | surface strict_dollar_statement """
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
    "line : line lemma_statement  "
    p[0]=p[1]
    p[0].lemmas=p[2]

  def p_line_note(self,p):
    "line : line note_statement "
    p[0]=p[1]
    p[0].notes.append(p[2])

  def p_lemma_list(self,p):
    "lemma_list : LEM ID"
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
    """note_statement : note_sequence newline_sequence"""
    p[0]=p[1]

  def p_note_sequence(self,p):
    """note_sequence : NOTE """
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
                                  | REFERENCE state
                                  | REFERENCE ID state
                                  | REFERENCE NUMBER state"""
    text=list(p)
    p[0]=State(text[-1]," ".join(text[1:-1]))

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
    p[0]=p[1]

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
    """qualification : AT LEAST
                     | AT MOST
                     | ABOUT"""
    p[0]=" ".join(p[1:])

  def p_translation_statement(self,p):
    "translation_statement : TRANSLATION PARALLEL ID PROJECT newline_sequence"
    p[0]=Translation()

  def p_translation(self,p):
    "translation : translation_statement"
    p[0]=p[1]

  def p_translation_surface(self,p):
    "translation : translation surface "
    p[0]=p[1]
    p[0].children.append(p[2])

  # There is a potential shift-reduce conflict in the following sample:

  """
  @tablet
  @obverse
  @translation
  @obverse
  """

  # where (object(surface,translation(surface))) could be read as
  # object(surface,translation(),surface)
  # These need to be resolved by making surface establishment and composition
  # take precedence over the completion of a translation

  precedence = (
    ('nonassoc','TRANSLATIONEND'),
    ('nonassoc','OBVERSE','REVERSE','LEFT','RIGHT','TOP','BOTTOM',
    'CATCHLINE','COLOPHON','DATE','SIGNATURES','SIGNATURE','SUMMARY',
    'WITNESSES','FACE','SINGLEID','SURFACE','EDGE','COLUMN','SEAL')
  )
