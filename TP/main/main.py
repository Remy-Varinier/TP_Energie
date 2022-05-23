# /usr/bin/python3
import typing
import copy

from globals import Globals
from tour import Tour

# VARIABLES DE CONFIGURATION (si on appelle le module sans argument fourni)
FOLDER = "../Data/lyon_100_1_1/"
MODE_TOUR = "Naif"
MODE_VOISINAGE = 2


#remainingVisits: typing.List[Visit], vehicleModel: Vehicle, distanceMatrix, timeMatrix,
def buildTours(global_vars: Globals, mode: str = MODE_TOUR) -> typing.Tuple[typing.List[Tour], str]:
    """
    Construit la liste de tours ainsi que la chaîne de caractères affichable.

    :param global_vars: Objet contenant les variables globales :
        liste de visites à effectuer, modèle du véhicule, matrice des distances, matrice des temps
    :param mode: "Glouton" | "Naif" | "Random" (par défaut Glouton)
    :return: Tuple(liste des tours, chaîne de caractères)
    """
    depot = global_vars.list_visits.pop(0)
    v = global_vars.vehicle_model.clone()
    current_tour = Tour([], v, global_vars)
    remaining_visits = current_tour.buildTour(mode, global_vars.list_visits, depot)
    result = [current_tour]
    str_tours = current_tour.str_tour
    while len(remaining_visits) > 0:
        v = global_vars.vehicle_model.clone()
        current_tour = Tour([], v, global_vars)
        remaining_visits = current_tour.buildTour(mode, global_vars.list_visits, depot)
        result.append(current_tour)
        str_tours += "\n" + current_tour.str_tour
    return result, str_tours


#Méthodes pour construire les voisinages
def doVoisinage1(list_tours: typing.List[Tour], tindex: int, v1index: int, v2index: int) \
        -> typing.Union[typing.List[Tour], bool]:
    """
    Echanger deux visites dans un tour.

    :param list_tours: liste des Tour
    :param tindex: l'index du Tour à modifier
    :param v1index, v2index: index des visites à échanger
    :return list_tours modifié (si les tours sont valides), False (si un tour n'est pas valide)
    """
    list_tours[tindex].swapVisits(v1index, v2index)
    return list_tours



def doVoisinage2(list_tours: typing.List[Tour], t1index: int, t2index: int, v1index: int,
                 v2index: int) -> typing.Union[typing.List[Tour], bool]:
    """
    A partir de deux tours T1 et T2 sélectionnés dans une liste de tours,
    retirer une visite de T1 et l'ajouter sur T2.

    :param list_tours: liste des Tour
    :param t1index, t2index: index des Tour à modifier
    :param v1index, v2index: index de départ sur T1 et d'arrivée sur T2
    :return list_tours modifié (si les tours sont valides), False (si un tour n'est pas valide)
    """
    try:
        item = list_tours[t1index].visits.pop(v1index)
    except IndexError:
        return False
    list_tours[t2index].visits.insert(v2index, item)
    #Retirer un tour sur t1Index le rend toujours valide
    return list_tours



def doVoisinage3(list_tours: typing.List[Tour], t1index: int, t2index: int) \
        -> typing.Union[typing.List[Tour], bool]:
    """
    A partir de deux tours T1 et T2 sélectionnés dans une liste de tours,
    prendre le dernier morceau de T1 (toutes les visites après le dernier 'C' ou 'R') et le déplacer sur la fin de T2.

    :param list_tours: liste des Tour
    :param t1index: index du Tour à modifier
    :param t2index:
    :return list_tours modifié (si les tours sont valides), False (si un tour n'est pas valide)
    """
    item_index = list_tours[t1index].findCorRVisits()[-1]
    list_end = list_tours[t1index].visits[item_index:]
    t2_length = len(list_tours[t2index].visits)
    try:
        del list_tours[t1index].visits[item_index:]
        list_tours[t2index].visits.extend(list_end)
        #Retirer un tour sur t1Index le rend toujours valide
        return list_tours
    except IndexError:
        #Défaire les actions
        list_tours[t1index].visits.extend(list_end)
        del list_tours[t2index].visits[t2_length:]
    return False


def doVoisinage4(list_tours: typing.List[Tour], tindex: int, crindex: int = 0, shift: int = 1) \
        -> typing.Union[typing.List[Tour], bool]:
    """
    Déplacer une étape 'C' ou 'R' dans un tour.

    :param list_tours: liste des Tour
    :param tindex: l'index du Tour à modifier
    :param crindex: l'index de l'étape 'C' ou 'R' à retenir
    :param shift: déplacement de l'élement à effectuer (par défaut 1 élement après).
    :return list_tours modifié (si les tours sont valides), False (si un tour n'est pas valide)
    """
    try:
        item_index = list_tours[tindex].findCorRVisits()[crindex]
        item = list_tours[tindex].visits.pop(item_index)
    except IndexError:
        return False
    list_tours[tindex].visits.insert(item_index + shift, item)
    return list_tours



def findBestScore(list_tours: typing.List[Tour], mode_voisinage: int = MODE_VOISINAGE) \
        -> typing.Tuple[typing.List[Tour], float]:
    """
    Choisit un mode de voisinage et tente d'améliorer une solution donnée de list_tours.

    :param list_tours:
    :param mode_voisinage:
    :return:
    """
    #Pour des raisons de performance, appeller isAValidTour() le moins de fois possible ;
    #le sortir des fonctions doVoisinage()
    list_tours_simule = copy.deepcopy(list_tours)
    best_score = sum(tour.calcKilometre() for tour in list_tours_simule) #TODO bug sur best_score quelquefois, augmente par rapport au précédent
    if mode_voisinage == 1:
        tindex = 0
        while tindex < len(list_tours_simule):
            v1index = 0
            while v1index < len(list_tours_simule[tindex].visits):
                v2index = v1index
                while v2index < len(list_tours_simule[tindex].visits):
                    voisin = doVoisinage1(list_tours_simule, tindex, v1index, v2index)
                    if not voisin:
                        v2index += 1
                        continue
                    else:
                        new_score = sum(tour.calcKilometre() for tour in voisin)
                        if new_score < best_score:
                            #Tester la reconstruction du tour
                            if voisin[tindex].isAValidTour():
                                print(f"Voisinage 1 : Found better score for tindex {tindex} v1index {v1index} v2index {v2index}")
                                return voisin, new_score
                    v2index += 1
                v1index += 1
            tindex += 1
        return list_tours_simule, best_score

    elif mode_voisinage == 2:
        t1index = 0
        while t1index < len(list_tours_simule):
            t2index = t1index
            while t2index < len(list_tours_simule):
                v1index = 0
                while v1index < len(list_tours_simule[t1index].visits):
                    v2index = v1index
                    while v2index < len(list_tours_simule[t2index].visits):
                        voisin = doVoisinage2(list_tours_simule, t1index, t2index, v1index, v2index)
                        #list_tours_simule peut remplacer voisin ?
                        if not voisin:
                            v2index += 1
                            continue
                        else:
                            new_score = sum(tour.calcKilometre() for tour in voisin)
                            if new_score < best_score:
                                #Tester la reconstruction du tour :
                                #Attention bien tester les deux tours même si celui de t1 sera toujours valide
                                if voisin[t1index].isAValidTour() and voisin[t2index].isAValidTour():
                                    print(f"Voisinage 2 : Found better score for t1index {t1index} t2index {t2index} v1index {v1index} v2index {v2index}")
                                    return voisin, new_score
                        v2index += 1
                    v1index += 1
                t2index += 1
            t1index += 1
        return list_tours_simule, best_score
    elif mode_voisinage == 3:
        t1index = 0
        while t1index < len(list_tours_simule):
            t2index = t1index
            while t2index < len(list_tours_simule):
                voisin = doVoisinage3(list_tours_simule, t1index, t2index)
                #list_tours_simule peut remplacer voisin ?
                if not voisin:
                    t2index += 1
                    continue
                else:
                    new_score = sum(tour.calcKilometre() for tour in voisin)
                    if new_score < best_score:
                        #Tester la reconstruction du tour
                        #Attention bien tester les deux tours même si celui de t1 sera toujours valide
                        if voisin[t1index].isAValidTour() and voisin[t2index].isAValidTour():
                            print(f"Voisinage 3 : Found better score for t1index {t1index} t2index {t2index}")
                            return voisin, new_score
                t2index += 1
            t1index += 1
        return list_tours_simule, best_score
    elif mode_voisinage == 4:
        tindex = 0
        while tindex < len(list_tours_simule):
            crindex = 0
            while crindex < 10:
                shift = -5
                while shift < 6:
                    voisin = doVoisinage4(list_tours_simule, tindex, crindex, shift)
                    #list_tours_simule peut remplacer voisin ?
                    if not voisin:
                        shift += 1
                        continue
                    else:
                        new_score = sum(tour.calcKilometre() for tour in voisin)
                        if new_score < best_score:
                            #Tester la reconstruction du tour
                            if voisin[tindex].isAValidTour():
                                print(f"Voisinage 4 : Found better score for tindex {tindex} crindex {crindex} shift {shift} ")
                                return voisin, new_score
                    shift += 1
                crindex += 1
            tindex += 1
        return list_tours_simule, best_score
    else:
        raise ValueError("Unknown mode parameter for findBestVoisinage")


def main(the_mode_tour=MODE_TOUR, the_folder=FOLDER, the_mode_voisinage=MODE_VOISINAGE):
    print("Le mode tour choisi est : ", the_mode_tour)
    print("Le dossier choisi est : ", the_folder)
    print("Le mode voisinage choisi est : ", the_mode_voisinage)

    my_globals = Globals()
    my_globals.define(the_folder)

    ### TP1 CONSTRUIRE LES TOURS ###
    (list_tours, the_result) = buildTours(my_globals, mode=the_mode_tour)
    print(the_result)

    ### TP2 CONSTRUIRE LES VOISINAGES ###
    """
    print(list_tours[0].calcKilometre())
    doVoisinage1(list_tours, 0, 3, 4)  #Modifie le list_tours en paramètre comme attendu
    print(list_tours[0].calcKilometre())
    """
    #Trouver le minimum local : On itère findBestScore() jusqu'à ce qu'il ne soit plus possible d'améliorer
    old_score = sum(tour.calcKilometre() for tour in list_tours)
    print("Old score = ", old_score)
    (list_tours, best_score) = findBestScore(list_tours, mode_voisinage=the_mode_voisinage)
    print("New score = ", best_score)
    while best_score < old_score:
        old_score = best_score
        (list_tours, best_score) = findBestScore(list_tours, mode_voisinage=the_mode_voisinage)
        print("New score = ", best_score)
    for tour in list_tours:
        #tour.replayTour(my_globals.distances, my_globals.times)
        print(tour.str_tour)




if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', metavar='path', required=False, default=FOLDER,
                        help='relative path to data folder containing all needed files')
    parser.add_argument('--mode', metavar='name', required=False, default=MODE_TOUR,
                        help='chosen mode to build tours. Values : Glouton | Naif | Random')
    parser.add_argument('--neighbour', metavar='number', required=False, default=MODE_VOISINAGE,
                        help='chosen mode to find neighbours. Values : 1 | 2 | 3 | 4')
    args = parser.parse_args()
    main(the_mode_tour=args.mode, the_folder=args.folder, the_mode_voisinage=args.neighbour)
