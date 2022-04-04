import typing

from main.vehicle import Vehicle
from main.visit import Visit


class Tour:
    def __init__(self, visits: typing.List[Visit], vehicle: Vehicle):
        self.visits = visits
        self.vehicle = vehicle

    def calcKilometre(self, distance) -> int:
        i = 0
        j = 1
        kilometer = 0
        while j < len(self.visits):
            dist = distance[self.visits[i].visitId][self.visits[j].visitId]
            kilometer += dist
            if self.vehicle.addKilometer(dist) == False:
                return -1
            if self.visits[i].visitName == "Depot":
                self.vehicle.resetKilometer()
            i += 1
            j += 1
        return kilometer


    def swapVisits(self, i, j):
        temp = self.visits[i]
        self.visits[i] = self.visits[j]
        self.visits[j] = temp

    def findCorRVisits(self, findC: bool=True, findR: bool=True) -> typing.List[int]:
        res = []
        for i in range(len(self.visits)):
            if (self.visits[i].visitName == 'C' and findC) or (self.visits[i].visitName == 'R' and findR):
                res.append(i)
        return res



    def __str__(self):
        return "TOUR: visits=" + str(self.visits) \
               + " vehicle=" + str(self.vehicle)