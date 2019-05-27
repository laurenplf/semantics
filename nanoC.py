from sly import Lexer, Parser
import sys

class NanoCLexer(Lexer):

    tokens = { OPBIN, ID, WHILE, MAIN, IF, NOMBRE, LBRACE, RBRACE, LPAREN, RPAREN,
               SEMICOLON, COMMA, EQUAL, LT }
    #On veut aussi ajouter les signes suivants : ( ) { } ; , = <

    ignore = ' \t\n'

    OPBIN = r'[\+-]'
    WHILE = r'while'
    IF = r'if'
    MAIN = r'main'
    NOMBRE = r'[0-9]+'
    LBRACE = r'\{'
    RBRACE = r'\}'
    LPAREN = r'\('
    RPAREN = r'\)'
    SEMICOLON = r'\;'
    COMMA = r'\,'
    EQUAL = r'\='
    LT = r'\<'


    @_(r'[a-z]+')
    def ID(self, t):
        return t

    def error(self, t):
        print("error at %s" % t)
        sys.exit(1)


programme = '''x, z'''
lexer = NanoCLexer()
toks = lexer.tokenize(programme)

class NanoCParser(Parser):

    tokens = lexer.tokens

    @_('ID')
    def varlist(self, p):
        return (p[0],)

    @_('ID COMMA varlist')
    def varlist(self, p):from sly import Lexer, Parser
import sys

class NanoCLexer(Lexer):

    tokens = { OPBIN, ID, WHILE, MAIN, IF, NOMBRE, LBRACE, RBRACE, LPAREN, RPAREN,
               SEMICOLON, COMMA, EQUAL, LT }
    #On veut aussi ajouter les signes suivants : ( ) { } ; , = <

    ignore = ' \t\n'

    OPBIN = r'[\+-]'
    WHILE = r'while'
    IF = r'if'
    MAIN = r'main'
    NOMBRE = r'[0-9]+'
    LBRACE = r'\{'
    RBRACE = r'\}'
    LPAREN = r'\('
    RPAREN = r'\)'
    SEMICOLON = r'\;'
    COMMA = r'\,'
    EQUAL = r'\='
    LT = r'\<'


    @_(r'[a-z]+')
    def ID(self, t):
        return t

    def error(self, t):
        print("error at %s" % t)
        sys.exit(1)


programme = '''a = 1'''
lexer = NanoCLexer()
toks = lexer.tokenize(programme)

class NanoCParser(Parser):

    tokens = lexer.tokens
    #start = 'varlist'
    @_('instr SEMICOLON instr')
    def instr(self, p):
        return p
    
    @_('WHILE expr LBRACE instr RBRACE')
    def instr(self, p):
        return p
    
    @_('ID EQUAL expr')
    def instr(self, p):
        return p 
    
    @_('IF expr LBRACE instr RBRACE')
    def instr(self, p):
        return p 
    
    
    @_('ID')
    def varlist(self, p):
        return (p[0],)

    @_('ID COMMA varlist')
    def varlist(self, p):
        return (p[0],) + p[2]

    @_('expr OPBIN expr')
    def expr(self, p):
        return p

    @_('NOMBRE')
    def expr(self, p):
        return p

    @_('ID')
    def expr(self, p):
        return p
     
    


parser = NanoCParser()
for t in lexer.tokenize(programme):
    print(t)
    
x = parser.parse(lexer.tokenize(programme))
print("x = %s" % str(x))
        return (p[0],) + p[2]

    @_('expr OPBIN expr')
    def expr(self, p):
        return p

    @_('NOMBRE')
    def expr(self, p):
        return p

    @_('ID')
    def expr(self, p):
        return p


parser = NanoCParser()
x = parser.parse(lexer.tokenize(programme))
print("x = %s" % str(x))
