# Création d'un compilateur : pointeurs

## Syntaxe des pointeurs

Toute variable qui commence par la lettre p ou la lettre q est un pointeur (p et q eux-mêmes compris)

## Opérations supportées sur les pointeurs

On peut réaliser les opérations suivantes avec les pointeurs:


### Allocation de mémoire à un pointeur
p = malloc(expr) fait pointer p sur une case mémoire où expr correspond au nombre d'octets à allouer

### Affectation d'adresse à un pointeur
p = &i (où p est un pointeur et i une variable quelconque) affecte à p l'adresse de l'objet i.

### Affectation d'une valeur à un pointeur
\*p = expr affecte à la valeur du pointeur p l'expression expr
a = \*p affecte à l'ID a la valeur du pointeur p
On peut aussi utiliser des pointeurs mutliples: \*\*p = expr...

