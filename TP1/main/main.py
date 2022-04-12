# /usr/bin/python3
import numpy as np
import csv
import typing

from configparser import ConfigParser
from main.tour import Tour
from main.visit import Visit

from main.vehicle import Vehicle

folder = "Data/lyon_40_1_1/"
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
tournoi = Tour(listVisits, vroom)
the_result = tournoi.buildTours(distances, times)
for r in the_result:
    print(r)

### TP2 CONSTRUIRE LES VOISINAGES ###
def findVoisinage1(listTours: typing.List[Tour], tIndex: int, v1Index: int, v2Index: int):
    """Echanger deux visites dans un tour.

    :param listTours: liste des Tour
    :param tIndex: l'index du Tour à modifier
    :param v1Index, v2Index: index des visites à échanger
    """
    try:
        listTours[tIndex].swapVisits(v1Index, v2Index)
    except IndexError:
        "Voisinage impossible"


def findVoisinage2(listTours: typing.List[Tour], t1Index: int, t2Index: int, v1Index: int, v2Index: int):
    """A partir de deux tours T1 et T2 sélectionnés dans une liste de tours,
    retirer une visite de T1 et l'ajouter sur T2.

    :param listTours: liste des Tour
    :param t1Index, t2Index: index des Tour à modifier
    :param v1Index, v2Index: index de départ sur T1 et d'arrivée sur T2
    """
    try:
        item = listTours[t1Index].visits.pop(v1Index)
        listTours[t2Index].visits.insert(v2Index, item)
    except IndexError:
        "Voisinage impossible"


def findVoisinage3(listTours: typing.List[Tour], t1Index: int, t2Index: int):
    """A partir de deux tours T1 et T2 sélectionnés dans une liste de tours,
    prendre le dernier morceau de T1 (toutes les visites après le dernier 'C' ou 'R') et le déplacer sur la fin de T2.

    :param listTours: liste des Tour
    :param t1Index: index du Tour à modifier
    :param t2Index:
    """
    try:
        itemIndex = listTours[t1Index].findCorRVisits()[-1]
        listEnd = listTours[t1Index].visits[itemIndex:]
        del listTours[t1Index].visits[itemIndex:]
        listTours[t2Index].visits.extend(listEnd)
    except IndexError:
        "Voisinage impossible"


def findVoisinage4(listTours: typing.List[Tour], tIndex: int, crIndex: int=0, shift: int=1):
    """Déplacer une étape 'C' ou 'R' dans un tour.

    :param listTours: liste des Tour
    :param tIndex: l'index du Tour à modifier
    :param crIndex: l'index de l'étape 'C' ou 'R' à retenir
    :param shift: déplacement de l'élement à effectuer (par défaut 1 élement après).
    """
    try:
        itemIndex = listTours[tIndex].findCorRVisits()[crIndex]
        item = listTours[tIndex].visits.pop(itemIndex)
        listTours[tIndex].visits.insert(itemIndex + shift, item)
    except IndexError:
        "Voisinage impossible"

