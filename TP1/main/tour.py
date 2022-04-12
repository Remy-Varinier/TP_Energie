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

    def buildTours(self, distanceMatrix, timeMatrix) -> typing.List[str]:
        depot = self.visits.pop(0)
        v = self.vehicle.clone()
        the_tour = self.buildTour(v, depot, distanceMatrix, timeMatrix)
        result = [the_tour]
        while len(self.visits) > 0:
            v = self.vehicle.clone()
            the_tour = self.buildTour(v, depot, distanceMatrix, timeMatrix)
            result.append(the_tour)
        return result

    def buildTour(self, vehicle: Vehicle, depot: Visit, distanceMatrix, timeMatrix) -> str:
        currentVisit = depot
        notFull = True
        tourRes = str(currentVisit.visitId)
        currentVehicle = vehicle
        currentVehicle.setCapacity(currentVehicle.capacity)
        while notFull:
            try:
                futurVisit = self.findNearestVisit(currentVisit, distanceMatrix)
                ### TODO Pour plus tard : nearestDepot = findNearestDepot(currentVisit, distanceMatrix)
            except IndexError:
                break  #La liste de visites restantes est vide, on a fini

            distMin = distanceMatrix[currentVisit.visitId][futurVisit.visitId]
            time = timeMatrix[currentVisit.visitId][futurVisit.visitId]

            if not (currentVehicle.canAddTime(time + timeMatrix[futurVisit.visitId][depot.visitId])):
                #La journée du véhicule est finie
                notFull = False
            elif not (currentVehicle.canAddKilometer(distMin + distanceMatrix[futurVisit.visitId][depot.visitId])):
                #Le véhicule ne peut pas effectuer la distance puis retourner au dépôt, il faut le recharger
                currentVehicle.addKilometer(distanceMatrix[currentVisit.visitId][depot.visitId])
                currentVehicle.addTime(timeMatrix[currentVisit.visitId][depot.visitId])
                tourRes += ",R"
                currentVehicle.recharge()  #charge FAST
                currentVisit = depot
            elif not (currentVehicle.canRemoveCapacity(futurVisit.demand)):
                #La destination a une demande trop forte, il faut réapprovisionner le véhicule en allant au dépôt
                currentVehicle.addKilometer(distanceMatrix[currentVisit.visitId][depot.visitId])
                currentVehicle.addTime(timeMatrix[currentVisit.visitId][depot.visitId])
                tourRes += ",C"
                currentVehicle.setCapacity(currentVehicle.capacity)
                currentVisit = depot
            else:
                #On peut effectuer la livraison
                currentVehicle.addKilometer(distMin)
                currentVehicle.addTime(time)
                currentVehicle.removeCapacity(futurVisit.demand)
                tourRes += "," + str(futurVisit.visitId)
                currentVisit = futurVisit
                self.visits.remove(futurVisit)
                if len(self.visits) == 0:
                    notFull = False

        return tourRes

    def findNearestVisit(self, fromVisit: Visit, distanceMatrix) -> Visit:
        distMin = distanceMatrix[fromVisit.visitId][self.visits[0].visitId]  #raises IndexError if listVisit is empty!
        futurVisit = self.visits[0]
        for j in range(0, len(self.visits) - 1):
            tempDist = distanceMatrix[fromVisit.visitId][self.visits[j].visitId]
            if distMin > tempDist:
                futurVisit = self.visits[j]
                distMin = tempDist
        return futurVisit

    def findNearestDepot(self, fromVisit: Visit, distanceMatrix) -> Visit:
        distMin = distanceMatrix[fromVisit.visitId][self.visits[0].visitId]  #raises IndexError if listVisit is empty!
        listDepots = list(filter(lambda x: x.visitName == "Depot", self.visits))
        futurVisit = None
        for j in range(0, len(listDepots) - 1):
            tempDist = distanceMatrix[fromVisit.visitId][listDepots[j].visitId]
            if distMin > tempDist:
                futurVisit = listDepots[j]
                distMin = tempDist
        return futurVisit

    def __str__(self):
        return "TOUR: visits=" + str(self.visits) \
               + " vehicle=" + str(self.vehicle)