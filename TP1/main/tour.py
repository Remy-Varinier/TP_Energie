from main.vehicle import Vehicle
from main.visit import Visit


class Tour:
    def __init__(self, visits: list[Visit], vehicle: Vehicle):
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
