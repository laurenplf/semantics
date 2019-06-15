# Semantics
# Compilateur : les fonctions

Possibilité de déclarer des fonctions autres que "main"

## Déclaration des fonctions

- Les fonctions annexes doivent être déclarées AVANT "main". Une déclaration après "main" entraînera un échec au niveau du parser
- Il n'y a pas de limitation quant au nombre de fonctions annexes qui peuvent être déclarées mais elles doivent l'être comme en C (en faisant abstraction du typage)
- Il n'y a pas de limitation quant au nombre d'arguments que peut attendre une fonction annexe mais il doivent être séparés par des virgules
- Le "main" a besoin d'au moins un argument et ne peut pas avoir de bloc d'instructions vide (contrairement aux fonctions annexes qui peuvent se passer d'instructions)
- Les fonctions annexes appelant d'autres fonctions annexes dans leur blocs d'instructions sont autorisées
- Les fonctions annexes récursives sont autorisées

## Utilisation des fonctions

- Les appels de fonctions s'effectuent comme en C
- Les paramètres donnés à la fonction annexe peuvent être des variables
    + des sommes de variables
    + des nombres
    + un résultat d'une autre fonction annexe appelée en argument

## Avertissement

- Les nombres négatifs ne sont pas pris en charge (ou alors pas correctement). Les entiers sont non signés, en conséquence, il vaut mieux éviter l'opération de soustraction et le passage de nombres négatifs en argument pour "main"

## Exemple

'''  
zero(){  
    &ensp;&ensp;&ensp;&ensp;return 0;  
}  
  
test(a, b , c, d){  
    &ensp;&ensp;&ensp;&ensp;a = a + b;  
    &ensp;&ensp;&ensp;&ensp;a = a + c;  
    &ensp;&ensp;&ensp;&ensp;a = a + d;  
    &ensp;&ensp;&ensp;&ensp;return a;  
}  
  
inc(a){  
    &ensp;&ensp;&ensp;&ensp;if(a < 10){  
        &ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;b = inc(a + 1);  
    &ensp;&ensp;&ensp;&ensp;}  
    &ensp;&ensp;&ensp;&ensp;if(a >= 10){  
        &ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;b = 10;  
    &ensp;&ensp;&ensp;&ensp;}  
    &ensp;&ensp;&ensp;&ensp;return b;  
}  
  
f(d, e){  
    &ensp;&ensp;&ensp;&ensp;d = d + 1;  
    &ensp;&ensp;&ensp;&ensp;e = e + d;  
    &ensp;&ensp;&ensp;&ensp;h = g(d, e);  
    &ensp;&ensp;&ensp;&ensp;return h;  
}  

g(h, i){  
    &ensp;&ensp;&ensp;&ensp;i = i + h;  
    &ensp;&ensp;&ensp;&ensp;return i;  
}  
  
main(a, b, c){  
    &ensp;&ensp;&ensp;&ensp;c = a + c;  
    &ensp;&ensp;&ensp;&ensp;a = g(inc(a + c), d);  
    &ensp;&ensp;&ensp;&ensp;d = f(c + a, d);  
    &ensp;&ensp;&ensp;&ensp;d = inc(f(d, a));  
    &ensp;&ensp;&ensp;&ensp;d = zero();  
    &ensp;&ensp;&ensp;&ensp;return d;  
}  
'''

## Compilation du code assembleur produit

- nasm -f elf64 <nom_fichier>.asm
- gcc <nom_fichier>.o -o <nom_executable> -no-pie
