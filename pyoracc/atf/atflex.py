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
    'PRIME',
    'DIVISION',
    'NOTEREF',
    'COMMENT',
    'ENDLEMMA'
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

  def t_COMMENT(self,t):
    "^\#\ "
    t.value=t.value[2:]
    t.lexer.push_state('note')
    return t

  # In all the single-line lexer states, a newline returns to the base state
  def t_protocol_code_text_division_note_dollar_lemmatize_NEWLINE(self,t):
    r'\n'
    t.lexer.pop_state()
    return t

  # In the multi-line base states, a newline doesn't change state
  t_INITIAL_translation_NEWLINE=r'\n'

  #-- RULES FOR THE code STATE ---
  # In this state, everything before the equals is tokenised
  # as a code token, and everything after, as a discussion

  def t_code_ID(self,t):
    r'[^\n]+'
    return t

  #-- RULES FOR THE protocol STATE ---
  # In this state, tokens are whitespace-separated,
  # and some are interpreted as keywords

  def t_protocol_SPACE(self,t):
    r'[ ]'
  # No return, don't add to token stream

  def t_protocol_ID(self,t):
    '[a-zA-Z\-\/]+'
    t.type=self.resolve_keyword(t.value,AtfLexer.protocol_keywords,'ID')
    return t

  #-- RULES FOR THE dollar STATE ---
  # In this state, tokens are whitespace-separated,
  # and some are interpreted as keywords
  # Numbers and ranges are tokenized separately
  # Bracketed content is assumed to be a single token

  def t_dollar_SPACE(self,t):
    r'[ ]'
  # No return, don't add to token stream

  def t_dollar_ID(self,t):
    '[a-zA-Z]+'
    t.type=self.resolve_keyword(t.value,
      AtfLexer.dollar_keywords+AtfLexer.divisions,'ID')
    return t

  t_dollar_RANGE="[1-9][0-9]*\-[1-9][0-9]"
  t_dollar_NUMBER="[1-9][0-9]*"

  def t_dollar_LOOSE(self,t):
    # Currently violates images
    "\((.*)\)"
    t.value=t.value[1:-1]
    return t

  #-- RULES FOR THE division STATE
  # In this state, tokens are whitespace-separated,
  # Certain characters are treated as flag markers
  # Single-character and number tokens are separately tokenised

  def t_division_SPACE(self,t):
    r'[ ]'
    # No return, don't add to token stream

  def t_division_FLAG(self,t):
    r'[\?\!\#\*]'
    t.type=flags[t.value]
    return t

  t_division_ID="[a-z][a-z]+"
  t_division_SINGLEID="[a-z]"
  t_division_NUMBER="[1-9][0-9]*"
  t_division_PRIME="'"

  #-- RULES FOR THE note STATE
  # In this state, all non-newline characters are interpreted as a
  # single token
  # Except for ^1^ which is tokenised as a NOTEREF

  def t_note_NOTEREF(self,t):
    "\^(.*?)\^\s*"
    t.value=t.lexer.lexmatch.groups()[2]
    return t

  t_note_ID=r'[^\^\n]+'

  # Does NOT apply when parsing CODE LINE, or COMMENT as that is literal and
  # inside the token

  #--- RULES FOR THE text STATE ----
  t_text_ID="[^\ \t \n\r]+"
  def t_text_SPACE(self,t):
    r'[\ \t]'
    # No token generated

  #--- RULES FOR THE lemmatize STATE
  t_lemmatize_ID="[^\;\n\r]+"
  t_lemmatize_ENDLEMMA=r'\;[\ \t]*'

  #--- RULES FOR THE TRANSLATION STATE ---
  # In this state, linelabels are tokenised separately,
  # But everything else is free text
  def t_translation_LINELABEL(self,t):
    r'^([1-9][0-9]*[a-z]*)\.[\ \t]*'
    t.value=t.lexer.lexmatch.groups()[2]
    return t

  t_translation_ID=".+$"

  # Error handling rule
  def t_ANY_error(self,t):
      print "Illegal character '%s'" % t.value[0]
      t.lexer.skip(1)

  def __init__(self):
    self.lexer=lex.lex(module=self,reflags=re.MULTILINE)
