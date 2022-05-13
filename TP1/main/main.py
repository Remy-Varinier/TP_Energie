# /usr/bin/python3
import typing

from globals import Globals
from tour import Tour

# VARIABLES DE CONFIGURATION (si on appelle le module sans argument fourni)
FOLDER = "../Data/lyon_150_1_1/"
MODE = "Glouton"


#remainingVisits: typing.List[Visit], vehicleModel: Vehicle, distanceMatrix, timeMatrix,
def buildTours(global_vars: Globals, mode: str = "Glouton") -> typing.Tuple[typing.List[Tour], str]:
    """
    Construit la liste de tours ainsi que la chaîne de caractères affichable.

    :param global_vars: Objet contenant les variables globales :
        liste de visites à effectuer, modèle du véhicule, matrice des distances, matrice des temps
    :param mode: "Glouton" | "Naif" | "Random" (par défaut Glouton)
    :return: Tuple(liste des tours, chaîne de caractères)
    """
    depot = global_vars.list_visits.pop(0)
    v = global_vars.vehicle_model.clone()
    current_tour = Tour([], v)
    remaining_visits = current_tour.buildTour(
        mode, global_vars.list_visits, depot, global_vars.distances, global_vars.times)
    result = [current_tour]
    str_tours = current_tour.str_tour
    while len(remaining_visits) > 0:
        v = global_vars.vehicle_model.clone()
        current_tour = Tour([], v)
        remaining_visits = current_tour.buildTour(
            mode, global_vars.list_visits, depot, global_vars.distances, global_vars.times)
        result.append(current_tour)
        str_tours += "\n" + current_tour.str_tour
    return result, str_tours


#Méthodes pour construire les voisinages
def doVoisinage1(global_vars: Globals, list_tours: typing.List[Tour], tindex: int, v1index: int, v2index: int) -> bool:
    """Echanger deux visites dans un tour.

    :param global_vars: Objet contenant les variables globales :
            Modèle de véhicule, matrice des distances, matrice des temps
    :param list_tours: liste des Tour
    :param tindex: l'index du Tour à modifier
    :param v1index, v2index: index des visites à échanger
    """
    try:
        list_tours[tindex].swapVisits(v1index, v2index)
        return list_tours[tindex].isAValidTour(global_vars.distances, global_vars.times)
    except IndexError:
        return False


def doVoisinage2(global_vars: Globals, list_tours: typing.List[Tour], t1index: int, t2index: int, v1index: int,
                 v2index: int) -> bool:
    """A partir de deux tours T1 et T2 sélectionnés dans une liste de tours,
    retirer une visite de T1 et l'ajouter sur T2.

    :param global_vars: Objet contenant les variables globales :
            Modèle de véhicule, matrice des distances, matrice des temps
    :param list_tours: liste des Tour
    :param t1index, t2index: index des Tour à modifier
    :param v1index, v2index: index de départ sur T1 et d'arrivée sur T2
    """
    try:
        item = list_tours[t1index].visits.pop(v1index)
        list_tours[t2index].visits.insert(v2index, item)
        #Retirer un tour sur t1Index le rend toujours valide
        return list_tours[t2index].isAValidTour(global_vars.distances, global_vars.times)
    except IndexError:
        return False


def doVoisinage3(global_vars: Globals, list_tours: typing.List[Tour], t1index: int, t2index: int) -> bool:
    """A partir de deux tours T1 et T2 sélectionnés dans une liste de tours,
    prendre le dernier morceau de T1 (toutes les visites après le dernier 'C' ou 'R') et le déplacer sur la fin de T2.

    :param global_vars: Objet contenant les variables globales :
            Modèle de véhicule, matrice des distances, matrice des temps
    :param list_tours: liste des Tour
    :param t1index: index du Tour à modifier
    :param t2index:
    """
    try:
        item_index = list_tours[t1index].findCorRVisits()[-1]
        list_end = list_tours[t1index].visits[item_index:]
        del list_tours[t1index].visits[item_index:]
        list_tours[t2index].visits.extend(list_end)
        #Retirer un tour sur t1Index le rend toujours valide
        return list_tours[t2index].isAValidTour(global_vars.distances, global_vars.times)
    except IndexError:
        return False


def doVoisinage4(global_vars: Globals, list_tours: typing.List[Tour], tindex: int, crindex: int = 0,
                 shift: int = 1) -> bool:
    """Déplacer une étape 'C' ou 'R' dans un tour.

    :param global_vars: Objet contenant les variables globales :
            Modèle de véhicule, matrice des distances, matrice des temps
    :param list_tours: liste des Tour
    :param tindex: l'index du Tour à modifier
    :param crindex: l'index de l'étape 'C' ou 'R' à retenir
    :param shift: déplacement de l'élement à effectuer (par défaut 1 élement après).
    """
    try:
        item_index = list_tours[tindex].findCorRVisits()[crindex]
        item = list_tours[tindex].visits.pop(item_index)
        list_tours[tindex].visits.insert(item_index + shift, item)
        return list_tours[tindex].isAValidTour(global_vars.distances, global_vars.times)
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
    doVoisinage1(my_globals, listTours, 0, 3, 4)  #Modifie le listTours en paramètre comme attendu


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', metavar='path', required=False, default=FOLDER,
                        help='relative path to data folder containing all needed files')
    parser.add_argument('--mode', metavar='path', required=False, default=MODE,
                        help='chosen mode to build tours. Values : Glouton | Naif | Random')
    args = parser.parse_args()
    main(the_mode=args.mode, the_folder=args.folder)
