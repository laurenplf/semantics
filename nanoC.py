from sly import Lexer, Parser
import sys

def declarations(vars):
    decls = ['%s:\tdq 0' % v for v in vars]
    return "\n".join(decls)
    
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



programme = '''
inc(a){
    if(a < 10){
        b = inc(a + 1);
    }
    if(a >= 10){
        b = 10;
    }
    return b;
}

f(d, e){
    d = d + 1;
    e = e + d;
    h = g(d, e);
    return h;
}

g(h, i){
    i = i + h;
    return i;
}

main(a, b, c){
    c = a + c;
    a = g(inc(a + c), d);
    d = f(c + a, d);
    d = inc(f(d, a));
    return d;
}
'''

lexer = NanoCLexer()
toks = lexer.tokenize(programme)

class NanoCParser(Parser):

    tokens = lexer.tokens


    #start = 'varlist'

    @_('function_def main')
    def prog(self, p):
        return 'prog', (p[0],), p[1]

    @_('functionlist main')
    def prog(self, p):
        return 'prog', p[0], p[1]
    
    @_('MAIN LPAREN varlist RPAREN LBRACE instr RETURN expr SEMICOLON RBRACE')
    def main(self, p):
        return 'main', p[2], p[5], p[7]

    @_('function LPAREN varlist RPAREN LBRACE instr RETURN expr SEMICOLON RBRACE')
    def function_def(self, p):
        return 'function def', p[0], p[2], p[5], p[7]

    @_('function_def function_def')
    def functionlist(self, p):
        return p[0], p[1]

    @_('function_def functionlist')
    def functionlist(self, p):
        return (p[0],) + p[1]

    @_('instr instr')
    def instr(self, p):
        return 'seq', p[0], p[1]
    
    @_('WHILE LPAREN expr RPAREN LBRACE instr RBRACE')
    def instr(self, p):
        return 'while', p[2], p[5]
    
    @_('ID EQUAL expr SEMICOLON')
    def instr(self, p):
        return 'affect', ('var', p[0]), p[2]
    
    @_('IF LPAREN expr RPAREN LBRACE instr RBRACE')
    def instr(self, p):
        return 'if', p[2], p[5]

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

    @_('ID')
    def exprlist(self, p):
        return ('var', p[0]),

    @_('ID COMMA exprlist')
    def exprlist(self, p):
        return (('var', p[0]),) + p[2]

    @_('expr COMMA exprlist')
    def exprlist(self, p):
        return (p[0],) + p[2]

    @_('expr')
    def exprlist(self, p):
        return p[0]

    @_('NUMBER')
    def expr(self, p):
        return 'nb', p[0]

    @_('ID')
    def expr(self, p):
        return 'var', p[0]

    @_('ID')
    def function(self, p):
        return 'function', p[0]

    @_('ID')
    def varlist(self, p):
        return ('var', p[0]),

    @_('ID COMMA varlist')
    def varlist(self, p):
        return (('var', p[0]),) + p[2]

    @_('function LPAREN exprlist RPAREN')
    def expr(self, p):
        return 'function call', p[0], p[2]

    @_('function LPAREN expr RPAREN')
    def expr(self, p):
        return 'function call', p[0], (p[2],)



parser = NanoCParser()
#for t in lexer.tokenize(programme):
    #print(t)
    
x = parser.parse(lexer.tokenize(programme))
print("x = %s\n" % str(x))
for elem in x:
    print(elem)
print("\n")



def fun_args(function_def):
    """
    Prend en arg un tuple dont le premier élément est 'function def'
    Renvoie la liste des arguments de la fonction
    """
    if len(function_def[2]) == 1:
        return [function_def[2][0][1]]
    return [elem[1] for elem in function_def[2]]

def fun_vars(function_def):
    """
    Prend en arg un tuple dont le premier élément est 'function def'
    Renvoie l'ensemble des variables (autres que les arguments) utilisées dans la fonction
    """
    args = set(fun_args(function_def))
    vars = i_vars(function_def[3])
    vars |= {function_def[4][1]}
    vars_copy = vars.copy()
    for elem in vars_copy:
        if elem in args:
            vars.remove(elem)
    return vars

def p_vars(prg):
    """
    Prend en arg un tuple dont le premier élément est 'prog'
    Renvoie l'ensemble des variables utilisées dans le main
    """
    vars = set([x[1] for x in prg[2][1]])
    #print(vars)
    vars |= i_vars(prg[2][2]) # |= = union dans un set
    vars |= {prg[2][3][1]}
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

def delta(function_def):
    """
    Prend en arg un tuple dont le premier élément est 'function def'
    Renvoie un dictionnaire associant à chaque variable (argument ou variable déclarée dans la fonction) son
    décalage d'adresse par rapport à rbp (en 64 bits)
    """
    args = fun_args(function_def)
    vars = fun_vars(function_def)
    result = {}
    for i in range(len(args)):
        result[args[i]] = "+" + str(8*(i+2)) #le premier décalage est de 16 octets
    cpt = 1
    for elem in vars:
        result[elem] = str(-8*cpt) #le premier décalage est de -8 octets
        cpt += 1
    return result
      
print("main : all vars = %s\n" %str(p_vars(x)))
print("f : args = %s\n" %str(fun_args(x[1][0])))
print("f : vars = %s\n" %str(fun_vars(x[1][0])))
print("f : delta = %s\n" %str(delta(x[1][0])))
    
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
    elif expr[0] == 'function call':
        res = []
        for i in range(len(expr[2])):
            res += e_asm(expr[2][-(i+1)])
            res.append("push rax")
        res.append("call %s" %expr[1][1])
        temp = ["pop rcx" for i in range(len(expr[2]))]
        res += temp
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
    code = code.replace("[FUN_DECL]", "\n".join(fun_asm(prg)))
    code = code.replace("[DECLS_VARS]", declarations(p_vars(prg)))
    code = code.replace("[CODE]", "\n".join(i_asm(prg[2][2])))
    ret = e_asm(prg[2][3])
    ret += ["mov rdi, nombre", "mov rsi, rax", "xor rax, rax", "call printf"]
    code = code.replace("[RETURN]", "\n".join(ret))
    init_vars = ""
    N = len(prg[2][1]) #nombre d'arguments
    for i in range(N):
        iv = ["mov rax, [argv]", "mov rbx, [rax+DELTA]", "mov rdi, rbx", "call atoi", "mov [VAR], rax"]
        iv[1] = iv[1].replace("DELTA", str((i+1)*8))
        iv[4] = iv[4].replace("VAR", prg[2][1][i][1])
        init_vars += "\n"+ "\n".join(iv)
    code = code.replace("[INIT_VARS]", init_vars)
    return code


def e_asm_fun(expr, delta_function):
    global cpt_cmp
    if expr[0] == 'nb':
        return ["mov rax, " + expr[1]]
    elif expr[0] == 'var':
        return ["mov rax, [rbp " + str(delta_function[expr[1]]) + "]"]
    elif expr[0] == 'opbin':

        e_fin = "fin_cmp_%s" % cpt_cmp
        e_saut = "cmp_%s" % cpt_cmp
        cpt_cmp += 1

        res = e_asm_fun(expr[3], delta_function)
        res.append("push rax")
        res += e_asm_fun(expr[1], delta_function)
        res.append("pop rbx")

        if expr[2] == '+':
            res.append("add rax, rbx")
        elif expr[2] == '-':
            res.append("sub rax, rbx")
        else:
            res.append("cmp rax, rbx")
            res.append(i_test[expr[2]] + " " + e_saut)
            res.append("mov rax, 0")
            res.append("jmp %s" % e_fin)
            res.append("%s: mov rax, 1" % e_saut)
            res.append("%s:" % e_fin)
        return res
    elif expr[0] == 'function call':
        res = []
        for i in range(len(expr[2])):
            print(expr[2])
            res += e_asm_fun(expr[2][-(i+1)], delta_function)
            res.append("push rax")
        res.append("call %s" %expr[1][1])
        temp = ["pop rcx" for i in range(len(expr[2]))]
        res += temp
        return res


def i_asm_fun(instr, delta_function):
    global cptinstr
    i = instr[0]
    st = []
    if i == "affect":  # var = instr[1][1], expr = instr[2]
        st += e_asm_fun(instr[2], delta_function)
        st.append("mov [rbp " + str(delta_function[instr[1][1]]) + "], rax")
    elif i == 'seq':
        st += i_asm_fun(instr[1], delta_function)
        st += i_asm_fun(instr[2], delta_function)
    elif i == 'if':
        st += e_asm_fun(instr[1], delta_function)
        st.append("cmp rax, 0")
        st.append("jz jzfin" + str(cptinstr))
        st += i_asm_fun(instr[2], delta_function)
        st.append("jzfin" + str(cptinstr) + ":")
        cptinstr += 1
    elif i == 'while':
        st.append("debut" + str(cptinstr) + ":")
        st += e_asm_fun(instr[1], delta_function)
        st.append("cmp rax, 0")
        st.append("jz jzfin" + str(cptinstr))
        st += i_asm_fun(instr[2], delta_function)
        st.append("jmp debut" + str(cptinstr))
        st.append("jzfin" + str(cptinstr) + ":")
        cptinstr += 1
    return st

def fun_asm(prg):
    fun_decl_asm = []
    for fun_def in prg[1]:
        delta_fun = delta(fun_def)
        fun_decl_asm.append(fun_def[1][1] + ": push rbp")
        fun_decl_asm.append("mov rbp, rsp")
        nb_var_loc = len(fun_vars(fun_def))
        fun_decl_asm.append("sub rsp, " + str(8*nb_var_loc))
        fun_decl_asm += i_asm_fun(fun_def[3], delta_fun)

        fun_decl_asm.append("mov rsp, rbp")
        fun_decl_asm.append("pop rbp")
        fun_decl_asm.append("ret")

    return fun_decl_asm
print("ici")
print(x[1][0][2][0][1])
print(fun_asm(x))
print(p_asm(x))
        
    
    
     
     

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
