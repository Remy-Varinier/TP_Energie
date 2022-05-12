# /usr/bin/python3
import typing

from globals import Globals
from tour import Tour


# VARIABLES DE CONFIGURATION (si on appelle le module sans argument fourni)
FOLDER = "../Data/lyon_150_1_1/"
MODE = "Random"

#remainingVisits: typing.List[Visit], vehicleModel: Vehicle, distanceMatrix, timeMatrix,
def buildTours(global_vars: Globals, mode: str="Glouton") -> typing.Tuple[typing.List[Tour], str]:
    """
    Construit la liste de tours ainsi que la chaîne de caractères affichable.

    :param global_vars: Objet contenant les variables globales : liste de visites à effectuer, modèle du véhicule, matrice des distances, matrice des temps
    :param mode: "Glouton" | "Naif" | "Random" (par défaut Glouton)
    :return: Tuple(liste des tours, chaîne de caractères)
    """
    depot = global_vars.listVisits.pop(0)
    v = global_vars.vehicleModel.clone()
    current_tour = Tour([], v)
    (remainingVisits, str_tour) = current_tour.buildTour(mode, global_vars.listVisits, depot, global_vars.distances, global_vars.times)
    result = [current_tour]
    str_tours = str_tour
    while len(remainingVisits) > 0:
        v = global_vars.vehicleModel.clone()
        current_tour = Tour([], v)
        (remainingVisits, str_tour) = current_tour.buildTour(mode, global_vars.listVisits, depot, global_vars.distances, global_vars.times)
        result.append(current_tour)
        str_tours += "\n"+str_tour
    return (result, str_tours)


### TP2 CONSTRUIRE LES VOISINAGES ###
def doVoisinage1(global_vars: Globals, listTours: typing.List[Tour], tIndex: int, v1Index: int, v2Index: int) -> bool:
    """Echanger deux visites dans un tour.

    :param global_vars: Objet contenant les variables globales : Modèle de véhicule, matrice des distances, matrice des temps
    :param listTours: liste des Tour
    :param tIndex: l'index du Tour à modifier
    :param v1Index, v2Index: index des visites à échanger
    """
    try:
        listTours[tIndex].swapVisits(v1Index, v2Index)
        return listTours[tIndex].isAValidTour(global_vars.vehicleModel, global_vars.distances, global_vars.times)
    except IndexError:
        return False


def doVoisinage2(global_vars: Globals, listTours: typing.List[Tour], t1Index: int, t2Index: int, v1Index: int, v2Index: int) -> bool:
    """A partir de deux tours T1 et T2 sélectionnés dans une liste de tours,
    retirer une visite de T1 et l'ajouter sur T2.

    :param global_vars: Objet contenant les variables globales : Modèle de véhicule, matrice des distances, matrice des temps
    :param listTours: liste des Tour
    :param t1Index, t2Index: index des Tour à modifier
    :param v1Index, v2Index: index de départ sur T1 et d'arrivée sur T2
    """
    try:
        item = listTours[t1Index].visits.pop(v1Index)
        listTours[t2Index].visits.insert(v2Index, item)
        #Retirer un tour sur t1Index le rend toujours valide
        return listTours[t2Index].isAValidTour(global_vars.vehicleModel, global_vars.distances, global_vars.times)
    except IndexError:
        return False


def doVoisinage3(global_vars: Globals, listTours: typing.List[Tour], t1Index: int, t2Index: int) -> bool:
    """A partir de deux tours T1 et T2 sélectionnés dans une liste de tours,
    prendre le dernier morceau de T1 (toutes les visites après le dernier 'C' ou 'R') et le déplacer sur la fin de T2.

    :param global_vars: Objet contenant les variables globales : Modèle de véhicule, matrice des distances, matrice des temps
    :param listTours: liste des Tour
    :param t1Index: index du Tour à modifier
    :param t2Index:
    """
    try:
        itemIndex = listTours[t1Index].findCorRVisits()[-1]
        listEnd = listTours[t1Index].visits[itemIndex:]
        del listTours[t1Index].visits[itemIndex:]
        listTours[t2Index].visits.extend(listEnd)
        #Retirer un tour sur t1Index le rend toujours valide
        return listTours[t2Index].isAValidTour(global_vars.vehicleModel, global_vars.distances, global_vars.times)
    except IndexError:
        return False


def doVoisinage4(global_vars: Globals, listTours: typing.List[Tour], tIndex: int, crIndex: int=0, shift: int=1) -> bool:
    """Déplacer une étape 'C' ou 'R' dans un tour.

    :param global_vars: Objet contenant les variables globales : Modèle de véhicule, matrice des distances, matrice des temps
    :param listTours: liste des Tour
    :param tIndex: l'index du Tour à modifier
    :param crIndex: l'index de l'étape 'C' ou 'R' à retenir
    :param shift: déplacement de l'élement à effectuer (par défaut 1 élement après).
    """
    try:
        itemIndex = listTours[tIndex].findCorRVisits()[crIndex]
        item = listTours[tIndex].visits.pop(itemIndex)
        listTours[tIndex].visits.insert(itemIndex + shift, item)
        return listTours[tIndex].isAValidTour(global_vars.vehicleModel, global_vars.distances, global_vars.times)
    except IndexError:
        return False


def main(the_mode=MODE, the_folder=FOLDER):

    print("Le mode choisi est : ", the_mode)
    print("Le dossier choisi est : ", the_folder)

    my_globals = Globals()
    my_globals.define(the_folder)

    ### TP1 CONSTRUIRE LES TOURS ###
    (listTours, the_result) = buildTours(my_globals, mode=the_mode)
    print(the_result)

    ### TP2 CONSTRUIRE LES VOISINAGES ###
    doVoisinage1(my_globals, listTours, 0, 3, 4) #Modifie le listTours en paramètre comme attendu


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', metavar='path', required=False, default=FOLDER,
                        help='relative path to data folder containing all needed files')
    parser.add_argument('--mode', metavar='path', required=False, default=MODE,
                        help='chosen mode to build tours. Values : Glouton | Naif | Random')
    args = parser.parse_args()
    main(the_mode=args.mode, the_folder=args.folder)




