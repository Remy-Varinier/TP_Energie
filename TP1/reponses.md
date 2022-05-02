# Livraison avec des véhicules électriques

## Modélisation

### 1) Quelles sont les variables de décision ? Quelles sont les contraintes ? Quels sont les objectifs ?

- Les variables de décision sont:
  - ListeVisites: represente le tour pour chaque camion
- L'objectif est:
  - On cherche à minimiser le nombre de kilomètre fait par les tous les camions de livraison pour finir toutes les livraisons en une journée
  - $z = min \sum calcKilometre(ListeVisite_i) $ calcKilometre calcule les kilometres d'un tour
- Les contraites sont:
  - $calcTemp(ListeVisite_i) \leq Vehicle.endTime - Vehicle.startTime $ calcTemp calcule le temps mis pour un tour donné
  - $calcEnergie(ListeVisite_i, Vehicle.maxDist) = 0$ calcEnergie renvoie true si le tour ne respecte pas la distance maximum du vehicule
  - $uneSeuleLivraison(ListeVisite) = 1$ uneSeuleLivraison renvoie true si les clients sont livrer qu'une seule fois
  - $jamaisCapaciteDepasse(ListeVisite_i) = 1$ jamaisCapaciteDepasse renvoie true si la capacite max du vehicule n'est pas depassé pendant le tour


---------------------

Variables de décision :
- Vehicle (un véhicule),
- listeVisites (liste de visites).

Objectif :
- On cherche à minimiser le nombre de kilomètre fait par les tous les camions de livraison
- Fonction objectif : min(sum(calcDist(listeVisites)))

Contraintes :
- La durée totale d'un trajet dans visit_list, y compris les temps de livraison et de rechargement, ne dépasse pas (end_time-start_time).
- Pour tout morceau de trajet entre deux étapes C (passage au dépôt) ou R (recharge) indifféremment, la distance ne doit pas dépasser max_dist.
- Pour tout morceau de trajet entre deux C (passage au dépôt), la capacité d'un camion ne dépasse pas capacity.

Pour info --- Constantes dans vehicle.ini :
max_dist, capacity, charge_fast, charge_medium, charge_slow, start_time, end_time,
demand (nombre de sacs à livrer),
time (temps de trajet entre deux dépôts),
distance (distance entre deux dépôts)



### 2) Comment représenter une solution (en programmation) ?

TODO voir code

### 3) Comment évaluer une solution réalisable ? Comment évaluer une solution non réalisable ?

La solution est réalisable si et seulement si elle respecte toutes les contraintes : On souhaite livrer la totalité des sites tout en prenant garde à ce que :
- Le kilométrage des camions soit cohérent durant tout le trajet (entre deux passages au dépôt ou des recharges, la distance totale ne dépasse jamais max_dist)
- La capacité totale d'un camion n'est jamais dépassé durant tout le trajet.


### 4) Proposer des instances pour lesquelles il n’existe pas de solution réalisable, chacune pour une contrainte différente.

Exemples d'instances :
- S'il existe un lieu à livrer dont la distance minimale pour la rejoindre est supérieure au max_dist de tous les camions
- S'il existe un lieu à livrer réclamant plus de sacs que la capacité max des camions (car selon la consigne, un client ne peut être livré qu'en une seule fois)


## TP1 : Premières heuristiques

### 1) Proposer une méthode déterministe pour construire une solution qui passe par le dépôt autant de fois que nécessaire pour respecter toutes les contraintes. Cette méthode doit être polynomiale

  Il faut que l'algorithme soit déterministe : il ne doit pas avoir de variables aléatoires.
  Il faut que l'algorithme respecte toutes les contraintes :
    - Un camion doit pouvoir faire toute les livraisons sans tomber en panne
    - Un camion doit livrer un client en une seule fois
    - Les camions doit respecter l'heure de départ et d'arrivée
  Voir le code pour plus de détails. Notament, la fonction `buildTours` défini dans `main.py`.
  
#### a. Indiquer la complexité de la méthode.

Pour chaque lieu -> O(n)\
Recherche du lieu -> O(n)\
Total = O(n^2)


#### b. Donner un exemple d’instance où la solution renvoyée utilise plus d’un véhicule.

TODO


#### c. Donner un exemple d’instance où la solution renvoyée est optimale.

TODO

### 2) Proposer une ou plusieurs heuristiques non déterministes pour construire une solution admissible. On veut que les solutions produites soient différentes à chaque exécution. Comment définir « différentes » ?

A la place d'une recherche pour sélectionner le prochain lieu non livré, on peut le sélectionner aléatoirement et contrôler s'il est admissible.



##TP2 : Voisinages

### 1) Proposer au moins trois voisinages de solutions. Dans chaque cas vous indiquerez la taille du voisinage et s'il est de taille polynomiale par rapport à la taille de l'instance. Indiquez aussi pour chaque voisinage s'il peut contenir des solutions non réalisables.

En partant d'une solution quelconque :

- On peut échanger deux visites dans un même tour (donc pour un véhicule),
- On peut retirer une visite d'un tour pour l'ajouter sur un autre tour,
- Prendre le dernier morceau d'un tour donné (toutes les visites après le dernier 'C' ou 'R') et le déplacer sur un autre tour.

Tailles des voisinages = S

Complexité :

- O(n^2)
- O(n^2)
- a

Renvoie possiblement des solutions non réalisables à partir de solutions réalisables :

- Oui (Non si on recalcule les retours au dépôt + rechargements de façon optimale) 
- Oui
- Oui


### 2) Descentes : Améliorez la solution obtenue à l'aide de la méthode déterministe en cherchant à chaque pas la meilleure solution d'un voisinage choisi parmi les 3 proposés. Comparer l'exécution et le résultat obtenus avec le cas où on prend la première solution du voisinage rencontrée qui améliore la solution.

### 3) Descentes avec départ "aléatoire". Utiliser l'heuristique constructive non-déterministe pour générer plusieurs solutions et améliorer chacune d'elle.

### Vitesse de rechargement et flotte de véhicules

### 4) Pour chaque taille d'instance, quel est en général le nombre de véhicules nécessaires et le nombre de rechargements de la batterie dans chacun des cas rechargement rapide, rechargement medium, rechargement lent ?

### 5) Quel type de rechargement conseillerez-vous pour cette flotte de véhicules ?

### 6) Si on voulait renouveler la flotte de véhicules pour qu'ils puissent effectuer plus de kilomètres avant rechargement, quelle autonomie minimum serait appropriée pour éviter dans la plupart des cas les rechargmeents en cours de journée ? Quel serait alors la nombre de véhicules nécessaires pour les différentes tailles d'instances ?