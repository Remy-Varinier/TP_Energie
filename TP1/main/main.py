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

distance = np.loadtxt(folder+"distances.txt")
times = np.loadtxt(folder+"times.txt")


def getIntFromIni(value: str):
    return config.getint("Vehicle", value)


def getStrFromIni(value: str):
    return config.get("Vehicle", value)


vroom = Vehicle(
    600,
    getIntFromIni("capacity"),
    getIntFromIni("charge_fast"),
    getIntFromIni("charge_medium"),
    getIntFromIni("charge_slow"),
    getStrFromIni("start_time"),
    getStrFromIni("end_time")
)
tourVisits = []
tourVisits.append(listVisits[0])
tourVisits.append(listVisits[1])
tourVisits.append(listVisits[0])
tourVisits.append(listVisits[1])
#tour = Tour(tourVisits, vroom)
# print(tour.calcKilometre(distance))


def buildTours(allVisits: list[Visit], vehicle: Vehicle, distance) -> list[Tour]:
    depot = allVisits.pop(0)
    v = vehicle.clone()
    t = buildTour(allVisits, v, depot, distance)
    result = []
    result.append(str(t[0]))
    result = []
    while len(t[0]) > 0:
        v = vehicle.clone()
        t: tuple = buildTour(t[0], v, depot, distance)
        result.append(str(t[1]))
    return result


def buildTour(listVist: typing.List[Visit], vehicle: Vehicle, depot: Visit) -> typing.Tuple[typing.List[Visit], Tour]:
    actualVisit = depot
    notFull = True
    visits = []
    visits.append(actualVisit)
    while notFull == True:
        visits = []
        futurVisit: Visit = findNearVisit(listVist, actualVisit, distance)
        distMin = distance[actualVisit.visitId][futurVisit.visitId]

        time = times[actualVisit.visitId][futurVisit.visitId]
        if vehicle.canAddKilometer(distMin + distance[futurVisit.visitId][depot.visitId]) == False & vehicle.canAddTime(time + times[futurVisit.visitId][depot.visitId]) == False:
            notFull = False
        else:
            vehicle.addKilometer(distMin)
            vehicle.addTime(time)
            visits.append(futurVisit)
            vehicle.removeCharge(futurVisit.demand)
            listVisits.remove(futurVisit)
            if len(listVisits) == 0:
                notFull = False
    return (listVisits, Tour(visits, vehicle))


def findNearVisit(listVisit: list[Visit], visit: Visit, distance) -> Visit:
    distMin = distance[visit.visitId][listVisit[0].visitId]
    tempDist = -1
    futurVisit = listVisit[0]
    for j in range(0, len(listVisit)-1):
        tempDist = distance[visit.visitId][listVisit[j].visitId]
        if distMin > tempDist:
            futurVisit = listVisit[j]
            distMin = tempDist
    return futurVisit


print(buildTours(listVisits, vroom, distance))


def findVoisinage1(listTours: typing.List[Tour], tIndex: int, v1Index: int, v2Index: int):
    """Echange de deux visites dans un même tour.

    :param listTours: liste des Tour
    :param tIndex: l'index du Tour à modifier
    :param v1Index, v2Index: index des visites à échanger
    """
    try:
        listTours[tIndex].swapVisits(v1Index, v2Index)
    except IndexError:
        "Voisinage impossible"


def findVoisinage2(listTours: typing.List[Tour], t1Index: int, t2Index: int, v1Index: int, v2Index: int):
    """Retirer une visite de T1 et l'ajouter sur T2.

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
    """Prendre le dernier morceau d'un tour donné (toutes les visites après le dernier 'C' ou 'R') et le déplacer sur un autre tour.

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
    :param shift: déplacement de l'élement à effectuer.
    """
    try:
        itemIndex = listTours[tIndex].findCorRVisits()[crIndex]
        item = listTours[tIndex].visits.pop(itemIndex)
        listTours[tIndex].visits.insert(itemIndex + shift, item)
    except IndexError:
        "Voisinage impossible"


vroom = Vehicle(
    6,
    getIntFromIni("capacity"),
    getIntFromIni("charge_fast"),
    getIntFromIni("charge_medium"),
    getIntFromIni("charge_slow"),
    getStrFromIni("start_time"),
    getStrFromIni("end_time")
)
tourVisits = []
tourVisits.append(listVisits[0])
tourVisits.append(listVisits[1])
tourVisits.append(listVisits[0])
tourVisits.append(listVisits[1])
tour = Tour(tourVisits, vroom)
print(tour.calcKilometre(distance))