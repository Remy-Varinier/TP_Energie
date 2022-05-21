Pour lancer le projet : Appeller le script main.py contenu dans TP1/main.
2 méthodes sont possibles pour renseigner les options :
- Les renseigner sous forme d'arguments :
  ````
  usage: main.py [-h] [--folder path] [--mode name] [--neighbour number]

  optional arguments:
  -h, --help          show this help message and exit
  --folder path       relative path to data folder containing all needed files
  --mode name         chosen mode to build tours. Values : Glouton | Naif |
                      Random
  --neighbour number  chosen mode to find neighbours. Values : 1 | 2 | 3 | 4
  
- Modifier les constantes dans le code : `FOLDER`, `MODE_TOUR`, `MODE_VOISINAGE`.

La priorité est donnée à la méthode arguments.

Fichiers supplémentaires :

- requirements.txt : Définit les dépendances externes à installer avant exécution.
- Les réponses aux questions sont dans reponses.md.
- Des exemples d'entrées/sorties sont disponibles dans output.txt.
- Les méthodes de test sont rangées dans le même dossier que le code.