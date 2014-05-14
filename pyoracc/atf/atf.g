grammar atf;

// Antlr Grammar for ATF
options {
	language=Python;
}

@header {
  from ...artifact import Artifact
}

@init {
	self.artifact=Artifact()
}

startRule
    :   codeline
				rest
    ;

codeline
    :   '&' code=object_code ' = ' description=object_description NEWLINE
				{
				self.artifact.code=$code.text
				self.artifact.description=$description.text
				}
    ;

rest
		:  (DIGIT|UPPER|LOWER|SPACE|COMMA|OTHER)+;

object_code: UPPER DIGIT+;
object_description: (DIGIT|UPPER|LOWER|SPACE|COMMA)+;

// An upper case letter, followed by one or more numbers

DIGIT: '0'..'9';
UPPER: 'A'..'Z';
LOWER: 'a'..'z';
SPACE: ' ';
COMMA: ',';
EQUAL: '=';
OTHER:~(DIGIT|UPPER|LOWER|SPACE|'\r'|'\n'|COMMA);

NEWLINE
    :   '\r' '\n'   // DOS
    |   '\n'        // UNIX
    ;
