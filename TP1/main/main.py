# /usr/bin/python3
import numpy as np
import csv
import typing
from configparser import ConfigParser

from tour import Tour
from visit import Visit
from vehicle import Vehicle

folder = "../Data/lyon_40_1_1/"
with open(folder+'visits.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    listVisits: typing.List[Visit] = []
    for row in reader:
        listVisits.append(Visit(int(row['visit_id']),
                                row['visit_name'],
                                float(row['visit_lat']),
                                float(row['visit_lon']),
                                int(row['demand'])))


config = ConfigParser()
config.read(folder+"vehicle.ini")

distances = np.loadtxt(folder+"distances.txt")
times = np.loadtxt(folder+"times.txt")


def getIntFromIni(value: str):
    return config.getint("Vehicle", value)


def getStrFromIni(value: str):
    return config.get("Vehicle", value)


for v in listVisits :
    print(str(v))


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
tourVisits.append(listVisits[3])
tourVisits.append(listVisits[4])
tourVisits.append(listVisits[0])

tour = Tour(tourVisits, vroom)
print(tour.calculateTour(distances, times))


def defineTour():
    return
