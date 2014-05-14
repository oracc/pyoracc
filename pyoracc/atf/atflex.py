import ply.lex as lex
import re

protocols={}
for token in ['ATF','LEM','PROJECT','NOTE']:
  protocols[token.lower()]=token

protocol_tokens={}
for token in ['LANG','USE','MATH','UNICODE']:
  protocol_tokens[token.lower()]=token

divisions={}
for division in ['TABLET','ENVELOPE','PRISM','BULLA','FRAGMENT','OBJECT',
  'SEAL','OBVERSE','REVERSE','LEFT','RIGHT','TOP','BOTTOM','FACE',
  'SURFACE','EDGE','COLUMN','CATCHLINE','COLOPHON','DATE','SIGNATURES',
  'SIGNATURE','SUMMARY','WITNESSES','TRANSLATION','NOTE','M']:
  divisions[division.lower()]=division

dollar_tokens={}
for token in ['AT','MOST','ABOUT',
  'SEVERAL','SOME','REST','OF','START','BEGINNING','MIDDLE','END',
  'COLUMNS','LINE','LINES','CASE','CASES','SURFACE',
  'BLANK','BROKEN','EFFACED','ILLEGIBLE','MISSING','TRACES',
  'RULING','SINGLE','DOUBLE','TRIPLE']:
  dollar_tokens[token.lower()]=token


flags={
  '!':'REMARK',
  '#':'BROKEN',
  '?':'QUERY',
  '*':'COLLATED'
}

tokens=([
  'CODE',
  'NEWLINE',
  'SPACE',
  'OTHER',
  'LINELABEL',
  'ID',
  'PROTOCOL',
  'DOLLAR',
  'LOOSE',
  'RANGE',
  'NUMBER',
  'COMMENT',
  'PRIME',
  'DIVISION',
  'NOTEREF'
]+protocols.values()+protocol_tokens.values()+
  divisions.values()+flags.values()+dollar_tokens.values())

states=(
  ('protocol','exclusive'),
  ('code','exclusive'),
  ('division','exclusive'),
  ('text','exclusive'),
  ('lemmatize','exclusive'),
  ('dollar','exclusive'),
  ('comment','exclusive'),
  ('note','exclusive')
)

def t_LINELABEL(t):
  r'^[1-9][0-9]*[a-z]*\.'
  t.value=t.value[:-1]
  t.lexer.begin('text')
  return t

def t_CODE(t):
  '^&[A-Z][0-9]+\ \=\ '
  t.value=t.value[1:-3]
  t.lexer.begin('code')
  return t
  # Match e.g. &X0001 at the start of a line

def t_PROTOCOL(t):
  "^\#[a-z]*:\ "
  t.value=t.value[1:-2]
  t.type=protocols.get(t.value,'PROTOCOL')
  if t.value=="lem":
    t.lexer.begin("lemmatize")
  elif t.value=="note":
    t.lexer.begin("comment")
  else:
    t.lexer.begin('protocol')
  return t

def t_COMMENT(t):
  "^\#\ "
  t.lexer.begin("comment")
  return t

def t_DIVISION(t):
  "^@[a-z]*"
  t.value=t.value[1:]
  t.type=divisions.get(t.value,'DIVISION')
  if t.type=="NOTE":
    t.lexer.begin("comment")
  else:
    t.lexer.begin('division')
  return t

def t_DOLLAR(t):
  r'^\$\ '
  t.lexer.begin('dollar')
  return t

def t_dollar_LOOSE(t):
  # Currently violates images
  "\((.*)\)"
  t.value=t.value[1:-1]
  return t

def t_dollar_ID(t):
  '[a-zA-Z]+'
  t.type=dollar_tokens.get(t.value,'ID')
  if t.type=='ID':
    t.type=divisions.get(t.value,'ID')
  return t

t_dollar_RANGE="[1-9][0-9]*\-[1-9][0-9]"
t_dollar_NUMBER="[1-9][0-9]*"

def t_protocol_ID(t):
  '[a-zA-Z\-\/]+'
  t.type=protocol_tokens.get(t.value,'ID')
  return t

def t_code_ID(t):
  r'[^\n]+'
  return t

def t_division_FLAG(t):
  r'[\?\!\#\*]'
  t.type=flags[t.value]
  return t

t_division_ID="[a-z]"
t_division_NUMBER="[1-9][0-9]*"
t_division_PRIME="'"

LANG="lang"
t_protocol_USE="use"
t_protocol_UNICODE="unicode"
t_protocol_MATH="math"

# Does NOT apply when parsing CODE LINE, or COMMENT as that is literal and
# inside the token
def t_INITIAL_division_protocol_dollar_SPACE(t):
  r'[ ]'
  # No return, don't add to token stream

t_text_OTHER="."
t_lemmatize_OTHER="."
t_comment_OTHER="."

def t_division_NOTEREF(t):
  "\^(.*?)\^"
  t.value=t.value[1:-1]
  return t

def t_ANY_NEWLINE(t):
  r'\n'
  t.lexer.begin('INITIAL')
  # No return, don't add to token stream

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

lexer=lex.lex(reflags=re.MULTILINE)
