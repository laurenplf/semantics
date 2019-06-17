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
main(tableau){
    n=len(tableau);
    inversion=1;
    i=0;
    while(inversion>0){
        inversion=0;
        while (i<n){
            vala=tableau[i];
            valb=tableau[i+1];
            if (tableau[i+1]<tableau[i]){
                inversion=1;
                tableau[i]=valb;
                tableau[i+1]=vala;
            i=i+1;
        }
    }
}
return tableau;
} 
