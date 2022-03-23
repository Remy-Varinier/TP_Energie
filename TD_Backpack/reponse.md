# Problème du sac à dos

| Objet (x) | Valeur (V) | Poids (P) |
| :-------: | :--------: | :-------: |
|     1     |     7      |    13     |
|     2     |     4      |    12     |
|     3     |     3      |     8     |
|     4     |     3      |    10     |

---

## 1) Quelles sont les variables de décision, l’objectif et les contraintes du problème ?

- Les variables de décision sont:

  - x1: booleen qui représente si le l'objet 1 est dans le sac
  - x2: booleen qui représente si le l'objet 2 est dans le sac
  - x3: booleen qui représente si le l'objet 3 est dans le sac
  - x4: booleen qui représente si le l'objet 4 est dans le sac

- L'objectif est: $ z = max 7 \times x1 + 4 \times x2 + 3 \times x3 + 3 \times x4 \Rightarrow \sum_{i = 1}^{4} Vi \times xi$

- Les contraintes sont:
  - $ 13 \times x1 + 12 \times x2 + 8 \times x3 + 10 \times x4 \leq 30 \Rightarrow \sum_{i=1}^{4} Pi \times xi $
  - $ x1 \in \{0, 1\} $
  - $ x2 \in \{0, 1\} $
  - $ x3 \in \{0, 1\} $
  - $ x4 \in \{0, 1\} $
$ \Rightarrow \forall xi \in \{0, 1\} $

## 2) Solution réalisable/admissible

### a. Proposer une solution non réalisable pour l’exemple

- $ x1 = 1; x2 = 1; x3 = 1; x4 = 1; $

### b. Supposons qu’on doit au minimum mettre un objet dans le sac. Proposer une instance pour laquelle il n’y a pas de solution réalisable

- Ajouter une contrainte $ x1 + x2 + x3 + x4 >= 1 $
- Changer le poid de tous les objets par 31 (car 31 > 30)

Après ces changements il n'y a pas de solution réalisable

## 3) Proposer une méthode exacte pour résoudre le problème.

### a. Quelle est sa complexité ?

$ \sum C_n^k \Rightarrow 2^n$ (le $C_n^k$ represente un ensemble comme par exemple $\{1, 3, 4\}$)


## 4) Proposer une heuristique gloutonne qui donne toujours une solution réalisable 
Optim local Vi
```
ensemble = {}
usort de X via décroissant de Vi => complexité O(n * ln(n))
p = 0
v = 0
foreach (obj in X){
  if (p+ obj.p <= C) {
    ensemble = ensemble U {obj}
    p += obj.p
    v += obj.v
  }
} => complexité O(n)
```
### a. Quelle est sa complexité ?
La complexité est: $O(n \times \ln(n))$ car :
la complexité $O(n)$ est très inférieure à $O(n \times \ln(n))$ donc on garde que cette dernière.

## 5) Proposer un algorithme constructif non déterministe polynomial 

```
algo(capa, list){
  poidSac = 0;
  solution = [];
  for(i = 0; i < list.lengh; i++) {
    elem = randomElem(list);
    if(elem.poid + poidSac <= capa) {
      poidSac += elem.poid
      list.pop(elem)
      solution.push(elem)
    }
  }
  return solution.reduce(fn (e, acc)=> acc + e)
}
```