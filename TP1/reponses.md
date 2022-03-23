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
  

### 2) Comment représenter une solution (en programmation) ?

### 3) Comment évaluer une solution réalisable ? Comment évaluer une solution non réalisable ?

### 4) Proposer des instances pour lesquelles il n’existe pas de solution réalisable, chacune pour une contrainte différente.

## Premières heuristiques

### 1) Proposer une méthode déterministe pour construire une solution qui passe par le dépôt autant de fois que nécessaire pour respecter toutes les contraintes. Cette méthode doit être polynomiale

#### a. Indiquer la complexité de la méthode.

#### b. Donner un exemple d’instance où la solution renvoyée utilise plus d’un véhicule.

#### c. Donner un exemple d’instance où la solution renvoyée est optimale.

### 2) Proposer une ou plusieurs heuristiques non déterministes pour construire une solution admissible. On veut que les solutions produites soient différentes à chaque exécution. Comment définir « différentes » ?