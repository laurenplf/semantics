# semantics
Projet Semantics

## Ajout de CodeToCFG

Transforme le code en graph de controle de flot

### programme 

main(a,b,c){a = c; while(a < 1){a = a + 1; if(a > 4){b = b - 1;} c= a + 1;} a= a+3; a=b+2; return a;}

### Architecture et résultat :

[(('var', 'a'), ('var', 'b'), ('var', 'c')), []]


[[('affect', ('var', 'a'), ('var', 'c'))], [2]]


[['while', ('opbin', ('var', 'a'), 'lt', ('nb', '1'))], [3, 7]]


[[('affect', ('var', 'a'), ('opbin', ('var', 'a'), '+', ('nb', '1')))], [4, 6]]


[['if', ('opbin', ('var', 'a'), 'gt', ('nb', '4'))], [5, 6]]


[[('affect', ('var', 'b'), ('opbin', ('var', 'b'), '-', ('nb', '1')))], [4]]


[[('affect', ('var', 'c'), ('opbin', ('var', 'a'), '+', ('nb', '1')))], 2]


[[('affect', ('var', 'a'), ('opbin', ('var', 'a'), '+', ('nb', '3')))], [8]]


[[('affect', ('var', 'a'), ('opbin', ('var', 'b'), '+', ('nb', '2')))], [9]]



## Ajout de CFGtoCode

Transforme le graph de controle de flot en code

### Résultat

- Avec CFG obtenu précédemment :
- main(a,b,c){a = c; while(a < 1){a = a + 1; if(a > 4){b = b - 1; }c = a + 1; }a = a + 3; a = b + 2; return a;}

