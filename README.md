# Semantics
# Compilateur : les fonctions

Possibilité de déclarer des fonctions autres que "main".

## Déclaration des fonctions

- Les fonctions annexes doivent être déclarées AVANT "main". Une déclaration après "main" entraînera un échec au niveau du parser.
- Il n'y a pas de limitation quant au nombre de fonctions annexes qui peuvent être déclarées mais elles doivent l'être comme en C (en faisant abstraction du typage)
- Il n'y a pas de limitation quant au nombre d'arguments que peut attendre une fonction annexe mais il doivent être séparés par des virgules
- Le "main" a besoin d'au moins un argument et ne peut pas avoir de bloc d'instructions vide (contrairement aux fonctions annexes qui le peuvent)
- Les fonctions annexes appelant d'autres fonctions annexes dans leur blocs d'instructions sont autorisées
- Les fonctions annexes récursives sont autorisées

## Utilisation des fonctions

- Les appels de fonctions s'effectuent comme en C
- Les paramètres donnés à la fonction annexe peuvent être des variables, des sommes de variables, des nombres, un résultat d'une autre fonction annexe appelée en argument
