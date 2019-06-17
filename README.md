# semantics

## Partie sur les tableaux 

Le programme peut gérer les lignes suivantes: 
- int id[nbr]; 
- int id[nbr]={nbr,nbr};
- len(id);
- id[expr]=expr;
- id=id[expr]; 

Avec un première programme simple: '''main(a){int l[6]={1,2,3,4,5,6};l[2]=5; return a;}'''

Puis avec un programme effectuant le tri à bulle d'un tableau : 


main(a){
    int tableau[4]={5,4,3,2};
    n=len(tableau);
    inversion=1;
    i=0;
    while(inversion>0){
        inversion=0;
        while (i<n-1){
            vala=tableau[i];
            valb=tableau[i+1];
            if (tableau[i+1]<tableau[i]){
                inversion=1;
                tableau[i]=valb;
                tableau[i+1]=vala;
                }
            i=i+1;
    }
}
return tableau;
} 


Je n'ai pas encore réussi à mettre la liste en argument de mon main car je ne peux mettre que des varlists or si je souhaite accéder à la taille de ma liste, il faut que je l'ai déclarée quelque part. 
