# $ANTLR 3.1.3 Mar 18, 2009 10:09:25 atf.g 2014-05-14 16:39:11

import sys
from antlr3 import *
from antlr3.compat import set, frozenset
         
from ...artifact import Artifact



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

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>", 
    "NEWLINE", "DIGIT", "UPPER", "LOWER", "SPACE", "COMMA", "OTHER", "EQUAL", 
    "'&'", "' = '"
]




class atfParser(Parser):
    grammarFileName = "atf.g"
    antlr_version = version_str_to_tuple("3.1.3 Mar 18, 2009 10:09:25")
    antlr_version_str = "3.1.3 Mar 18, 2009 10:09:25"
    tokenNames = tokenNames

    def __init__(self, input, state=None, *args, **kwargs):
        if state is None:
            state = RecognizerSharedState()

        super(atfParser, self).__init__(input, state, *args, **kwargs)



               
        self.artifact=Artifact()




                


        



    # $ANTLR start "startRule"
    # atf.g:16:1: startRule : codeline rest ;
    def startRule(self, ):

        try:
            try:
                # atf.g:17:5: ( codeline rest )
                # atf.g:17:9: codeline rest
                pass 
                self._state.following.append(self.FOLLOW_codeline_in_startRule40)
                self.codeline()

                self._state.following.pop()
                self._state.following.append(self.FOLLOW_rest_in_startRule46)
                self.rest()

                self._state.following.pop()




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return 

    # $ANTLR end "startRule"


    # $ANTLR start "codeline"
    # atf.g:21:1: codeline : '&' code= object_code ' = ' description= object_description NEWLINE ;
    def codeline(self, ):

        code = None

        description = None


        try:
            try:
                # atf.g:22:5: ( '&' code= object_code ' = ' description= object_description NEWLINE )
                # atf.g:22:9: '&' code= object_code ' = ' description= object_description NEWLINE
                pass 
                self.match(self.input, 12, self.FOLLOW_12_in_codeline65)
                self._state.following.append(self.FOLLOW_object_code_in_codeline69)
                code = self.object_code()

                self._state.following.pop()
                self.match(self.input, 13, self.FOLLOW_13_in_codeline71)
                self._state.following.append(self.FOLLOW_object_description_in_codeline75)
                description = self.object_description()

                self._state.following.pop()
                self.match(self.input, NEWLINE, self.FOLLOW_NEWLINE_in_codeline77)
                #action start
                     
                self.artifact.code=((code is not None) and [self.input.toString(code.start,code.stop)] or [None])[0]
                self.artifact.description=((description is not None) and [self.input.toString(description.start,description.stop)] or [None])[0]
                				
                #action end




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return 

    # $ANTLR end "codeline"


    # $ANTLR start "rest"
    # atf.g:29:1: rest : ( DIGIT | UPPER | LOWER | SPACE | COMMA | OTHER )+ ;
    def rest(self, ):

        try:
            try:
                # atf.g:30:3: ( ( DIGIT | UPPER | LOWER | SPACE | COMMA | OTHER )+ )
                # atf.g:30:6: ( DIGIT | UPPER | LOWER | SPACE | COMMA | OTHER )+
                pass 
                # atf.g:30:6: ( DIGIT | UPPER | LOWER | SPACE | COMMA | OTHER )+
                cnt1 = 0
                while True: #loop1
                    alt1 = 2
                    LA1_0 = self.input.LA(1)

                    if ((DIGIT <= LA1_0 <= OTHER)) :
                        alt1 = 1


                    if alt1 == 1:
                        # atf.g:
                        pass 
                        if (DIGIT <= self.input.LA(1) <= OTHER):
                            self.input.consume()
                            self._state.errorRecovery = False

                        else:
                            mse = MismatchedSetException(None, self.input)
                            raise mse




                    else:
                        if cnt1 >= 1:
                            break #loop1

                        eee = EarlyExitException(1, self.input)
                        raise eee

                    cnt1 += 1




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return 

    # $ANTLR end "rest"

    class object_code_return(ParserRuleReturnScope):
        def __init__(self):
            super(atfParser.object_code_return, self).__init__()





    # $ANTLR start "object_code"
    # atf.g:32:1: object_code : UPPER ( DIGIT )+ ;
    def object_code(self, ):

        retval = self.object_code_return()
        retval.start = self.input.LT(1)

        try:
            try:
                # atf.g:32:12: ( UPPER ( DIGIT )+ )
                # atf.g:32:14: UPPER ( DIGIT )+
                pass 
                self.match(self.input, UPPER, self.FOLLOW_UPPER_in_object_code119)
                # atf.g:32:20: ( DIGIT )+
                cnt2 = 0
                while True: #loop2
                    alt2 = 2
                    LA2_0 = self.input.LA(1)

                    if (LA2_0 == DIGIT) :
                        alt2 = 1


                    if alt2 == 1:
                        # atf.g:32:20: DIGIT
                        pass 
                        self.match(self.input, DIGIT, self.FOLLOW_DIGIT_in_object_code121)


                    else:
                        if cnt2 >= 1:
                            break #loop2

                        eee = EarlyExitException(2, self.input)
                        raise eee

                    cnt2 += 1



                retval.stop = self.input.LT(-1)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return retval

    # $ANTLR end "object_code"

    class object_description_return(ParserRuleReturnScope):
        def __init__(self):
            super(atfParser.object_description_return, self).__init__()





    # $ANTLR start "object_description"
    # atf.g:33:1: object_description : ( DIGIT | UPPER | LOWER | SPACE | COMMA )+ ;
    def object_description(self, ):

        retval = self.object_description_return()
        retval.start = self.input.LT(1)

        try:
            try:
                # atf.g:33:19: ( ( DIGIT | UPPER | LOWER | SPACE | COMMA )+ )
                # atf.g:33:21: ( DIGIT | UPPER | LOWER | SPACE | COMMA )+
                pass 
                # atf.g:33:21: ( DIGIT | UPPER | LOWER | SPACE | COMMA )+
                cnt3 = 0
                while True: #loop3
                    alt3 = 2
                    LA3_0 = self.input.LA(1)

                    if ((DIGIT <= LA3_0 <= COMMA)) :
                        alt3 = 1


                    if alt3 == 1:
                        # atf.g:
                        pass 
                        if (DIGIT <= self.input.LA(1) <= COMMA):
                            self.input.consume()
                            self._state.errorRecovery = False

                        else:
                            mse = MismatchedSetException(None, self.input)
                            raise mse




                    else:
                        if cnt3 >= 1:
                            break #loop3

                        eee = EarlyExitException(3, self.input)
                        raise eee

                    cnt3 += 1



                retval.stop = self.input.LT(-1)


            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass
        return retval

    # $ANTLR end "object_description"


    # Delegated rules


 

    FOLLOW_codeline_in_startRule40 = frozenset([5, 6, 7, 8, 9, 10])
    FOLLOW_rest_in_startRule46 = frozenset([1])
    FOLLOW_12_in_codeline65 = frozenset([6])
    FOLLOW_object_code_in_codeline69 = frozenset([13])
    FOLLOW_13_in_codeline71 = frozenset([5, 6, 7, 8, 9])
    FOLLOW_object_description_in_codeline75 = frozenset([4])
    FOLLOW_NEWLINE_in_codeline77 = frozenset([1])
    FOLLOW_set_in_rest99 = frozenset([1, 5, 6, 7, 8, 9, 10])
    FOLLOW_UPPER_in_object_code119 = frozenset([5])
    FOLLOW_DIGIT_in_object_code121 = frozenset([1, 5])
    FOLLOW_set_in_object_description128 = frozenset([1, 5, 6, 7, 8, 9])



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import ParserMain
    main = ParserMain("atfLexer", atfParser)
    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)


if __name__ == '__main__':
    main(sys.argv)
