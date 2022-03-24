import typing

from vehicle import Vehicle
from visit import Visit

"""TODO plusieurs possibilités :
construire le tour avec une par une visite, check à chaque fois si elle n'est pas déjà faite

"""
class Tour:
    def __init__(self, visits: typing.List[Visit], vehicle: Vehicle):
        self.visits = visits #Liste des visites pour le tour
        self.vehicle = vehicle #Véhicule associé au tour

    def buildTour(self):
        pass

    def calculateTour(self, distances, times):
        i = 0
        j = 1
        kilometer = 0
        duration = 10*60 #10 minutes initiales pour charger le véhicule

        while j < len(self.visits):
            dist = distances[self.visits[i].visitId][self.visits[j].visitId]
            kilometer += dist
            thetime = times[self.visits[i].visitId][self.visits[j].visitId]
            duration += thetime
            duration += self.timeToDeliver(self.visits[j].demand)
            if self.vehicle.addKilometer(dist) == False:
                return -1 #Ce tour est impossible à réaliser car la distance à parcourir entre deux recharges est trop grande
            if self.vehicle.addTime(thetime) == False:
                return -1 #Ce tour est impossible à réaliser car il prend trop de temps sur la journée
            if self.visits[j].visitName == "Depot":
                #Retour au dépôt
                self.vehicle.resetKilometer()
                duration += 10*60
            i += 1
            j += 1

        print("result of tour ="+str(kilometer)+"km et "+str(duration)+"sec")
        return (kilometer, duration)


    def timeToDeliver(self, demand: int):
        return (5*60)+(10*demand)


    def __str__(self):
        return "TOUR: visits="+str(self.visits)\
               +" vehicle="+str(self.vehicle)
