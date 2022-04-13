import random
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

    def isAValidTour(self, vehicleModel: Vehicle, distanceMatrix, timeMatrix) -> bool:
        try:
            if len(self.visits) == 0:
                return True
            currentVisit = self.visits[0]
            for futurVisit in self.visits[1:]:
                dist = distanceMatrix[currentVisit.visitId][futurVisit.visitId]
                time = timeMatrix[currentVisit.visitId][futurVisit.visitId]
                vehicleModel.addKilometer(dist)
                vehicleModel.addTime(time)
                if futurVisit.visitName == "C":
                    vehicleModel.setCapacity(self.vehicle.capacity)
                elif futurVisit.visitName == "R":
                    vehicleModel.recharge()
                else:
                    vehicleModel.removeCapacity(futurVisit.demand)
                currentVisit = futurVisit

            return True
        except (IndexError, ValueError):
            return False

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

    def buildTour(self, mode: str, remainingVisits: typing.List[Visit], depot: Visit, distanceMatrix, timeMatrix)\
        -> typing.Tuple[typing.List[Visit], str]:
        if mode == "Naif":
            return self.buildTourNaif(remainingVisits, depot, distanceMatrix, timeMatrix)
        elif mode == "Random":
            return self.buildTourRandom(remainingVisits, depot, distanceMatrix, timeMatrix)
        elif mode == "Optimal":
            return self.buildTourOptimal(remainingVisits, depot, distanceMatrix, timeMatrix)
        else:
            raise ValueError("Unknown mode for buildTour")

    def buildTourNaif(self, remainingVisits: typing.List[Visit], depot: Visit, distanceMatrix, timeMatrix)\
        -> typing.Tuple[typing.List[Visit], str]:
        currentVisit = depot
        notFull = True
        str_tour = str(currentVisit.visitId)
        self.vehicle.setCapacity(self.vehicle.capacity)
        while (len(remainingVisits) > 0 and notFull):
            futurVisit = remainingVisits[0]
            dist = distanceMatrix[currentVisit.visitId][futurVisit.visitId]
            time = timeMatrix[currentVisit.visitId][futurVisit.visitId]

            if not (self.vehicle.canAddTime(time + timeMatrix[futurVisit.visitId][depot.visitId])):
                #La journée du véhicule est finie
                notFull = False
            elif not (self.vehicle.canAddKilometer(dist + distanceMatrix[futurVisit.visitId][depot.visitId])):
                #Le véhicule ne peut pas effectuer la distance puis retourner au dépôt, il faut le recharger
                self.vehicle.addKilometer(distanceMatrix[currentVisit.visitId][depot.visitId])
                self.vehicle.addTime(timeMatrix[currentVisit.visitId][depot.visitId])
                str_tour += ",R"
                visitToAdd = depot.clone()
                visitToAdd.visitName = "R"
                self.visits.append(visitToAdd)
                self.vehicle.recharge()  #charge FAST
                currentVisit = depot
            elif not (self.vehicle.canRemoveCapacity(futurVisit.demand)):
                #La destination a une demande trop forte, il faut réapprovisionner le véhicule en allant au dépôt
                self.vehicle.addKilometer(distanceMatrix[currentVisit.visitId][depot.visitId])
                self.vehicle.addTime(timeMatrix[currentVisit.visitId][depot.visitId])
                str_tour += ",C"
                visitToAdd = depot.clone()
                visitToAdd.visitName = "C"
                self.visits.append(visitToAdd)
                self.vehicle.setCapacity(self.vehicle.capacity)
                currentVisit = depot
            else:
                #On peut effectuer la livraison
                self.vehicle.addKilometer(dist)
                self.vehicle.addTime(time)
                self.vehicle.removeCapacity(futurVisit.demand)
                str_tour += "," + str(futurVisit.visitId)
                currentVisit = futurVisit
                remainingVisits.pop(0)
                self.visits.append(futurVisit)
                if len(remainingVisits) == 0:
                    notFull = False

        return (remainingVisits, str_tour)


    def buildTourRandom(self, remainingVisits: typing.List[Visit], depot: Visit, distanceMatrix, timeMatrix)\
        -> typing.Tuple[typing.List[Visit], str]:
        currentVisit = depot
        notFull = True
        str_tour = str(currentVisit.visitId)
        self.vehicle.setCapacity(self.vehicle.capacity)
        while (len(remainingVisits) > 0 and notFull):
            futurVisit = remainingVisits[random.randint(0, len(remainingVisits)-1)]
            dist = distanceMatrix[currentVisit.visitId][futurVisit.visitId]
            time = timeMatrix[currentVisit.visitId][futurVisit.visitId]

            if not (self.vehicle.canAddTime(time + timeMatrix[futurVisit.visitId][depot.visitId])):
                #La journée du véhicule est finie
                notFull = False
            elif not (self.vehicle.canAddKilometer(dist + distanceMatrix[futurVisit.visitId][depot.visitId])):
                #Le véhicule ne peut pas effectuer la distance puis retourner au dépôt, il faut le recharger
                self.vehicle.addKilometer(distanceMatrix[currentVisit.visitId][depot.visitId])
                self.vehicle.addTime(timeMatrix[currentVisit.visitId][depot.visitId])
                str_tour += ",R"
                visitToAdd = depot.clone()
                visitToAdd.visitName = "R"
                self.visits.append(visitToAdd)
                self.vehicle.recharge()  #charge FAST
                currentVisit = depot
            elif not (self.vehicle.canRemoveCapacity(futurVisit.demand)):
                #La destination a une demande trop forte, il faut réapprovisionner le véhicule en allant au dépôt
                self.vehicle.addKilometer(distanceMatrix[currentVisit.visitId][depot.visitId])
                self.vehicle.addTime(timeMatrix[currentVisit.visitId][depot.visitId])
                str_tour += ",C"
                visitToAdd = depot.clone()
                visitToAdd.visitName = "C"
                self.visits.append(visitToAdd)
                self.vehicle.setCapacity(self.vehicle.capacity)
                currentVisit = depot
            else:
                #On peut effectuer la livraison
                self.vehicle.addKilometer(dist)
                self.vehicle.addTime(time)
                self.vehicle.removeCapacity(futurVisit.demand)
                str_tour += "," + str(futurVisit.visitId)
                currentVisit = futurVisit
                remainingVisits.remove(futurVisit)
                self.visits.append(futurVisit)
                if len(remainingVisits) == 0:
                    notFull = False

        return (remainingVisits, str_tour)

    def buildTourOptimal(self, remainingVisits: typing.List[Visit], depot: Visit, distanceMatrix, timeMatrix)\
        -> typing.Tuple[typing.List[Visit], str]:
        currentVisit = depot
        notFull = True
        str_tour = str(currentVisit.visitId)
        self.vehicle.setCapacity(self.vehicle.capacity)
        while notFull:
            try:
                futurVisit = findNearestVisit(remainingVisits, currentVisit, distanceMatrix)
                ### TODO Pour plus tard : nearestDepot = findNearestDepot(currentVisit, distanceMatrix)
            except IndexError:
                break  #La liste de visites restantes est vide, on a fini

            distMin = distanceMatrix[currentVisit.visitId][futurVisit.visitId]
            time = timeMatrix[currentVisit.visitId][futurVisit.visitId]

            if not (self.vehicle.canAddTime(time + timeMatrix[futurVisit.visitId][depot.visitId])):
                #La journée du véhicule est finie
                notFull = False
            elif not (self.vehicle.canAddKilometer(distMin + distanceMatrix[futurVisit.visitId][depot.visitId])):
                #Le véhicule ne peut pas effectuer la distance puis retourner au dépôt, il faut le recharger
                self.vehicle.addKilometer(distanceMatrix[currentVisit.visitId][depot.visitId])
                self.vehicle.addTime(timeMatrix[currentVisit.visitId][depot.visitId])
                str_tour += ",R"
                visitToAdd = depot.clone()
                visitToAdd.visitName = "R"
                self.visits.append(visitToAdd)
                self.vehicle.recharge()  #charge FAST
                currentVisit = depot
            elif not (self.vehicle.canRemoveCapacity(futurVisit.demand)):
                #La destination a une demande trop forte, il faut réapprovisionner le véhicule en allant au dépôt
                self.vehicle.addKilometer(distanceMatrix[currentVisit.visitId][depot.visitId])
                self.vehicle.addTime(timeMatrix[currentVisit.visitId][depot.visitId])
                str_tour += ",C"
                visitToAdd = depot.clone()
                visitToAdd.visitName = "C"
                self.visits.append(visitToAdd)
                self.vehicle.setCapacity(self.vehicle.capacity)
                currentVisit = depot
            else:
                #On peut effectuer la livraison
                self.vehicle.addKilometer(distMin)
                self.vehicle.addTime(time)
                self.vehicle.removeCapacity(futurVisit.demand)
                str_tour += "," + str(futurVisit.visitId)
                currentVisit = futurVisit
                remainingVisits.remove(futurVisit)
                self.visits.append(futurVisit)
                if len(remainingVisits) == 0:
                    notFull = False

        return (remainingVisits, str_tour)

    def __str__(self):
        return "TOUR: visits=" + str(self.visits) \
               + " vehicle=" + str(self.vehicle)


def findNearestVisit(listVisit: typing.List[Visit], fromVisit: Visit, distanceMatrix) -> Visit:
    distMin = distanceMatrix[fromVisit.visitId][listVisit[0].visitId]  #raises IndexError if listVisit is empty!
    futurVisit = listVisit[0]
    for j in range(0, len(listVisit) - 1):
        tempDist = distanceMatrix[fromVisit.visitId][listVisit[j].visitId]
        if distMin > tempDist:
            futurVisit = listVisit[j]
            distMin = tempDist
    return futurVisit

def findNearestDepot(listVisit: typing.List[Visit], fromVisit: Visit, distanceMatrix) -> Visit:
    listDepots = list(filter(lambda x: x.visitName == "Depot", listVisit))
    distMin = distanceMatrix[fromVisit.visitId][listDepots[0].visitId]  #raises IndexError if listDepots is empty!
    futurVisit = None
    for j in range(0, len(listDepots) - 1):
        tempDist = distanceMatrix[fromVisit.visitId][listDepots[j].visitId]
        if distMin > tempDist:
            futurVisit = listDepots[j]
            distMin = tempDist
    return futurVisit