import csv
import numpy as np
from configparser import ConfigParser

from vehicle import Vehicle
from visit import Visit


class Globals:

    def __init__(self):
        self.listVisits = []
        self.distances = None
        self.times = None
        self.vehicleModel = None
        self.config = ConfigParser()

    def define(self, folder):
        with open(folder + 'visits.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.listVisits.append(Visit(int(row['visit_id']), row['visit_name'],
                                        row['visit_lat'], row['visit_lon'], int(row['demand'])))

        self.distances = np.loadtxt(folder + "distances.txt")
        self.times = np.loadtxt(folder + "times.txt")
        self.config.read(folder + "vehicle.ini")
        self.vehicleModel = Vehicle(
            600,
            self.getIntFromIni("capacity"),
            self.getIntFromIni("charge_fast"),
            self.getIntFromIni("charge_medium"),
            self.getIntFromIni("charge_slow"),
            self.getStrFromIni("start_time"),
            self.getStrFromIni("end_time")
        )

    def getIntFromIni(self, value: str):
        return self.config.getint("Vehicle", value)

    def getStrFromIni(self, value: str):
        return self.config.get("Vehicle", value)