from sly import Lexer
import sys

class NanoCLexer(Lexer):

    tokens = { PLUS, MOINS, ID }

    ignore = ' \t\n'

    ID = r'[a-z]+'
    PLUS = r'\+'
    MOINS = r'-'

    def error(self, t):
        print("error at %s" % t)
        sys.exit(1)


lexer = NanoCLexer()
toks = lexer.tokenize('''qsjd ++
12-
qsdkh''')
for tok in toks:
    print(tok)