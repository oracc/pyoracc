import ply.lex as lex
import re


class AtfLexer(object):

    def _keyword_dict(self, tokens, extra):
        keywords= {token.lower(): token for token in tokens}
        keywords.update(extra)
        return keywords

    def resolve_keyword(self, value, source, fallback=None, extra={}):
        source = self._keyword_dict(source, extra)
        if not fallback:
            return source[value]
        return source.get(value, fallback)

    structures = [
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
        'COMPOSITE',
        'LABEL'
    ]

    long_argument_structures = [
        'OBJECT',
        'SURFACE',
        'FRAGMENT',
        'HEADING'
    ]

    protocols = ['ATF', 'LEM', 'PROJECT', 'NOTE', "LINK"]

    protocol_keywords = ['LANG', 'USE', 'MATH', 'UNICODE', 'DEF']

    translation_keywords = ['PARALLEL', 'PROJECT', "LABELED"]

    dollar_keywords = [
        'MOST', 'LEAST', 'ABOUT',
        'SEVERAL', 'SOME', 'REST', 'OF', 'START', 'BEGINNING', 'MIDDLE', 'END',
        'COLUMNS', 'LINE', 'LINES', 'CASE', 'CASES', 'SURFACE',
        'BLANK', 'BROKEN', 'EFFACED', 'ILLEGIBLE', 'MISSING', 'TRACES',
        'RULING', 'SINGLE', 'DOUBLE', 'TRIPLE', 'AT']

    base_tokens = [
        'AMPERSAND',
        'LINELABEL',
        'ID',
        'DOLLAR',
        'PARENTHETICALID',
        'HAT',
        'SEMICOLON',
        'EQUALS',
        'MULTILINGUAL',
        'LSQUARE',
        'RSQUARE',
        'EXCLAIM',
        'QUERY',
        'STAR',
        'RANGE',
        'HASH',
        'NEWLINE',
        'REFERENCE',
        'MINUS',
        'FROM',
        'TO',
        'PARBAR',
        'OPENR',
        'CLOSER'
    ]

    keyword_tokens = list(set(
        structures +
        long_argument_structures +
        protocols +
        protocol_keywords +
        dollar_keywords +
        translation_keywords
    ))

    tokens = list(set(
        keyword_tokens +
        base_tokens))

    state_names = [
        'absorb',
        'text',
        'lemmatize',
        'parallel',  # translation
        'labeled',   # translation
        'transctrl',
        'transpara'
    ]

    states = [(state, 'exclusive') for state in state_names]

    t_AMPERSAND = "\&"
    t_HASH = "\#"
    t_EXCLAIM = "\!"
    t_QUERY = "\?"
    t_STAR = "\*"
    t_DOLLAR = "\$"
    t_MINUS = "\-"
    t_FROM = "\<\<"
    t_TO = "\>\>"
    t_PARBAR = "\|\|"


    t_PARENTHETICALID = "\([^\)\n\r]*\)"

    def t_INITIAL_transctrl_WHITESPACE(self, t):
        r'[\t ]+'
        # NO TOKEN

    def  t_MULTILINGUAL(self,t):
        "\=\="
        t.lexer.push_state("text")
        return t

    def t_EQUALS(self, t):
        "\="
        t.lexer.push_state('absorb')
        return t



    def t_INITIAL_parallel_labeled_COMMENT(self, t):
        r'^\#[^\n\r\:]*([\ \t][^\n\r]*)?\n'
        t.type = "NEWLINE"
        return t

    def t_INITIAL_parallel_labeled_DOTLINE(self,t):
        r'^\s*\.\s*\n'
        # A line with just a dot, occurs in brm_4_19 at the end
        t.type = "NEWLINE"
        return t

        # In the multi-line base states, a newline doesn't change state
    def t_INITIAL_parallel_labeled_NEWLINE(self, t):
        r'\s*\n'
        t.lexer.lineno += 1
        return t

    def t_INITIAL_parallel_labeled_ATID(self, t):
        '\@[a-zA-Z][a-zA-Z0-9\[\]]+\+?'
        t.value = t.value[1:]

        t.type = self.resolve_keyword(t.value,
                                      AtfLexer.structures +
                                      AtfLexer.long_argument_structures,
                                      extra={
                                        "h1":"HEADING",
                                        "h2":"HEADING",
                                        "h3":"HEADING",
                                        "label+":"LABEL",
                                      },
                                      )

        if t.type == "LABEL":
            t.lexer.push_state("transpara")
            t.lexer.push_state("transctrl")

        if t.type in AtfLexer.long_argument_structures + ["NOTE"]:
            t.lexer.push_state('absorb')
        return t

    def t_labeled_OPENR(self, t):
        "\@\("
        t.lexer.push_state("transpara")
        t.lexer.push_state("transctrl")
        return t

    def t_INITIAL_parallel_labeled_HASHID(self, t):
        '\#[a-zA-Z][a-zA-Z0-9\[\]]+\:'
        # Note that \:? absorbs a trailing colon in protocol keywords
        t.value = t.value[1:-1]
        t.type = self.resolve_keyword(t.value,
                                      AtfLexer.protocols)
        if t.type == "LEM":
            t.lexer.push_state('lemmatize')
        if t.type in ['NOTE', 'PROJECT']:
            t.lexer.push_state('absorb')
        return t

    def t_LINELABEL(self, t):
        r'^[^.\ \t]*\.'
        t.value = t.value[:-1]
        t.lexer.push_state('text')
        return t

    def t_parallel_labeled_DOLLAR(self,t):
        "^\$"
        t.lexer.push_state("transctrl")
        return t

    def t_INITIAL_transctrl_ID(self, t):
        '[a-zA-Z0-9][a-zA-Z\'\.0-9\-\[\]]*'

        t.type = self.resolve_keyword(t.value,
                                      AtfLexer.protocol_keywords +
                                      AtfLexer.dollar_keywords +
                                      AtfLexer.structures +
                                      AtfLexer.translation_keywords +
                                      AtfLexer.long_argument_structures, 'ID')

        if t.type in ['LANG']:
            t.lexer.push_state('absorb')
        if t.type == "LABELED":
            t.lexer.push_state('labeled')
            t.lexer.push_state('transctrl')
        if t.type == "PARALLEL":
            t.lexer.push_state('parallel')
            t.lexer.push_state('transctrl')

        if t.type in set(AtfLexer.structures +
                         AtfLexer.long_argument_structures) - set(["NOTE"]):
            # Since @structure tokens are so important to the grammar,
            # the keywords refering to structural elements in strict dollar
            # lines must be DIFFERENT TOKENS IN THE LEXER
            t.type = "REFERENCE"
        return t

    # In the absorb, text, transctrl and lemmatize states,
    # a newline returns to the base state
    def t_absorb_text_lemmatize_transctrl_NEWLINE(self, t):
        r'\n'
        t.lexer.lineno += 1
        t.lexer.pop_state()
        return t

    #--- RULES FOR THE TRANSLATION STATES ---
    # In this state, the base state is free text
    # And certain tokens deviate from that, rather
    # than the other way round as for base state

    def t_parallel_LINELABEL(self, t):
        r'^([^\.\ \t]*)\.[\ \t]*'
        t.value = t.value.strip(" \t.")
        return t


    t_transctrl_MINUS = "\-\ "
    
    def t_transctrl_CLOSER(self,t):
        "\)"
        t.lexer.pop_state()
        return t

    #--- RULES FOR THE ABSORB STATE ---

    white = r'[\ \t]*'
    nonflagnonwhite = r'[^\ \t\#\!\^\*\?\n\r\=]'
    internalonly = r'[^\n\^\r\=]'
    nonflag = r'[^\ \t\#\!\^\*\?\n\r\=]'
    many_int_then_nonflag = '(' + internalonly + '*' + nonflag + '+' + ')'
    many_nonflag = nonflag + '*'
    intern_or_nonflg = '(' + many_int_then_nonflag + '|' + many_nonflag + ')'
    absorb_regex = (white + '(' + nonflagnonwhite + intern_or_nonflg +
                    ')' + white )

    @lex.TOKEN(absorb_regex)
    def t_absorb_ID(self, t):
        # Discard leading whitespace, token is not flag or newline
        # And has at least one non-whitespace character
        t.value = t.value.strip()
        return t


    # Flag characters (#! etc ) don't apply in translations
    # But reference anchors ^1^ etc do.
    translation_regex = white + "[^\^\n\r]+" + white

    @lex.TOKEN(translation_regex)
    def t_parallel_ID(self,t):
        t.value = t.value.strip()
        return t

    def t_transpara_ID(self,t):
        r'([^\^\n\r]|([\n\r](?!\s*[\n\r])(?!(\@label|\@\())))+'
        t.value = t.value.strip()
        return t
    
    # Translation paragraph state is ended by a double newline
    def t_transpara_NEWLINE(self,t):
        r'[\n\r]\s*[\n\r]+'    
        t.lexer.lineno += t.value.count("\n")
        t.lexer.pop_state()
        return t

    # BUT, exceptionally to fix existing bugs in active members of corpus,
    # it is ended by an @label or an @(), and these tokens are not absorbed by this token
    # Translation paragraph state is ended by a double newline
    def t_transpara_MAGICNEWLINE(self,t):
        r'[\n\r](?=(\@label|\@\())'    
        t.lexer.lineno += 1
        t.lexer.pop_state()
        t.type = "NEWLINE"
        return t


    t_absorb_HASH = "\#"
    t_absorb_EXCLAIM = "\!"
    t_absorb_QUERY = "\?"
    t_absorb_STAR = "\*"
    t_absorb_parallel_transpara_HAT = "[\ \t]*\^[\ \t]*"
    t_absorb_EQUALS = "\="

    #--- RULES FOR THE text STATE ----
    t_text_ID = "[^\ \t \n\r]+"

    def t_text_SPACE(self, t):
        r'[\ \t]'
        # No token generated

    #--- RULES FOR THE lemmatize STATE
    t_lemmatize_ID = "[^\;\n\r]+"
    t_lemmatize_SEMICOLON = r'\;[\ \t]*'

    # Error handling rule
    def t_ANY_error(self, t):
        print "Illegal character '%s'" % t.value[0]
        raise SyntaxError
        t.lexer.skip(1)

    def __init__(self):
        self.lexer = lex.lex(module=self, reflags=re.MULTILINE)
