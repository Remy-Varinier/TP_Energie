# /usr/bin/python3
import numpy as np
import csv
import typing

from configparser import ConfigParser
from main.tour import Tour
from main.visit import Visit

from main.vehicle import Vehicle

folder = "Data/lyon_150_1_1/"
with open(folder+'visits.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    listVisits: typing.List[Visit] = []
    for row in reader:
        listVisits.append(Visit(int(row['visit_id']), row['visit_name'],
                          row['visit_lat'], row['visit_lon'], int(row['demand'])))


config = ConfigParser()
config.read(folder+"vehicle.ini")

distances = np.loadtxt(folder + "distances.txt")
times = np.loadtxt(folder+"times.txt")


def getIntFromIni(value: str):
    return config.getint("Vehicle", value)


def getStrFromIni(value: str):
    return config.get("Vehicle", value)

def buildTours(remainingVisits: typing.List[Visit], vehicleModel: Vehicle, distanceMatrix, timeMatrix,
               mode: str="Optimal") -> typing.Tuple[typing.List[Tour], str]:
    depot = remainingVisits.pop(0)
    v = vehicleModel.clone()
    current_tour = Tour([], v)
    (remainingVisits, str_tour) = current_tour.buildTour(mode, remainingVisits, depot, distanceMatrix, timeMatrix)
    result = [current_tour]
    str_tours = str_tour
    while len(remainingVisits) > 0:
        v = vehicleModel.clone()
        current_tour = Tour([], v)
        (remainingVisits, str_tour) = current_tour.buildTour(mode, remainingVisits, depot, distanceMatrix, timeMatrix)
        result.append(current_tour)
        str_tours += "\n"+str_tour
    return (result, str_tours)


### TP1 CONSTRUIRE LES TOURS ###
vroom = Vehicle(
    600,
    getIntFromIni("capacity"),
    getIntFromIni("charge_fast"),
    getIntFromIni("charge_medium"),
    getIntFromIni("charge_slow"),
    getStrFromIni("start_time"),
    getStrFromIni("end_time")
)
(listTours, the_result) = buildTours(listVisits, vroom, distances, times, mode="Random")
print(the_result)


### TP2 CONSTRUIRE LES VOISINAGES ###
def findVoisinage1(listTours: typing.List[Tour], tIndex: int, v1Index: int, v2Index: int) -> bool:
    """Echanger deux visites dans un tour.

    :param listTours: liste des Tour
    :param tIndex: l'index du Tour à modifier
    :param v1Index, v2Index: index des visites à échanger
    """
    global vroom
    global distances
    global times
    try:
        listTours[tIndex].swapVisits(v1Index, v2Index)
        return listTours[tIndex].isAValidTour(vroom, distances, times)
    except IndexError:
        return False


def findVoisinage2(listTours: typing.List[Tour], t1Index: int, t2Index: int, v1Index: int, v2Index: int) -> bool:
    """A partir de deux tours T1 et T2 sélectionnés dans une liste de tours,
    retirer une visite de T1 et l'ajouter sur T2.

    :param listTours: liste des Tour
    :param t1Index, t2Index: index des Tour à modifier
    :param v1Index, v2Index: index de départ sur T1 et d'arrivée sur T2
    """
    global vroom
    global distances
    global times
    try:
        item = listTours[t1Index].visits.pop(v1Index)
        listTours[t2Index].visits.insert(v2Index, item)
        #Retirer un tour sur t1Index le rend toujours valide
        return listTours[t2Index].isAValidTour(vroom, distances, times)
    except IndexError:
        return False


def findVoisinage3(listTours: typing.List[Tour], t1Index: int, t2Index: int) -> bool:
    """A partir de deux tours T1 et T2 sélectionnés dans une liste de tours,
    prendre le dernier morceau de T1 (toutes les visites après le dernier 'C' ou 'R') et le déplacer sur la fin de T2.

    :param listTours: liste des Tour
    :param t1Index: index du Tour à modifier
    :param t2Index:
    """
    global vroom
    global distances
    global times
    try:
        itemIndex = listTours[t1Index].findCorRVisits()[-1]
        listEnd = listTours[t1Index].visits[itemIndex:]
        del listTours[t1Index].visits[itemIndex:]
        listTours[t2Index].visits.extend(listEnd)
        #Retirer un tour sur t1Index le rend toujours valide
        return listTours[t2Index].isAValidTour(vroom, distances, times)
    except IndexError:
        return False


def findVoisinage4(listTours: typing.List[Tour], tIndex: int, crIndex: int=0, shift: int=1) -> bool:
    """Déplacer une étape 'C' ou 'R' dans un tour.

    :param listTours: liste des Tour
    :param tIndex: l'index du Tour à modifier
    :param crIndex: l'index de l'étape 'C' ou 'R' à retenir
    :param shift: déplacement de l'élement à effectuer (par défaut 1 élement après).
    """
    global vroom
    global distances
    global times
    try:
        itemIndex = listTours[tIndex].findCorRVisits()[crIndex]
        item = listTours[tIndex].visits.pop(itemIndex)
        listTours[tIndex].visits.insert(itemIndex + shift, item)
        return listTours[tIndex].isAValidTour(vroom, distances, times)
    except IndexError:
        return False

