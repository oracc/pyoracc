'''
Copyright 2015, 2016 University College London.

This file is part of PyORACC.

PyORACC is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyORACC is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyORACC. If not, see <http://www.gnu.org/licenses/>.
'''

# -*- coding: utf-8 -*-
from __future__ import print_function

import ply.lex as lex
import re
import warnings
from pyoracc import _pyversion
from pyoracc.atf.common.atflexicon import AtfLexicon


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

    structures = AtfLexicon.STRUCTURES

    long_argument_structures = AtfLexicon.LONG_ARGUMENT_STRUCTURES

    protocols = AtfLexicon.PROTOCOLS

    protocol_keywords = AtfLexicon.PROTOCOL_KEYWORDS

    translation_keywords = AtfLexicon.TRANSLATION_KEYWORDS

    dollar_keywords = AtfLexicon.DOLLAR_KEYWORDS

    base_tokens = AtfLexicon.BASE_TOKENS

    keyword_tokens = AtfLexicon.KEYWORD_TOKENS

    tokens = AtfLexicon.TOKENS

    exclusive_state_names = AtfLexicon.EXCLUSIVE_STATE_NAMES

    exc_states = AtfLexicon.EXC_STATES

    inclusive_state_names = AtfLexicon.INCLUSIVE_STATE_NAMES
    inc_states = AtfLexicon.INC_STATES

    states = AtfLexicon.STATES

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
        '^\@[a-zA-Z][a-zA-Z0-9\[\]]*\+?'
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
            if not self.skipinvalid or t.lexer.current_state() != 'INITIAL':
                t.lexer.pop_state()
            t.lexer.push_state('transctrl')

        if t.type == "LABEL":
            t.lexer.push_state("para")
            t.lexer.push_state("transctrl")

        if t.type == "TRANSLATION":
            t.lexer.push_state("transctrl")

        if t.type == "SCORE":
            t.lexer.push_state('score')

        if t.type in AtfLexer.long_argument_structures + ["NOTE"]:
            t.lexer.push_state('flagged')
        if t.type is None:
            formatstring = u"Illegal @STRING '{}'".format(t.value)
            valuestring = t.value
            if _pyversion() == 2:
                formatstring = formatstring.encode('UTF-8')
                valuestring = valuestring.encode('UTF-8')
            if self.skipinvalid:
                warnings.warn(formatstring, UserWarning)
                return
            else:
                raise SyntaxError(formatstring,
                                  (None, t.lineno, t.lexpos, valuestring))
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
        # Use lower here since there are some ATF files with
        # the protocol incorrectly written as #NOTE:
        t.type = self.resolve_keyword(t.value.lower(),
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
            valuestring = t.value
            if _pyversion() == 2:
                formatstring = formatstring.encode('UTF-8')
                valuestring = valuestring.encode('UTF-8')
            if self.skipinvalid:
                warnings.warn(formatstring, UserWarning)
                return
            else:
                raise SyntaxError(formatstring,
                                  (None, t.lineno, t.lexpos, valuestring))
        return t

    def t_LINELABEL(self, t):
        r'^[^\ \t\n]*\.'
        t.value = t.value[:-1]
        t.lexer.push_state('text')
        return t

    def t_score_SCORELABEL(self, t):
        r'^[^.:\ \t\#][^.:\ \t]*\:'
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
        # print("id " + t.value + t.type)
        if t.type in ['LANG']:
            t.lexer.push_state('flagged')

        if t.type in set(AtfLexer.structures +
                         AtfLexer.long_argument_structures) - {"NOTE"}:
            # Since @structure tokens are so important to the grammar,
            # the keywords refering to structural elements in strict dollar
            # lines must be DIFFERENT TOKENS IN THE LEXER
            t.type = "REFERENCE"
        # print("id " + t.value + t.type)
        return t

    # In the flagged, text, transctrl and lemmatize states,
    # one or more newlines returns to the base state
    # In several of the files such as bb_2_006.atf the blank line contains tab
    # or other trailing whitespace
    def t_flagged_text_lemmatize_transctrl_nonequals_absorb_NEWLINE(self, t):
        r'[\n\r]*\s*[\n\r]+'
        t.lexer.lineno += t.value.count("\n")
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
                         AtfLexer.long_argument_structures) - {"NOTE"}:
            # Since @structure tokens are so important to the grammar,
            # the keywords refering to structural elements in strict dollar
            # lines must be DIFFERENT TOKENS IN THE LEXER
            t.type = "REFERENCE"
        return t

    t_parallel_QUERY = "\?"

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
    # translation_regex1 and translation_regex2 are identical appart from the
    # fact that the first character may not be a ?
    # We are looking for a string that does not start with ? it may include
    # newlines if they are followed by a whitespace.
    translation_regex1 = '([^\?\^\n\r]|([\n\r](?=[ \t])))'
    translation_regex2 = '([^\^\n\r]|([\n\r](?=[ \t])))*'
    translation_regex = white + translation_regex1 + translation_regex2 + white

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

    terminates_para = \
        "(\#|\@[^i][^\{]|\&|\Z|(^[0-9]+[\'\u2019\u2032\u02CA\xb4]?\.))"

    @lex.TOKEN(r'([^\^\n\r]|(\r?\n(?!\s*\r?\n)(?!' +
               terminates_para + ')))+')
    def t_para_ID(self, t):
        t.lexer.lineno += t.value.count("\n")
        t.value = t.value.strip()
        return t

    # Paragraph state is ended by a double newline
    def t_para_NEWLINE(self, t):
        r'\r?\n\s*[\n\r]*\n'
        t.lexer.lineno += t.value.count("\n")
        t.lexer.pop_state()
        return t

    # BUT, exceptionally to fix existing bugs in active members of corpus,
    # it is also ended by an @label or an @(), or a new document,
    # Or a linelabel, or the end of the stream. Importantly it does not end
    # by @i{xxx} which is used for un translated words.
    # and these tokens are not absorbed by this token
    # Translation paragraph state is ended by a double newline
    @lex.TOKEN(r'\r?\n(?=' + terminates_para + ')')
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
        fstring = u"PyOracc got an illegal character " \
                  u"'{}' at line number '{}' at lex pos '{}'" \
            .format(t.value, t.lineno, t.lexpos)
        valuestring = t.value
        if _pyversion() == 2:
            fstring = fstring.encode('UTF-8')
            valuestring = valuestring.encode('UTF-8')
        if self.skipinvalid:
            t.lexer.skip(1)
            warnings.warn(fstring, UserWarning)
            return
        else:
            raise SyntaxError(fstring,
                              (None, t.lineno, t.lexpos, valuestring))

    def __init__(self, skipinvalid=False, debug=0, log=lex.NullLogger()):
        self.skipinvalid = skipinvalid
        self.lexer = lex.lex(module=self, reflags=re.MULTILINE, debug=debug,
                             debuglog=log)
