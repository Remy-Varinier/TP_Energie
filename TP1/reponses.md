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
-Vehicle (un véhicule),
-listeVisites (liste de visites)

Objectif :
On cherche à minimiser le nombre de kilomètre fait par les tous les camions de livraison
Fonction objectif : min(sum(calcDist(listeVisites)))

Contraintes :
-La durée totale d'un trajet dans visit_list, y compris les temps de livraison et de rechargement, ne dépasse pas (end_time-start_time).
-Pour tout morceau de trajet entre deux étapes C (passage au dépôt) ou R (recharge) indifféremment, la distance ne doit pas dépasser max_dist.
-Pour tout morceau de trajet entre deux C (passage au dépôt), la capacité d'un camion ne dépasse pas capacity.

Pour info --- Constantes dans vehicle.ini :
max_dist, capacity, charge_fast, charge_medium, charge_slow, start_time, end_time,
demand (nombre de sacs à livrer),
time (temps de trajet entre deux dépôts),
distance (distance entre deux dépôts)



### 2) Comment représenter une solution (en programmation) ?

### 3) Comment évaluer une solution réalisable ? Comment évaluer une solution non réalisable ?

La solution est réalisable si elle respecte toutes les contraintes.


### 4) Proposer des instances pour lesquelles il n’existe pas de solution réalisable, chacune pour une contrainte différente.

Exemples d'instances :
-S'il existe un lieu à livrer dont la distance minimale pour la rejoindre est supérieure au max_dist de tous les camions
-S'il existe un lieu à livrer réclamant plus de sacs que la capacité max des camions (car selon la consigne, un client ne peut être livré qu'en une seule fois)


## Premières heuristiques

### 1) Proposer une méthode déterministe pour construire une solution qui passe par le dépôt autant de fois que nécessaire pour respecter toutes les contraintes. Cette méthode doit être polynomiale

Pour chaque camion :
  Tant que nb(lieux_non_livres) != 0:
    Rechercher le lieu non livré le plus proche;
    Si (distance > (max_dist - currentKilometer)):
      Recharger le véhicule;
    Si (demande > currentCapacity):
      Aller au dépôt; 
    Sinon :
      Sélectionner le lieu;
      lieux_non_livres -= 1;


#### a. Indiquer la complexité de la méthode.

#### b. Donner un exemple d’instance où la solution renvoyée utilise plus d’un véhicule.

#### c. Donner un exemple d’instance où la solution renvoyée est optimale.

### 2) Proposer une ou plusieurs heuristiques non déterministes pour construire une solution admissible. On veut que les solutions produites soient différentes à chaque exécution. Comment définir « différentes » ?