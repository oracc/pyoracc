# $ANTLR 3.1.3 Mar 18, 2009 10:09:25 atf.g 2014-05-14 16:39:11

import sys
from antlr3 import *
from antlr3.compat import set, frozenset


# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
COMMA=9
NEWLINE=4
EQUAL=11
DIGIT=5
SPACE=8
OTHER=10
UPPER=6
LOWER=7
T__12=12
T__13=13
EOF=-1


class atfLexer(Lexer):

    grammarFileName = "atf.g"
    antlr_version = version_str_to_tuple("3.1.3 Mar 18, 2009 10:09:25")
    antlr_version_str = "3.1.3 Mar 18, 2009 10:09:25"

    def __init__(self, input=None, state=None):
        if state is None:
            state = RecognizerSharedState()
        super(atfLexer, self).__init__(input, state)


        self.dfa2 = self.DFA2(
            self, 2,
            eot = self.DFA2_eot,
            eof = self.DFA2_eof,
            min = self.DFA2_min,
            max = self.DFA2_max,
            accept = self.DFA2_accept,
            special = self.DFA2_special,
            transition = self.DFA2_transition
            )






    # $ANTLR start "T__12"
    def mT__12(self, ):

        try:
            _type = T__12
            _channel = DEFAULT_CHANNEL

            # atf.g:7:7: ( '&' )
            # atf.g:7:9: '&'
            pass 
            self.match(38)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "T__12"



    # $ANTLR start "T__13"
    def mT__13(self, ):

        try:
            _type = T__13
            _channel = DEFAULT_CHANNEL

            # atf.g:8:7: ( ' = ' )
            # atf.g:8:9: ' = '
            pass 
            self.match(" = ")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "T__13"



    # $ANTLR start "DIGIT"
    def mDIGIT(self, ):

        try:
            _type = DIGIT
            _channel = DEFAULT_CHANNEL

            # atf.g:37:6: ( '0' .. '9' )
            # atf.g:37:8: '0' .. '9'
            pass 
            self.matchRange(48, 57)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "DIGIT"



    # $ANTLR start "UPPER"
    def mUPPER(self, ):

        try:
            _type = UPPER
            _channel = DEFAULT_CHANNEL

            # atf.g:38:6: ( 'A' .. 'Z' )
            # atf.g:38:8: 'A' .. 'Z'
            pass 
            self.matchRange(65, 90)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "UPPER"



    # $ANTLR start "LOWER"
    def mLOWER(self, ):

        try:
            _type = LOWER
            _channel = DEFAULT_CHANNEL

            # atf.g:39:6: ( 'a' .. 'z' )
            # atf.g:39:8: 'a' .. 'z'
            pass 
            self.matchRange(97, 122)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "LOWER"



    # $ANTLR start "SPACE"
    def mSPACE(self, ):

        try:
            _type = SPACE
            _channel = DEFAULT_CHANNEL

            # atf.g:40:6: ( ' ' )
            # atf.g:40:8: ' '
            pass 
            self.match(32)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "SPACE"



    # $ANTLR start "COMMA"
    def mCOMMA(self, ):

        try:
            _type = COMMA
            _channel = DEFAULT_CHANNEL

            # atf.g:41:6: ( ',' )
            # atf.g:41:8: ','
            pass 
            self.match(44)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "COMMA"



    # $ANTLR start "EQUAL"
    def mEQUAL(self, ):

        try:
            _type = EQUAL
            _channel = DEFAULT_CHANNEL

            # atf.g:42:6: ( '=' )
            # atf.g:42:8: '='
            pass 
            self.match(61)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "EQUAL"



    # $ANTLR start "OTHER"
    def mOTHER(self, ):

        try:
            _type = OTHER
            _channel = DEFAULT_CHANNEL

            # atf.g:43:6: (~ ( DIGIT | UPPER | LOWER | SPACE | '\\r' | '\\n' | COMMA ) )
            # atf.g:43:7: ~ ( DIGIT | UPPER | LOWER | SPACE | '\\r' | '\\n' | COMMA )
            pass 
            if (0 <= self.input.LA(1) <= 9) or (11 <= self.input.LA(1) <= 12) or (14 <= self.input.LA(1) <= 31) or (33 <= self.input.LA(1) <= 43) or (45 <= self.input.LA(1) <= 47) or (58 <= self.input.LA(1) <= 64) or (91 <= self.input.LA(1) <= 96) or (123 <= self.input.LA(1) <= 65535):
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse




            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "OTHER"



    # $ANTLR start "NEWLINE"
    def mNEWLINE(self, ):

        try:
            _type = NEWLINE
            _channel = DEFAULT_CHANNEL

            # atf.g:46:5: ( '\\r' '\\n' | '\\n' )
            alt1 = 2
            LA1_0 = self.input.LA(1)

            if (LA1_0 == 13) :
                alt1 = 1
            elif (LA1_0 == 10) :
                alt1 = 2
            else:
                nvae = NoViableAltException("", 1, 0, self.input)

                raise nvae

            if alt1 == 1:
                # atf.g:46:9: '\\r' '\\n'
                pass 
                self.match(13)
                self.match(10)


            elif alt1 == 2:
                # atf.g:47:9: '\\n'
                pass 
                self.match(10)


            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "NEWLINE"



    def mTokens(self):
        # atf.g:1:8: ( T__12 | T__13 | DIGIT | UPPER | LOWER | SPACE | COMMA | EQUAL | OTHER | NEWLINE )
        alt2 = 10
        alt2 = self.dfa2.predict(self.input)
        if alt2 == 1:
            # atf.g:1:10: T__12
            pass 
            self.mT__12()


        elif alt2 == 2:
            # atf.g:1:16: T__13
            pass 
            self.mT__13()


        elif alt2 == 3:
            # atf.g:1:22: DIGIT
            pass 
            self.mDIGIT()


        elif alt2 == 4:
            # atf.g:1:28: UPPER
            pass 
            self.mUPPER()


        elif alt2 == 5:
            # atf.g:1:34: LOWER
            pass 
            self.mLOWER()


        elif alt2 == 6:
            # atf.g:1:40: SPACE
            pass 
            self.mSPACE()


        elif alt2 == 7:
            # atf.g:1:46: COMMA
            pass 
            self.mCOMMA()


        elif alt2 == 8:
            # atf.g:1:52: EQUAL
            pass 
            self.mEQUAL()


        elif alt2 == 9:
            # atf.g:1:58: OTHER
            pass 
            self.mOTHER()


        elif alt2 == 10:
            # atf.g:1:64: NEWLINE
            pass 
            self.mNEWLINE()







    # lookup tables for DFA #2

    DFA2_eot = DFA.unpack(
        u"\2\uffff\1\14\13\uffff"
        )

    DFA2_eof = DFA.unpack(
        u"\16\uffff"
        )

    DFA2_min = DFA.unpack(
        u"\1\0\1\uffff\1\75\13\uffff"
        )

    DFA2_max = DFA.unpack(
        u"\1\uffff\1\uffff\1\75\13\uffff"
        )

    DFA2_accept = DFA.unpack(
        u"\1\uffff\1\1\1\uffff\1\3\1\4\1\5\1\7\1\10\1\11\1\12\1\1\1\2\1\6"
        u"\1\10"
        )

    DFA2_special = DFA.unpack(
        u"\1\0\15\uffff"
        )

            
    DFA2_transition = [
        DFA.unpack(u"\12\10\1\11\2\10\1\11\22\10\1\2\5\10\1\1\5\10\1\6\3"
        u"\10\12\3\3\10\1\7\3\10\32\4\6\10\32\5\uff85\10"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\13"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"")
    ]

    # class definition for DFA #2

    class DFA2(DFA):
        pass


        def specialStateTransition(self_, s, input):
            # convince pylint that my self_ magic is ok ;)
            # pylint: disable-msg=E0213

            # pretend we are a member of the recognizer
            # thus semantic predicates can be evaluated
            self = self_.recognizer

            _s = s

            if s == 0: 
                LA2_0 = input.LA(1)

                s = -1
                if (LA2_0 == 38):
                    s = 1

                elif (LA2_0 == 32):
                    s = 2

                elif ((48 <= LA2_0 <= 57)):
                    s = 3

                elif ((65 <= LA2_0 <= 90)):
                    s = 4

                elif ((97 <= LA2_0 <= 122)):
                    s = 5

                elif (LA2_0 == 44):
                    s = 6

                elif (LA2_0 == 61):
                    s = 7

                elif ((0 <= LA2_0 <= 9) or (11 <= LA2_0 <= 12) or (14 <= LA2_0 <= 31) or (33 <= LA2_0 <= 37) or (39 <= LA2_0 <= 43) or (45 <= LA2_0 <= 47) or (58 <= LA2_0 <= 60) or (62 <= LA2_0 <= 64) or (91 <= LA2_0 <= 96) or (123 <= LA2_0 <= 65535)):
                    s = 8

                elif (LA2_0 == 10 or LA2_0 == 13):
                    s = 9

                if s >= 0:
                    return s

            nvae = NoViableAltException(self_.getDescription(), 2, _s, input)
            self_.error(nvae)
            raise nvae
 



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import LexerMain
    main = LexerMain(atfLexer)
    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)


if __name__ == '__main__':
    main(sys.argv)
