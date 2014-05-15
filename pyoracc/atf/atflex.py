import ply.lex as lex
import re

class AtfLexer(object):
  def _keyword_dict(self,tokens):
    return {token.lower(): token for token in tokens}

  def resolve_keyword(self,value,source,fallback=None):
    if not fallback:
      return self._keyword_dict(source)[value]
    return self._keyword_dict(source).get(value,fallback)


  divisions=[
    'TABLET',
    'ENVELOPE',
    'PRISM',
    'BULLA',
    'FRAGMENT',
    'OBJECT',
    'SEAL',
    'OBVERSE',
    'REVERSE',
    'LEFT',
    'RIGHT',
    'TOP',
    'BOTTOM',
    'FACE',
    'SURFACE',
    'EDGE',
    'COLUMN',
    'CATCHLINE',
    'COLOPHON',
    'DATE',
    'SIGNATURES',
    'SIGNATURE',
    'SUMMARY',
    'WITNESSES',
    'TRANSLATION',
    'NOTE',
    'M'
  ]

  protocols=['ATF','LEM','PROJECT','NOTE']

  protocol_keywords=['LANG','USE','MATH','UNICODE']

  dollar_keywords=[
    'AT','MOST','ABOUT',
    'SEVERAL','SOME','REST','OF','START','BEGINNING','MIDDLE','END',
    'COLUMNS','LINE','LINES','CASE','CASES','SURFACE',
    'BLANK','BROKEN','EFFACED','ILLEGIBLE','MISSING','TRACES',
    'RULING','SINGLE','DOUBLE','TRIPLE']

  flags={
    '!':'REMARK',
    '#':'BROKEN',
    '?':'QUERY',
    '*':'COLLATED'
  }

  base_tokens=[
    'CODE',
    'NEWLINE',
    'SPACE',
    'OTHER',
    'LINELABEL',
    'ID',
    'SINGLEID',
    'PROTOCOL',
    'DOLLAR',
    'LOOSE',
    'RANGE',
    'NUMBER',
    'COMMENT',
    'PRIME',
    'DIVISION',
    'NOTEREF',
    'TRANSLATIONTEXT'
  ]

  tokens=list(set(
    divisions+
    protocols+
    protocol_keywords+
    dollar_keywords+
    flags.values()+
    base_tokens))

  state_names=[
    'protocol',
    'code',
    'division',
    'text',
    'lemmatize',
    'dollar',
    'note',
    'translation'
  ]

  states=[(state,'exclusive') for state in state_names ]

  #----- METHODS DEFINING LINE-START TOKENS, WHICH SET STATE ----

  def t_LINELABEL(self,t):
    r'^[1-9][0-9]*[a-z]*\.'
    t.value=t.value[:-1]
    t.lexer.push_state('text')
    return t

  def t_CODE(self,t):
    '^&[A-Z][0-9]+\ \=\ '
    t.value=t.value[1:-3]
    t.lexer.push_state('code')
    return t
    # Match e.g. &X0001 at the start of a line

  def t_PROTOCOL(self,t):
    "^\#[a-z]*:\ "
    t.value=t.value[1:-2]
    t.type=self.resolve_keyword(t.value,AtfLexer.protocols)
    if t.value=="lem":
      t.lexer.push_state("lemmatize")
    elif t.value=="note":
      t.lexer.push_state("note")
    else:
      t.lexer.push_state('protocol')
    return t

  def t_INITIAL_translation_DIVISION(self,t):
    "^@[a-z]*"
    t.value=t.value[1:]
    t.type=self.resolve_keyword(t.value,AtfLexer.divisions)
    if t.type=="NOTE":
      t.lexer.push_state("note")
    elif t.type=="TRANSLATION":
      t.lexer.push_state("translation")
      t.lexer.push_state("division")
    else:
      t.lexer.push_state('division')
    return t

  def t_DOLLAR(self,t):
    r'^\$\ '
    t.lexer.push_state('dollar')
    return t

  #-- OTHER RULES ---

  def t_COMMENT(self,t):
    "^\#\ .*$"
    t.value=t.value[2:]
    return t



  def t_dollar_LOOSE(self,t):
    # Currently violates images
    "\((.*)\)"
    t.value=t.value[1:-1]
    return t

  def t_dollar_ID(self,t):
    '[a-zA-Z]+'
    t.type=self.resolve_keyword(t.value,
      AtfLexer.dollar_keywords+AtfLexer.divisions,'ID')
    return t

  t_dollar_RANGE="[1-9][0-9]*\-[1-9][0-9]"
  t_dollar_NUMBER="[1-9][0-9]*"

  def t_protocol_ID(self,t):
    '[a-zA-Z\-\/]+'
    t.type=self.resolve_keyword(t.value,AtfLexer.protocol_keywords,'ID')
    return t

  def t_code_ID(self,t):
    r'[^\n]+'
    return t

  def t_division_FLAG(self,t):
    r'[\?\!\#\*]'
    t.type=flags[t.value]
    return t

  t_division_ID="[a-z][a-z]+"
  t_division_SINGLEID="[a-z]"
  t_division_NUMBER="[1-9][0-9]*"
  t_division_PRIME="'"

  LANG="lang"
  t_protocol_USE="use"
  t_protocol_UNICODE="unicode"
  t_protocol_MATH="math"

  # Does NOT apply when parsing CODE LINE, or COMMENT as that is literal and
  # inside the token
  def t_INITIAL_division_protocol_dollar_SPACE(self,t):
    r'[ ]'
    # No return, don't add to token stream

  t_text_OTHER="."
  t_lemmatize_OTHER="."

  def t_note_NOTEREF(self,t):
    "\^(.*?)\^"
    t.value=t.value[1:-1]
    return t

  t_note_COMMENT=".+$"

  def t_protocol_code_text_division_note_dollar_lemmatize_NEWLINE(self,t):
    r'\n'
    t.lexer.pop_state()
    # No return, don't add to token stream

  t_INITIAL_translation_NEWLINE=r'\n'

  def t_translation_LINELABEL(self,t):
    r'^[1-9][0-9]*[a-z]*\.'
    t.value=t.value[:-1]
    return t

  t_translation_TRANSLATIONTEXT=".+$"

  # Error handling rule
  def t_error(self,t):
      print "Illegal character '%s'" % t.value[0]
      t.lexer.skip(1)

  def __init__(self,content):
    self.lexer=lex.lex(module=self,reflags=re.MULTILINE)
    self.lexer.input(content)
