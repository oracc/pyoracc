from .atflex import AtfLexer
from .atfyacc import AtfParser
from mako.template import Template


class AtfFile(object):

    template = Template("${text.serialize()}")

    def __init__(self, content):
        self.content = content
        if content[-1] != '\n':
            content += "\n"
        lexer = AtfLexer().lexer
        parser = AtfParser().parser
        self.text = parser.parse(content, lexer=lexer)

    def __str__(self):
        return AtfFile.template.render_unicode(**vars(self))

    def serialize(self):
        return AtfFile.template.render_unicode(**vars(self))


def _debug_lex_and_yac_file(file, debug=0):
    import codecs
    text = codecs.open(file, encoding='utf-8-sig').read()
    from pyoracc.atf.atffile import AtfLexer
    lexer = AtfLexer(debug=debug).lexer
    lexer.input(text)
    for tok in lexer:
        print(tok)
    print("Lexed file")
    lexer = AtfLexer().lexer
    parser = AtfParser().parser
    parser.parse(text, lexer=lexer)
    print("Parsed file")
