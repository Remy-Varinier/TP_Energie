# /usr/bin/python3
from tempfile import tempdir
import numpy as np
import csv
from configparser import ConfigParser
from main.tour import Tour
from main.visit import Visit

from main.vehicle import Vehicle

folder = "Data/lyon_40_1_1/"
with open(folder+'visits.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    listVisits: list[Visit] = []
    for row in reader:
        listVisits.append(Visit(int(row['visit_id']), row['visit_name'],
                          row['visit_lat'], row['visit_lon'], row['demand']))


config = ConfigParser()
config.read(folder+"vehicle.ini")

distance = np.loadtxt(folder+"distances.txt")
times = np.loadtxt(folder+"times.txt")


def getIntFromIni(value: str):
    return config.getint("Vehicle", value)


def getStrFromIni(value: str):
    return config.get("Vehicle", value)


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


def defineTours(allVisits: list[Visit], vehicle: Vehicle, distance) -> list[Tour]:
    depot = allVisits.pop(0)
    actualVisit = depot
    notFull = True
    v = vehicle.clone()
    t = buildTour(allVisits, v, depot)
    while len(allVisits) > 0:
        v = vehicle.clone()
        t: tuple = buildTour(t[0], v, depot)
        return None


def buildTour(listVist: list[Visit], vehicle: Vehicle, depot: Visit) -> tuple(list[Visit], Tour):
    actualVisit = depot
    notFull = True
    while notFull == True:
        visits = []
        distMin = distance[actualVisit.visitId][listVist[j].visitId]
        tempDist = -1
        futurVistit: Visit = None
        for j in range(0, len(listVist)):
            tempDist = distance[actualVisit.visitId][listVist[j].visitId]
            if distMin > tempDist:
                futurVisit = listVist[j]
                distMin = tempDist
        if vehicle.addKilometer(distMin + distance[futurVisit.visitId][depot.visitId]) == False:
            notFull = False
        visits.append(futurVisit)
        vehicle.removeCharge(futurVisit.demand)
    return (visits, Tour(visits, vehicle))
