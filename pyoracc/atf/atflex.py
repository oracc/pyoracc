import ply.lex as lex
import re

class AtfLexer(object):

  def _keyword_dict(self,tokens):
    return {token.lower(): token for token in tokens}

  def resolve_keyword(self,value,source,fallback=None):
    source = self._keyword_dict(source)
    if not fallback:
      return source[value]
    return source.get(value,fallback)


  structures=[
    'TABLET',
    'ENVELOPE',
    'PRISM',
    'BULLA',
    'OBVERSE',
    'REVERSE',
    'LEFT',
    'RIGHT',
    'TOP',
    'BOTTOM',
    'CATCHLINE',
    'COLOPHON',
    'DATE',
    'SIGNATURES',
    'SIGNATURE',
    'SUMMARY',
    'FACE',
    'EDGE',
    'COLUMN',
    'SEAL',
    'WITNESSES',
    'TRANSLATION',
    'NOTE',
    'M',
    'H'
  ]

  long_argument_structures=[
    'OBJECT',
    'SURFACE',
    'FRAGMENT'
  ]

  protocols=['ATF','LEM','PROJECT','NOTE']

  protocol_keywords=['LANG','USE','MATH','UNICODE']

  translation_keywords=['PARALLEL','PROJECT']

  dollar_keywords=[
    'MOST','LEAST','ABOUT',
    'SEVERAL','SOME','REST','OF','START','BEGINNING','MIDDLE','END',
    'COLUMNS','LINE','LINES','CASE','CASES','SURFACE',
    'BLANK','BROKEN','EFFACED','ILLEGIBLE','MISSING','TRACES',
    'RULING','SINGLE','DOUBLE','TRIPLE','AT']

  base_tokens=[
    'AMPERSAND',
    'LINELABEL',
    'ID',
    'SINGLEID',
    'DOLLAR',
    'PARENTHETICALID',
    'NUMBER',
    'HAT',
    'SEMICOLON',
    'EQUALS',
    'LSQUARE',
    'RSQUARE',
    'EXCLAIM',
    'QUERY',
    'STAR',
    'PRIME',
    'RANGE',
    'LETTER',
    'HASH',
    'NEWLINE',
    'REFERENCE'
  ]

  keyword_tokens=list(set(
    structures+
    long_argument_structures+
    protocols+
    protocol_keywords+
    dollar_keywords+
    translation_keywords
  ))

  tokens=list(set(
    keyword_tokens+
    base_tokens))

  state_names=[
    'absorb',
    'text',
    'lemmatize',
    'translation'
  ]

  states=[(state,'exclusive') for state in state_names ]

  t_INITIAL_translation_AMPERSAND="\&"
  t_INITIAL_translation_HASH="\#"
  t_INITIAL_translation_EXCLAIM="\!"
  t_INITIAL_translation_QUERY="\?"
  t_INITIAL_translation_STAR="\*"
  t_INITIAL_translation_PRIME=r'\''
  t_INITIAL_translation_DOLLAR="\$"

  t_PARENTHETICALID="\([^\)\n\r]*\)"

  def t_INITIAL_translation_WHITESPACE(self,t):
    r'[\t ]+'
    # NO TOKEN

  def t_INITIAL_translation_EQUALS(self,t):
    "\="
    t.lexer.push_state('absorb')
    return t

  def t_INITIAL_translation_COMMENT(self,t):
    "^\#[\ \t][^\n\r]*"
    # No token

  # In the multi-line base states, a newline doesn't change state
  def t_INITIAL_translation_NEWLINE(self,t):
    r'\n'
    t.lexer.lineno += 1
    return t

  def t_INITIAL_translation_ATID(self,t):
    '\@[a-zA-Z][a-zA-Z0-9\[\]]+'
    t.value=t.value[1:]
    t.type=self.resolve_keyword(t.value,
      AtfLexer.structures+AtfLexer.long_argument_structures)
    if t.type == "TRANSLATION":
      t.lexer.push_state('translation')
    if t.type in AtfLexer.long_argument_structures+["NOTE"]:
      t.lexer.push_state('absorb')
    return t

  def t_INITIAL_translation_HASHID(self,t):
    '\#[a-zA-Z][a-zA-Z0-9\[\]]+\:'
    # Note that \:? absorbs a trailing colon in protocol keywords
    t.value=t.value[1:-1]
    t.type=self.resolve_keyword(t.value,
      AtfLexer.protocols)

    if t.type == "LEM":
      t.lexer.push_state('lemmatize')
    if t.type in ['PROJECT','NOTE']:
      t.lexer.push_state('absorb')
    return t

  def t_INITIAL_translation_ID(self,t):
    '[a-zA-Z][a-zA-Z0-9\[\]]+'

    t.type=self.resolve_keyword(t.value,
      AtfLexer.protocol_keywords+
      AtfLexer.dollar_keywords+
      AtfLexer.structures+
      AtfLexer.translation_keywords+
      AtfLexer.long_argument_structures,'ID')

    if t.type in ['LANG']:
      t.lexer.push_state('absorb')

    if t.type in set(AtfLexer.structures+AtfLexer.long_argument_structures)-set(["NOTE"]):
      # Since @structure tokens are so important to the grammar,
      # the keywords refering to structural elements in strict dollar
      # lines must be DIFFERENT TOKENS IN THE LEXER
      t.type = "REFERENCE"
    return t

  def t_LINELABEL(self,t):
    r'^[1-9][0-9]*[a-z]*\.'
    t.value=t.value[:-1]
    t.lexer.push_state('text')
    return t


  # In the absorb, text, and lemmatize states, a newline returns to the base state
  def t_absorb_text_lemmatize_NEWLINE(self,t):
    r'\n'
    t.lexer.lineno += 1
    t.lexer.pop_state()
    return t

  t_RANGE="[1-9][0-9]*\-[1-9][0-9]*"
  t_NUMBER="[1-9][0-9]*"

  t_LETTER="[a-z]"

  #--- RULES FOR THE ABSORB STATE ---

  white=r'[\ \t]'
  nonflagnonwhite=r'[^\ \t\#\!\^\*\'\?\n\r]'
  internalonly=r'[^\n\^\r]'
  nonflag=r'[^\ \t\#\!\^\*\'\?\n\r]'
  absorb_regex=(white+'*'+'('+nonflagnonwhite+
                        '('+
                            '('+internalonly+'*'+nonflag+'+'+')'+
                            '|'+
                            nonflag+'*'+
                        ')'+
                      ')')

  @lex.TOKEN(absorb_regex)
  def t_absorb_ID(self,t):


    # Discard leading whitespace, token is not flag or newline
    # And has at least one non-whitespace character
    t.value=t.lexer.lexmatch.groups()[2]
    return t

  t_absorb_HASH="\#"
  t_absorb_EXCLAIM="\!"
  t_absorb_QUERY="\?"
  t_absorb_STAR="\*"
  t_absorb_PRIME="'"
  t_absorb_HAT="[\ \t]*\^[\ \t]*"

  #--- RULES FOR THE text STATE ----
  t_text_ID="[^\ \t \n\r]+"
  def t_text_SPACE(self,t):
    r'[\ \t]'
    # No token generated

  #--- RULES FOR THE lemmatize STATE
  t_lemmatize_ID="[^\;\n\r]+"
  t_lemmatize_SEMICOLON=r'\;[\ \t]*'

  #--- RULES FOR THE TRANSLATION STATE ---
  # In this state, linelabels are tokenised separately,
  # But everything else is free text
  def t_translation_LINELABEL(self,t):
    r'^([1-9][0-9]*[a-z]*)\.[\ \t]*'
    t.value=t.lexer.lexmatch.groups()[8]
    t.lexer.push_state('absorb')
    return t

  # Error handling rule
  def t_ANY_error(self,t):
      print "Illegal character '%s'" % t.value[0]
      t.lexer.skip(1)

  def __init__(self):
    self.lexer=lex.lex(module=self,reflags=re.MULTILINE)
