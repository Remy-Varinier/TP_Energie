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


def buildTours(allVisits: typing.List[Visit], vehicle: Vehicle, distance) -> typing.List[str]:
    depot = allVisits.pop(0)
    v = vehicle.clone()
    (the_visits, the_tour) = buildTour(allVisits, v, depot, distance)
    result = [the_tour]
    while len(the_visits) > 0:
        v = vehicle.clone()
        (the_visits, the_tour) = buildTour(the_visits, v, depot, distance)
        result.append(the_tour)
    return result


def buildTour(listVisit: typing.List[Visit], vehicle: Vehicle, depot: Visit, distance) -> typing.Tuple[typing.List[Visit], str]:
    currentVisit = depot
    notFull = True
    tourRes = str(currentVisit.visitId)
    vehicle.setCapacity(vehicle.capacity)
    while notFull:
        try:
            futurVisit = findNearestVisit(listVisit, currentVisit, distance)
            ### Pour plus tard : nearestDepot = findNearestDepot(listVisit, actualVisit, distances)
        except IndexError:
            break #La liste de visites restantes est vide, on a fini

        distMin = distance[currentVisit.visitId][futurVisit.visitId]
        time = times[currentVisit.visitId][futurVisit.visitId]

        if not(vehicle.canAddTime(time + times[futurVisit.visitId][depot.visitId])):
            #La journée du véhicule est finie
            notFull = False
        elif not(vehicle.canAddKilometer(distMin + distance[futurVisit.visitId][depot.visitId])):
            #Le véhicule ne peut pas effectuer la distance puis retourner au dépôt, il faut le recharger
            vehicle.addKilometer(distance[currentVisit.visitId][depot.visitId])
            vehicle.addTime(times[currentVisit.visitId][depot.visitId])
            tourRes += ",R"
            vehicle.recharge() #charge FAST
            currentVisit = depot
        elif not(vehicle.canRemoveCapacity(futurVisit.demand)):
            #La destination a une demande trop forte, il faut réapprovisionner le véhicule en allant au dépôt
            vehicle.addKilometer(distance[currentVisit.visitId][depot.visitId])
            vehicle.addTime(times[currentVisit.visitId][depot.visitId])
            tourRes += ",C"
            vehicle.setCapacity(vehicle.capacity)
            currentVisit = depot
        else:
            #On peut effectuer la livraison
            vehicle.addKilometer(distMin)
            vehicle.addTime(time)
            vehicle.removeCapacity(futurVisit.demand)
            tourRes += ","+str(futurVisit.visitId)
            currentVisit = futurVisit
            listVisit.remove(futurVisit)
            if len(listVisit) == 0:
                notFull = False

    return (listVisit, tourRes)


def findNearestVisit(listVisit: typing.List[Visit], fromVisit: Visit, distance) -> Visit:
    distMin = distance[fromVisit.visitId][listVisit[0].visitId] #raises IndexError if listVisit is empty!
    futurVisit = listVisit[0]
    for j in range(0, len(listVisit)-1):
        tempDist = distance[fromVisit.visitId][listVisit[j].visitId]
        if distMin > tempDist:
            futurVisit = listVisit[j]
            distMin = tempDist
    return futurVisit

def findNearestDepot(listVisit: typing.List[Visit], fromVisit: Visit, distance) -> Visit:
    distMin = distance[fromVisit.visitId][listVisit[0].visitId]  #raises IndexError if listVisit is empty!
    listDepots = list(filter(lambda x: x.visitName == "Depot", listVisit))
    futurVisit = None
    for j in range(0, len(listDepots) - 1):
        tempDist = distance[fromVisit.visitId][listDepots[j].visitId]
        if distMin > tempDist:
            futurVisit = listDepots[j]
            distMin = tempDist
    return futurVisit




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
the_result = buildTours(listVisits, vroom, distances)
for r in the_result:
    print(r)


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

