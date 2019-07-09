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



programme = '''main(a,b,c){a = c; while(a < 1){a = a + 1; if(a > 4){b = b - 1;} c= a + 1;} a= a+3; a=b+2; return a;}'''


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
#for t in lexer.tokenize(programme):
    #print(t)

x = parser.parse(lexer.tokenize(programme))
print("x = %s" % str(x))

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
        return  expr_dump(expr[1]) + " " + expr_dump(expr[2]) + " " + expr_dump(expr[3])
    elif (expr == 'lt'):
        return "<"
    elif (expr == 'lte'):
        return "<="
    elif (expr == 'gt'):
        return ">"
    elif (expr == 'gte'):
        return ">="
    elif (expr == '+'):
        return '+'
    elif (expr == '-'):
        return '-'
    elif (expr[0] == 'var'):
        return expr[1]
    elif (expr[0] == 'nb'):
        return expr[1]
    return str(expr)

#print(expr_dump(x))
    

opbinDic = {'+':0, '-':1, 'lte':2, 'lt':3, 'gte':4, 'gt':5}

def hachage(varDic, instr):
    """Fonction de hachage pour repérer deux opérations identiques"""
    a = varDic[instr[1][1]]
    b = varDic[instr[3][1]]
    return opbin[instr[2]] + 10*min(a,b) + 1000*max(a,b)
    
 

def optiLocal(instr):
    """Optimisation des blocs de base"""
    varDic = {'indice':0}
    tableHachage = dict()
    addInstr(instr, varDic, tableHachage)           
    return instr

def addInstr(instr, varDic, tableHachage):
    """Ajoute une instruction à la table de hachage :
        - Ajoute les nouvelles variables éventuelles dans varDic
        - Ajoute les opérations à la table de hachage """
    
    if instr[0] == 'affect':        
        addVar(instr[1], varDic)
        if instr[2][0] == 'opbin':
            addOpbin(instr, varDic, tableHachage)
        elif instr[2][0] == 'var':
            addVar(instr[2], varDic)
            varDic[instr[2][1]] = instr[1][1]
            delOpbin(instr, varDic, tableHachage)
            
    elif instr[0] == 'seq':
        addInstr(instr[1], varDic, tableHachage)
        addInstr(instr[2], varDic, tableHachage)
    return

def addVar(var, varDic):
    """Ajout des variables indicées"""
    if not var[1] in varDic:
        varDic['indice'] += 1
        varDic[var[1]] = varDic['indice']
    return
    
def addOpbin(instr, varDic, tableHachage):
    """Ajout des opérations dans la table de hachage"""
    indice = hachage(varDic, instr[2])
    if not indice in tableHachage :
        tableHachage[indice] = [instr]
    else : 
        instr[2] = tableHachage[indice][0][1]
        tableHachage[indice].append(instr)
    return

def delOpbin(instr, varDic, tableHachage):
    return
    
global bloc

def codeToCFG(parser):
    """Transforme le programme en Control Flow Graph"""
    global bloc
    bloc = 0
    graph = [[[],[]]]
    graph[0][0] = parser[1]
    findLoop(parser[2], graph) 
    graph.append([[parser[3]],[]])
    return graph

def findLoop(instr, graph):
    """Retourne le graph complété par l'instruction instr
    Ajoute les boucles existantes en indentant le numéro de bloc"""
    global bloc
    currentBloc = bloc
    if instr[0] == 'seq' :
        findLoop(instr[1], graph)
        findLoop(instr[2], graph)
    elif instr[0] == 'affect' :
        bloc += 1
        graph.append([[instr],[bloc+1]])
    elif instr[0] == 'if' :
        bloc += 1
        graph.append([[instr[0],instr[1]],[bloc+1]])
        findLoop(instr[2], graph)
        graph[currentBloc+1][1].append(bloc+1)
    elif instr[0] == 'while':
        bloc += 1
        graph.append([[instr[0],instr[1]],[bloc+1]])
        findLoop(instr[2], graph)
        graph[bloc][1] = [currentBloc+1]
        graph[currentBloc+1][1].append(bloc+1)
    return graph

graph = codeToCFG(x)
print("\n")
print(programme)
for i in graph :
    print("\n")
    print(i)


        


def CFGtoCode(graph):
    """Retourne les instructions correspondant au Control Flow Graph"""
    programme = "main("
    global bloc
    global M
    M =[]
    bloc = 1
    n = len(graph[0][0])-1
    for i in range(n):
        programme += expr_dump(graph[0][0][i]) +","
    programme += expr_dump(graph[0][0][n]) +"){"
    while bloc < len(graph)-1:
        programme += transfInstr(graph, graph[bloc][0])
        bloc += 1
    programme += "return " + expr_dump(graph[len(graph)-1][0][0]) +";}"
    return programme

def transfInstr(graph, instrL):
    """Retourne la chaine de caractère associé à liste d'instruction"""
    programme = ""
    global bloc
    if instrL[0] == 'while' or instrL[0] == 'if':
        programme += instrL[0] + "(" + expr_dump(instrL[1]) + "){"
        M.append(graph[bloc][1][1]-1)
        bloc += 1
        return programme + transfInstr(graph, graph[bloc][0])
    else :  
        programme += instr_dump(instrL[0])
    if (bloc in M):
        return programme +"}"           
    return programme
    
def instr_dump(instr):
    """Retourne la chaine de caractère d'une instruction"""
    return expr_dump(instr[1]) + " = " + expr_dump(instr[2]) + "; "

print("\n")
print(CFGtoCode(graph))
        


# AVAILin(b) = ensemble des expressions disponibles en entrée de b
# KILL(b) = ensemble des variables tuées/définies par b
# NKILL(b) = ensemble des expressions de AVAILin(b) non tuées par b, calculé à partir de AVAILin(b) et KILL(b)
# GEN(b) = ensemble des expressions définies par b et non tuées dans b après leur définition
# AVAILout(b) = ensemble des expressions disponibles en sortie de b qui vaut NKILL(b) U GEN(b)



def calculGeneralForward(graph):
    """"Calcul des ensembles définies précédemment pour tous les blocs du haut en bas"""
    n = len(graph)
    DEF = [[] for i in range(n)]
    KILLED = [[] for i in range(n)]
    NKILL = [[] for i in range(n)]
    AVAILin = [[] for i in range(n)]
    AVAILout = [[] for i in range(n)]
    AVAILout[0] = graph[0][0]
    for bloc in range(1,n):
        AVAILin[bloc] = list(AVAILout[bloc-1])
        for i in range(bloc):
            if bloc in graph[i][1]:
                AVAILin[bloc] = list(set(AVAILin[bloc] + AVAILout[i]))
        
        DEF[bloc], KILLED[bloc], NKILL[bloc] = calculGenKilledNKilled(graph, bloc,AVAILin[bloc])
        AVAILout[bloc] = list(set(DEF[bloc] + NKILL[bloc]))
    return DEF, KILLED, NKILL, AVAILin, AVAILout
        
def calculGenKilledNKilled(graph, bloc,AVAILin):
    """Calcul des ensembles définies précédemment pour un bloc"""
    DEF = []
    KILLED =[]
    n = len(graph[bloc][0])
    i = n-1
    instrL = graph[bloc][0]
    if len(graph[bloc][1]) == 2:
        i = i-2
    while i >= 0 :
        if estOpbin(instrL[i][2]):
            y, z = instrL[i][2][1], instrL[i][2][3]
            if (not y in KILLED) and (not z in KILLED):
                DEF.append(instrL[i][2])
        else :
            if not instrL[i][2] in KILLED:
                DEF.append(instrL[i][2])
        KILLED.append(instrL[i][1])
        i -=1
    
    NKILL = AVAILin
    for e in NKILL:
        for v in e:
            if estVar(v):
                if v in KILLED:
                    NKILL.remove(e)
    return DEF, KILLED, NKILL

def estOpbin(op):
    if len(op)==4:
        if op[0]=='opbin':
            return True
    return False

def estVar(v):
    if len(v) == 2:
        if v[0] == 'var':
            return True
    return False 


def calculGeneralBackward(graph):
    """"Calcul des ensembles définies précédemment pour tous les blocs du bas en haut"""
    n = len(graph)
    DEF = [[] for i in range(n)]
    USE = [[] for i in range(n)]
    AVAILin = [[] for i in range(n+1)]
    AVAILout = [[] for i in range(n+1)]
    AVAILin[n] = [expr_dump(graph[n-1][0][0])]
    CopieIn = []
    CopieOut =[]
    while CopieIn != AVAILin and CopieOut != AVAILout :
        CopieIn = list(AVAILin)
        CopieOut = list(AVAILout)
        for bloc in range(n-1,-1,-1):
            AVAILout[bloc] = list(AVAILin[bloc+1])
            for i in range(n-1, bloc, -1):
                if  len(graph[bloc][1]) == 2 and bloc in graph[i][1]:
                    AVAILout[bloc] = list(set(AVAILout[bloc] + AVAILout[graph[bloc][1][1]]))
            DEF[bloc], USE[bloc] = calculGenKilledNKilledBackward(graph[bloc][0])
            if not len(DEF[bloc]) == 0 :
                NKILL = list(set(AVAILout[bloc])-set(DEF[bloc]))
                AVAILin[bloc] = list(set(USE[bloc] + NKILL))
            else : 
                AVAILin[bloc] = list(set(USE[bloc] + AVAILout[bloc]))
    return DEF, USE, AVAILin, AVAILout

def calculGenKilledNKilledBackward(instr):
    """Calcul des ensembles définies précédemment pour un bloc de bas en haut"""
    USE = []
    DEF = []
    if instr[0] == 'if' or instr[0] == 'while':
        if estVar(instr[1][1]):
            USE.append(expr_dump(instr[1][1]))
        if estVar(instr[1][3]):
            USE.append(expr_dump(instr[1][3]))
    elif estVar(instr[0]):
        USE.append(expr_dump(instr[0]))
    else :
        instr = instr[0]
        DEF.append(expr_dump(instr[1]))
        if estOpbin(instr[2]):
            if estVar(instr[2][1]):
                USE.append(expr_dump(instr[2][1]))
            if estVar(instr[2][3]):
                USE.append(expr_dump(instr[2][3]))
        elif estVar(instr[2]):
            USE.append(expr_dump(instr[2][1]))
    return DEF, USE

print("\n")
DEF, USE, AVAILin, AVAILout = calculGeneralBackward(graph)
print(DEF)
print("\n")
print(USE)
print("\n")
print(AVAILin)
print("\n")
print(AVAILout)

# Ces ensembles sont ensuites nécessaires pour différents types d'optimisation
# que j'ai listé si dessous
    
def optiCFG(graph):
    """Transforme le CFG en graph sans code mort avec des blocs de base 
    optimisés"""
    DEF, KILLED, NKILL, AVAILin, AVAILout = calculGeneralForward(graph)
    graph = RD(DEF, KILLED, NKILL, AVAILin, AVAILout,graph)
    graph = VBE(DEF, KILLED, NKILL, AVAILin, AVAILout,graph)
    graph = AvailExpr(DEF, KILLED, NKILL, AVAILin, AVAILout,graph)
    DEF, USE, NKILL, AVAILin, AVAILout = calculGeneralBackward(graph)
    graph = Liveness(DEF, USE, NKILL, AVAILin, AVAILout,graph)
    return graph

def RD(DEF, KILLED, NKILL, AVAILin, AVAILout,graph):
    """Propagation de constante"""
    return graph

def VBE(DEF, KILLED, NKILL, AVAILin, AVAILout,graph):
    """Code hoisting"""
    return graph

def Liveness(DEF, USE, NKILL, AVAILin, AVAILout,graph):
    """Dead code elimination"""
    return graph

def AvailExpr(DEF, KILLED, NKILL, AVAILin, AVAILout,graph):
    """Elimination d’expression commune"""
    return graph

def optiGlobal(parser):
    """Optimise le code parsé"""
    graph = codeToCFG(parser)
    optiCFG(graph)   
    return CFGtoCode(graph)



