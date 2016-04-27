# -*- coding: utf-8 -*-
from __future__ import print_function

import ply.lex as lex
import re
import warnings
from pyoracc import _pyversion


class AtfLexer(object):

    def _keyword_dict(self, tokens, extra):
        keywords = {token.lower(): token for token in tokens}
        firstcap = {token.title(): token for token in tokens}
        keywords.update(firstcap)
        keywords.update(extra)
        return keywords

    def resolve_keyword(self, value, source, fallback=None, extra=None):
        if extra is None:
            extra = {}
        source = self._keyword_dict(source, extra)
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
        'LABEL',
        'INCLUDE',
        'SCORE'
    ]

    long_argument_structures = [
        'OBJECT',
        'SURFACE',
        'FRAGMENT',
        'HEADING'
    ]

    protocols = ['ATF', 'LEM', 'PROJECT', 'NOTE', "LINK",
                 "KEY", "BIB", "TR", 'CHECK', 'LEMMATIZER']

    protocol_keywords = ['LANG', 'USE', 'MATH', 'LEGACY', 'MYLINES',
                         'LEXICAL', 'UNICODE', 'DEF']

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
        'SCORELABEL',
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
        'CLOSER',
        'COMMA',
        'COMMENT',
        'EQUALBRACE'
    ]

    keyword_tokens = sorted(list(set(
        structures +
        long_argument_structures +
        protocols +
        protocol_keywords +
        dollar_keywords +
        translation_keywords
    )))

    tokens = sorted(list(set(
        keyword_tokens +
        base_tokens)))

    state_names = [
        'flagged',
        'text',
        'lemmatize',
        'nonequals',
        'parallel',  # translation
        'labeled',  # translation
        'interlinear',  # translation
        'transctrl',
        'para',
        'absorb'
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
    t_COMMA = "\,"
    t_PARBAR = "\|\|"

    t_INITIAL_transctrl_PARENTHETICALID = "\([^\n\r]*\)"

    def t_INITIAL_transctrl_WHITESPACE(self, t):
        r'[\t ]+'
        # NO TOKEN

    def t_MULTILINGUAL(self, t):
        "\=\="
        t.lexer.push_state("text")
        return t

    def t_EQUALBRACE(self, t):
        "^\=\{"
        t.lexer.push_state('text')
        return t

    def t_EQUALS(self, t):
        "\="
        t.lexer.push_state('flagged')
        return t

    def t_INITIAL_parallel_labeled_COMMENT(self, t):
        r'^\#+(?![a-zA-Z]+\:)'
        # Negative lookahead to veto protocols as comments
        t.lexer.push_state('absorb')
        return t

    def t_INITIAL_parallel_labeled_DOTLINE(self, t):
        r'^\s*\.\s*[\n\r]'
        # A line with just a dot, occurs in brm_4_19 at the end
        t.type = "NEWLINE"
        return t

    # In the base state, a newline doesn't change state
    def t_NEWLINE(self, t):
        r'\s*[\n\r]'
        t.lexer.lineno += t.value.count("\n")
        return t

    def t_INITIAL_parallel_labeled_ATID(self, t):
        '\@[a-zA-Z][a-zA-Z0-9\[\]]*\+?'
        t.value = t.value[1:]
        t.lexpos += 1
        t.type = self.resolve_keyword(t.value,
                                      AtfLexer.structures +
                                      AtfLexer.long_argument_structures,
                                      extra={
                                          "h1": "HEADING",
                                          "h2": "HEADING",
                                          "h3": "HEADING",
                                          "label+": "LABEL",
                                          "end": "END"
                                      },
                                      )

        if t.type == "INCLUDE":
            t.lexer.push_state('nonequals')

        if t.type == "END":
            t.lexer.pop_state()
            t.lexer.push_state('transctrl')

        if t.type == "LABEL":
            t.lexer.push_state("para")
            t.lexer.push_state("transctrl")

        if t.type == "TRANSLATION":
            t.lexer.push_state("transctrl")

        if t.type in AtfLexer.long_argument_structures + ["NOTE"]:
            t.lexer.push_state('flagged')
        if t.type is None:
            formatstring = u"Illegal @STRING '{}'".format(t.value)
            if _pyversion() == 2:
                formatstring = formatstring.encode('UTF-8')
            if self.skipinvalid:
                warnings.warn(formatstring, UserWarning)
                return
            else:
                raise SyntaxError(formatstring)
        return t

    def t_labeled_OPENR(self, t):
        "\@\("
        t.lexer.push_state("para")
        t.lexer.push_state("transctrl")
        return t

    def t_INITIAL_parallel_labeled_HASHID(self, t):
        '\#[a-zA-Z][a-zA-Z0-9\[\]]+\:'
        # Note that \:? absorbs a trailing colon in protocol keywords
        t.value = t.value[1:-1]
        t.lexpos += 1
        t.type = self.resolve_keyword(t.value,
                                      AtfLexer.protocols,
                                      extra={'CHECK': 'CHECK'})
        if t.type == "KEY":
            t.lexer.push_state('nonequals')
        if t.type == "LEM":
            t.lexer.push_state('lemmatize')
        if t.type == "TR":
            t.lexer.push_state('interlinear')
        if t.type in ['PROJECT', "BIB"]:
            t.lexer.push_state('flagged')
        if t.type in ['CHECK']:
            t.lexer.push_state('absorb')
        if t.type == "NOTE":
            t.lexer.push_state('para')
        if t.type is None:
            formatstring = u"Illegal #STRING '{}'".format(t.value)
            if _pyversion() == 2:
                formatstring = formatstring.encode('UTF-8')
            if self.skipinvalid:
                warnings.warn(formatstring, UserWarning)
                return
            else:
                raise SyntaxError(formatstring)
        return t

    def t_LINELABEL(self, t):
        r'^[^\ \t\n]*\.'
        t.value = t.value[:-1]
        t.lexer.push_state('text')
        return t

    def t_SCORELABEL(self, t):
        r'^[^.:\ \t]*\:'
        t.value = t.value[:-1]
        t.lexer.push_state('text')
        return t

    def t_ID(self, t):
        u'[a-zA-Z0-9][a-zA-Z\'\u2019\xb4\/\.0-9\:\-\[\]_\u2080-\u2089]*'
        t.value = t.value.replace(u'\u2019', "'")
        t.value = t.value.replace(u'\xb4', "'")
        t.type = self.resolve_keyword(t.value,
                                      AtfLexer.protocol_keywords +
                                      AtfLexer.dollar_keywords +
                                      AtfLexer.structures +
                                      AtfLexer.long_argument_structures, 'ID',
                                      extra={
                                          'fragments': "FRAGMENT",
                                          "parallel": "PARALLEL"
                                      },
                                      )

        if t.type in ['LANG']:
            t.lexer.push_state('flagged')

        if t.type in set(AtfLexer.structures +
                         AtfLexer.long_argument_structures) - set(["NOTE"]):
            # Since @structure tokens are so important to the grammar,
            # the keywords refering to structural elements in strict dollar
            # lines must be DIFFERENT TOKENS IN THE LEXER
            t.type = "REFERENCE"
        return t

    # In the flagged, text, transctrl and lemmatize states,
    # one or more newlines returns to the base state
    def t_flagged_text_lemmatize_transctrl_nonequals_absorb_NEWLINE(self, t):
        r'[\n\r]+'
        t.lexer.lineno += len(t.value)
        t.lexer.pop_state()
        return t

    # --- RULES FOR THE TRANSLATION STATES ---
    # In this state, the base state is free text
    # And certain tokens deviate from that, rather
    # than the other way round as for base state

    # Unicode 2019 is right single quotation
    # Unicode 02cCA is MODIFIER LETTER ACUTE ACCENT
    # Unicode 2032  is PRIME
    # All of these could be used as prime
    def t_transctrl_ID(self, t):
        u'[a-zA-Z0-9][a-zA-Z\'\u2019\u2032\u02CA\xb4\/\.0-9\:\-\[\]_' \
          u'\u2080-\u2089]*'
        t.value = t.value.replace(u'\u2019', "'")
        t.value = t.value.replace(u'\u2032', "'")
        t.value = t.value.replace(u'\u02CA', "'")
        t.value = t.value.replace(u'\xb4', "'")
        t.type = self.resolve_keyword(t.value,
                                      AtfLexer.protocol_keywords +
                                      AtfLexer.dollar_keywords +
                                      AtfLexer.structures +
                                      AtfLexer.translation_keywords +
                                      AtfLexer.long_argument_structures, 'ID',
                                      extra={'fragments': "FRAGMENT"}
                                      )

        if t.type == "LABELED":
            t.lexer.pop_state()
            t.lexer.push_state('labeled')
            t.lexer.push_state('transctrl')
        if t.type == "PARALLEL":
            t.lexer.pop_state()
            t.lexer.push_state('parallel')
            t.lexer.push_state('transctrl')

        if t.type in set(AtfLexer.structures +
                         AtfLexer.long_argument_structures) - set(["NOTE"]):
            # Since @structure tokens are so important to the grammar,
            # the keywords refering to structural elements in strict dollar
            # lines must be DIFFERENT TOKENS IN THE LEXER
            t.type = "REFERENCE"
        return t

    def t_parallel_LINELABEL(self, t):
        r'^([^\.\ \t]*)\.[\ \t]*'
        t.value = t.value.strip(" \t.")
        return t

    def t_parallel_labeled_DOLLAR(self, t):
        "^\$"
        t.lexer.push_state("absorb")
        return t

    t_transctrl_MINUS = "\-\ "

    def t_transctrl_CLOSER(self, t):
        "\)"
        t.lexer.pop_state()
        return t

    # In parallel states, a newline doesn't change state
    # A newline followed by a space gives continuation
    def t_parallel_NEWLINE(self, t):
        r'\s*[\n\r](?![ \t])'
        t.lexer.lineno += t.value.count("\n")
        return t

    # In interlinear states, a newline which is not continuation leaves state
    # A newline followed by a space gives continuation
    def t_interlinear_NEWLINE(self, t):
        r'\s*[\n\r](?![ \t])'
        t.lexer.lineno += t.value.count("\n")
        t.lexer.pop_state()
        return t

    # In labeled translation, a newline doesn't change state
    # A newline just passed through
    def t_labeled_NEWLINE(self, t):
        r'\s*[\n\r]'
        t.lexer.lineno += t.value.count("\n")
        return t

    # Flag characters (#! etc ) don't apply in translations
    # But reference anchors ^1^ etc do.
    # lines beginning with a space are continuations
    white = r'[\ \t]*'
    translation_regex = white + "([^\^\n\r]|([\n\r](?=[ \t])))+" + white

    @lex.TOKEN(translation_regex)
    def t_parallel_interlinear_ID(self, t):
        t.value = t.value.strip()
        t.value = t.value.replace("\r ", "\r")
        t.value = t.value.replace("\n ", "\n")
        t.value = t.value.replace("\n", " ")
        t.value = t.value.replace("\r", " ")
        return t

    def t_parallel_labeled_AMPERSAND(self, t):
        r'\&'
        # New document, so leave translation state
        t.lexer.pop_state()
        return t

    # This next rule should be unnecessary, as
    # paragraphs absorb multiple lines anyway
    # But because some malformed texts terminate translation blocks
    # with the next label, not a double-newline, fake labels, lines
    # which look like
    # labels, can cause apparent terminations of blocks
    # So we add this rule to accommodate these
    t_labeled_ID = "^[^\n\r]+"
    # --- RULES FOR THE ABSORB STATE ---
    # Used for states where only flag# characters! and ^1^ references
    # Are separately tokenised

    nonflagnonwhite = r'[^\ \t\#\!\^\*\?\n\r\=]'
    internalonly = r'[^\n\^\r\=]'
    nonflag = r'[^\ \t\#\!\^\*\?\n\r\=]'
    many_int_then_nonflag = '(' + internalonly + '*' + nonflag + '+' + ')'
    many_nonflag = nonflag + '*'
    intern_or_nonflg = '(' + many_int_then_nonflag + '|' + many_nonflag + ')'
    flagged_regex = (white + '(' + nonflagnonwhite + intern_or_nonflg +
                     ')' + white)

    @lex.TOKEN(flagged_regex)
    def t_flagged_ID(self, t):
        # Discard leading whitespace, token is not flag or newline
        # And has at least one non-whitespace character
        t.value = t.value.strip()
        return t

    t_flagged_HASH = "\#"
    t_flagged_EXCLAIM = "\!"
    t_flagged_QUERY = "\?"
    t_flagged_STAR = "\*"
    t_flagged_parallel_para_HAT = "[\ \t]*\^[\ \t]*"
    t_flagged_EQUALS = "\="
    # --- Rules for paragaph state----------------------------------
    # Free text, ended by double new line

    terminates_paragraph = "(\#|\@|\&|\Z|(^[^.\ \t]*\.))"

    @lex.TOKEN(r'([^\^\n\r]|([\n\r](?!\s*[\n\r])(?!' +
               terminates_paragraph + ')))+')
    def t_para_ID(self, t):
        t.lexer.lineno += t.value.count("\n")
        t.value = t.value.strip()
        return t

    # Paragraph state is ended by a double newline
    def t_para_NEWLINE(self, t):
        r'[\n\r]\s*[\n\r]+'
        t.lexer.lineno += t.value.count("\n")
        t.lexer.pop_state()
        return t

    # BUT, exceptionally to fix existing bugs in active members of corpus,
    # it is also ended by an @label or an @(), or a new document,
    # Or a linelabel, or the end of the stream.
    # and these tokens are not absorbed by this token
    # Translation paragraph state is ended by a double newline
    @lex.TOKEN(r'[\n\r](?=' + terminates_paragraph + ')')
    def t_para_MAGICNEWLINE(self, t):
        t.lexer.lineno += t.value.count("\n")
        t.lexer.pop_state()
        t.type = "NEWLINE"
        return t

    # --- RULES FOR THE nonequals STATE -----
    # Absorb everything except an equals
    def t_nonequals_ID(self, t):
        "[^\=\n\r]+"
        t.value = t.value.strip()
        return t

    t_nonequals_EQUALS = "\="

    # --- RULES FOR THE absorb STATE -----
    # Absorb everything
    def t_absorb_ID(self, t):
        "[^\n\r]+"
        t.value = t.value.strip()
        return t

    # --- RULES FOR THE text STATE ----
    t_text_ID = "[^\ \t \n\r]+"

    def t_text_SPACE(self, t):
        r'[\ \t]'
        # No token generated

    # --- RULES FOR THE lemmatize STATE
    t_lemmatize_ID = "[^\;\n\r]+"
    t_lemmatize_SEMICOLON = r'\;[\ \t]*'

    # Error handling rule
    def t_ANY_error(self, t):
        formatstring = u"PyOracc got an illegal character '{}'".format(t.value[0])
        if _pyversion() == 2:
            formatstring = formatstring.encode('UTF-8')
        if self.skipinvalid:
            t.lexer.skip(1)
            warnings.warn(formatstring, UserWarning)
        else:
            raise SyntaxError(formatstring)

    def __init__(self, skipinvalid=False):
        self.skipinvalid = skipinvalid
        self.lexer = lex.lex(module=self, reflags=re.MULTILINE)
