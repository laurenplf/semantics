from sly import Lexer, Parser
import sys

def declarations(vars):
    decls = ['%s:\tdq 0' % v for v in vars]
    return "\n".join(decls)
    
class NanoCLexer(Lexer):

    tokens = { OPBIN, ID, WHILE, MAIN, IF, NUMBER, LBRACE, RBRACE, LPAREN, RPAREN,
               SEMICOLON, COMMA, EQUAL, LTE, LT, GTE, GT, STRUCT, INT, DOT, RETURN }

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
    
    DOT = r'\.'
    STRUCT = r'struct'
    INT = r'int'

    @_(r'[a-z_]+')
    def ID(self, t):
        return t


    def error(self, t):
        print("error at %s" % t)
        sys.exit(1)



#programme = '''struct{int a;}s;main(a,b,c){a = c; while(a < 1){a = a + 1;b = b - 1;} return a;}'''
#programme = '''struct{int a;struct point p;}s;struct{int x; int y;}point;main(a,b,c){a = c; return a;}'''
#programme = '''struct{int x; int y;}point;main(a,b,c){point_a.x = point_b.y; a = 3; return a;}'''
programme = '''struct{int a;struct point point_p;int b}s;struct{int x; int y;}point;main(a,b,c){s_test.point_p.x = 5; a = 3; return a;}'''
print(programme+"\n")

lexer = NanoCLexer()
toks = lexer.tokenize(programme)

class NanoCParser(Parser):

    tokens = lexer.tokens


    #start = 'varlist'   
    
    @_('MAIN LPAREN varlist RPAREN LBRACE instr RETURN expr SEMICOLON RBRACE')
    def prog(self, p):
        return 'prog', ('defs',()),('main', p[2], p[5], p[7])
    
    @_('struct MAIN LPAREN varlist RPAREN LBRACE instr RETURN expr SEMICOLON RBRACE')
    def prog(self, p):
        return 'prog', ('defs',p[0]),('main', p[3], p[6], p[8])
    
    @_('STRUCT LBRACE attr RBRACE ID SEMICOLON')
    def struct(self, p):
        return ('struct',p[2],p[4])
    
    @_('STRUCT LBRACE attr RBRACE ID SEMICOLON struct')
    def struct(self, p):
        return ('struct',p[2],p[4]) + p[6]
    
    @_('INT ID SEMICOLON')
    def attr(self, p):
        return ('int',p[1])
    
    @_('STRUCT ID ID SEMICOLON')
    def attr(self, p):
        return ('struct', p[1], p[2])

    @_('INT ID SEMICOLON attr')
    def attr(self, p):
        return ('int', p[1]) + p[3]
    
    @_('STRUCT ID ID SEMICOLON attr')
    def attr(self, p):
        return ('struct', p[1],p[2]) + p[4]


    
    
    @_('instr instr')
    def instr(self, p):
        return 'seq', p[0], p[1]
    
    @_('WHILE LPAREN expr RPAREN LBRACE instr RBRACE')
    def instr(self, p):
        return 'while', p[2], p[5]
    
#    @_('ID EQUAL expr SEMICOLON')
#    def instr(self, p):
#        return 'affect', ('var', p[0]), p[2]    
    
#    @_('lhs EQUAL expr SEMICOLON')
#    def instr(self, p):
#        return 'affect', p[0], p[2]
    
    @_('lhs EQUAL rhs SEMICOLON')
    def instr(self, p):
        return 'affect', p[0], p[2]    
    
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
        return 'opbin', p[0], 'lte', p[2]

    @_('expr LT expr')
    def expr(self, p):
        return 'opbin', p[0], 'lt', p[2]

    @_('expr GTE expr')
    def expr(self, p):
        return 'opbin', p[0], 'gte', p[2]

    @_('expr GT expr')
    def expr(self, p):
        return 'opbin', p[0], 'gt', p[2]

    @_('expr OPBIN expr')
    def expr(self, p):
        return 'opbin', p[0], p[1], p[2]

    @_('NUMBER')
    def expr(self, p):
        return 'nb', p[0]

#    @_('ID')
#   def expr(self, p):
#        return 'var', p[0]
    @_('ID')
    def expr(self, p):
        if "_" in p[0]:
            for i in range(len(p[0])):
                if p[0][i] == "_":
                    indice = i
            return 'struct', p[0][:indice],p[0][indice+1:]
        else:
            return 'var',p[0]


    @_('lhs DOT lhs')
    def lhs(self, p):
        return p[0], p[2]    
    
    @_('expr')
    def lhs(self, p):
        return p[0]
    
    @_('rhs DOT rhs')
    def rhs(self, p):
        return p[0], p[2]

    @_('expr')
    def rhs(self, p):
        return p[0]
    

    @_('ID')
    def varlist(self, p):
        return ('var', p[0])

    @_('ID COMMA varlist')
    def varlist(self, p):
        return ('var', p[0]) + p[2]




parser = NanoCParser()
#for t in lexer.tokenize(programme):
    #print(t)
    
x = parser.parse(lexer.tokenize(programme))
print("x = %s \n" % str(x))
print(x[1][1])
print("\n")

def create_dict_struct(s):
    d = {}
    for i in range(len(s)):
        if s[i] == 'struct':
            d[s[i+2]] = s[i+1]
    return d

d_struct = create_dict_struct(x[1][1])
#global d_struct

# par exemple, s = ('int', 'x', 'int', 'y')
"""
def taille_struct(s):
    l = d_struct[s]
    cpt = 0
    i = 0
    while i < len(l):
        if l[i] == 'int':
            cpt += 8
            i += 2
        elif l[i] == 'struct':
            cpt += taille_struct(l[i+1])
            i += 3
    return cpt
"""

def position(s, b):
    l = d_struct[s]
    cpt = 0
    i = 0
    while i < len(l):
        if l[i] == 'int':
            if l[i+1] == b:
                return cpt
            else:
                cpt += 8
                i += 2
        elif l[i] == 'struct':
            if l[i+2] == b:
                return cpt
            else:
                #cpt += taille_struct(l[i+1])
                cpt += position(l[i+1], b)
                i += 3
    return cpt
            
print(position('point', 'x'))

#s = "abcd"
#for (indice,k1) in enumerate(s):
#    print(indice,k1)


def p_vars(prg):
    vars = set([x[1] for x in prg[1]])
    #print(vars)
    vars |= i_vars(prg[2]) # |= = union dans un set
    vars |= {prg[3][1]}
    return vars

def e_vars(expr):
    if expr[0] == 'var':
        return { expr[1] }
    if expr[0] == 'nb':
        return set()
    if expr[0] == 'opbin':
        return e_vars(expr[1])|e_vars(expr[3])
    else:
        #print(expr)
        return set()

def i_vars(instr):
    #print(instr)
    i = instr[0]
    vars = set()
    if i == 'while' or i == 'if':
        vars |= e_vars(instr[1])
        vars |= i_vars(instr[2])
    elif i == 'seq':
        vars |= i_vars(instr[1])
        vars |= i_vars(instr[2])
    elif i == 'affect':
        vars |= {instr[1][1]}
        vars |= e_vars(instr[2])
    return vars
     
      
#print(p_vars(x))
    
global cpt_cmp
global cptinstr
cptinstr = 0
cpt_cmp = 0
i_test = {"lt":"jl", "lte":"jle", "gt":"jg", "gte":"jge"}

def e_asm(expr):
    global cpt_cmp
    if expr[0] == 'nb':
        return ["mov rax, " + expr[1]]
    elif expr[0] == 'var':
        return ["mov rax, [" + expr[1] + "]"]
    elif expr[0] == 'opbin':
        
        e_fin = "fin_cmp_%s" % cpt_cmp
        e_saut = "cmp_%s" % cpt_cmp
        cpt_cmp += 1
        
        res = e_asm(expr[3])
        res.append("push rax")
        res += e_asm(expr[1])
        res.append("pop rbx")
        
        if expr[2] == '+':
            res.append("add rax, rbx")
        elif expr[2] == '-':
            res.append("sub rax, rbx")    
        else:
            res.append("cmp rax, rbx")
            res.append(i_test[expr[2]] + " "+ e_saut)
            res.append("mov rax, 0")
            res.append("jmp %s" % e_fin)
            res.append("%s: mov rax, 1" % e_saut)
            res.append("%s:" % e_fin)
        return res
 
def i_asm(instr):
    global cptinstr
    i = instr[0]
    st = []
    if i == "affect": # var = instr[1][1], expr = instr[2]
        st += e_asm(instr[2]) 
        st.append("mov [" + str(instr[1][1]) + "], rax")
    elif i == 'seq':
        st += i_asm(instr[1])
        st += i_asm(instr[2])
    elif i == 'if':
        st += e_asm(instr[1])
        st.append("cmp rax, 0")
        st.append("jz jzfin" + str(cptinstr))
        st += i_asm(instr[2])
        st.append("jzfin" +str(cptinstr)+":")
        cptinstr += 1
    elif i == 'while':
        st.append("debut"+str(cptinstr)+ ":")
        st += e_asm(instr[1])
        st.append("cmp rax, 0")
        st.append("jz jzfin" + str(cptinstr))
        st += i_asm(instr[2])
        st.append("jmp debut" + str(cptinstr))
        st.append("jzfin" +str(cptinstr)+":")        
        cptinstr += 1   
    return st 


def p_asm(prg):
    code = open("moule.asm").read()
    code = code.replace("[DECLS_VARS]", declarations(p_vars(prg)))
    code = code.replace("[CODE]", "\n".join( i_asm(prg[2])))
    ret = e_asm(prg[3])
    ret += ["mov rdi, nombre", "mov rsi, rax", "call printf"]
    code = code.replace("[RETURN]", "\n".join(ret))
    init_vars = ""
    N = len(prg[1])
    for i in range(N):
        iv = ["mov rax, [argv]", "mov rbx, [rax+DELTA]", "mov rdi, rbx", "call atoi", "mov [VAR], rax"]
        iv[1] = iv[1].replace("DELTA", str((i+1)*8))
        iv[4] = iv[4].replace("VAR", prg[1][i][1])
        init_vars += "\n"+ "\n".join(iv)
    code = code.replace("[INIT_VARS]", init_vars)
    return code

#print(p_asm(x))
        
    
    
     
     

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
