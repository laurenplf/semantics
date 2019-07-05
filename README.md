# semantics
Projet Semantics

## Ajout de CodeToCFG

Transforme le code en graph de controle de flot

### programme 

main(a,b,c){a = c; while(a < 1){a = a + 1; if(a > 4){b = b - 1;} c= a + 1;} a= a+3; a=b+2; return a;}

### Architecture et résultat :

- [(('var', 'a'), ('var', 'b'), ('var', 'c')), []]


- [[('affect', ('var', 'a'), ('var', 'c')), 'while', ('opbin', ('var', 'a'), 'lt', ('nb', '1'))], [2, 5]]


- [[('affect', ('var', 'a'), ('opbin', ('var', 'a'), '+', ('nb', '1'))), 'if', ('opbin', ('var', 'a'), 'gt', ('nb', '4'))], [3, 4]]


- [[('affect', ('var', 'b'), ('opbin', ('var', 'b'), '-', ('nb', '1')))], [4]]


- [[('affect', ('var', 'c'), ('opbin', ('var', 'a'), '+', ('nb', '1')))], [5]]


- [[('affect', ('var', 'a'), ('opbin', ('var', 'a'), '+', ('nb', '3'))), ('affect', ('var', 'a'), ('opbin', ('var', 'b'), '+', ('nb', '2')))], [('var', 'a')]]



## Ajout de CFGtoCode

Transforme le graph de controle de flot en code

### Résultat

- Avec CFG obtenu précédemment :
- main(a,b,c){a = c; while(a < 1){a = a + 1; if(a > 4){b = b - 1; }c = a + 1; }a = a + 3; a = b + 2; return a;}

