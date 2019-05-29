from sly import Lexer, Parser
import sys

class NanoCLexer(Lexer):

    tokens = { OPBIN, ID, WHILE, MAIN, IF, NUMBER, LBRACE, RBRACE, LPAREN, RPAREN,
               SEMICOLON, COMMA, EQUAL, LTE, LT, GTE, GT, RETURN }

    ignore = ' \t\n'

    OPBIN = r'[\+-]'
    WHILE = r'while'
    IF = r'if'
    RETURN = r'return'
    MAIN = r'main'
    NUMBER = r'[0-9]+'
    LBRACE = r'\{'
    RBRACE = r'\}'
    LPAREN = r'\('
    RPAREN = r'\)'
    SEMICOLON = r'\;'
    COMMA = r'\,'
    EQUAL = r'\='
    LTE = r'<='
    LT = r'\<'
    GTE = r'>='
    GT = r'>'


    @_(r'[a-z]+')
    def ID(self, t):
        return t

    def error(self, t):
        print("error at %s" % t)
        sys.exit(1)



programme = '''main(a,b,c){a = c; while(a < 1){a = a + 1;} return a;}'''

lexer = NanoCLexer()
toks = lexer.tokenize(programme)

class NanoCParser(Parser):

    tokens = lexer.tokens


    #start = 'varlist'
    
    @_('MAIN LPAREN varlist RPAREN LBRACE instr RETURN expr SEMICOLON RBRACE')
    def prog(self, p):
        return 'prog', p[2], p[5], p[7]
    
    @_('instr instr')
    def instr(self, p):
        return p[0], p[1]
    
    @_('WHILE LPAREN expr RPAREN LBRACE instr RBRACE')
    def instr(self, p):
        return 'while', p[2], p[5]
    
    @_('ID EQUAL expr SEMICOLON')
    def instr(self, p):
        return 'affect', ('var', p[0]), p[2]
    
    @_('IF LPAREN expr RPAREN LBRACE instr RBRACE')
    def instr(self, p):
        return 'if', p[2], p[5]

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p[1]

    @_('LBRACE expr RBRACE')
    def expr(self, p):
        return p[1]

    @_('expr LTE expr')
    def expr(self, p):
        return 'lte', p[0], p[2]

    @_('expr LT expr')
    def expr(self, p):
        return 'lt', p[0], p[2]

    @_('expr GTE expr')
    def expr(self, p):
        return 'gte', p[0], p[2]

    @_('expr GT expr')
    def expr(self, p):
        return 'gt', p[0], p[2]

    @_('expr OPBIN expr')
    def expr(self, p):
        return 'opbin', p[0], p[1], p[2]

    @_('NUMBER')
    def expr(self, p):
        return 'nb', p[0]

    @_('ID')
    def expr(self, p):
        return 'var', p[0]

    @_('ID')
    def varlist(self, p):
        return ('var', p[0]),

    @_('ID COMMA varlist')
    def varlist(self, p):
        return (('var', p[0]),) + p[2]




parser = NanoCParser()
for t in lexer.tokenize(programme):
    print(t)
    
x = parser.parse(lexer.tokenize(programme))
print("x = %s" % str(x))

def expr_dump(expr):
    if (expr[0] == 'opbin'):
        return "(" + expr_dump(expr[1]) + " " + expr[2] + " " + expr_dump(expr[3]) + ")"
    elif (expr[0] == 'lt'):
        return "(" + expr_dump(expr[1]) + " < " + expr_dump(expr[2]) + ")"
    elif (expr[0] == 'lte'):
        return "(" + expr_dump(expr[1]) + " <= " + expr_dump(expr[2]) + ")"
    elif (expr[0] == 'gt'):
        return "(" + expr_dump(expr[1]) + " > " + expr_dump(expr[2]) + ")"
    elif (expr[0] == 'gte'):
        return "(" + expr_dump(expr[1]) + " >= " + expr_dump(expr[2]) + ")"
    elif (expr[0] == 'var'):
        return expr[1]
    elif (expr[0] == 'nb'):
        return expr[1]
    return 'pb'

#print(expr_dump(x))
