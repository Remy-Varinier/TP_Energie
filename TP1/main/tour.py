import random
import typing

from vehicle import Vehicle
from visit import Visit


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
        """
        Fonction de contrôle d'un Tour valide.
        Rejoue simplement le trajet et vérifie qu'il n'y a pas d'exceptions levées.

        :param vehicleModel: modèle de Vehicle
        :param distanceMatrix: matrice des distances
        :param timeMatrix: matrice des temps
        :return: bool
        """
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
        """
        Echange les objets indiqués aux index i et j dans la liste de visites.

        :param i: index 1
        :param j: index 2
        """
        temp = self.visits[i]
        self.visits[i] = self.visits[j]
        self.visits[j] = temp

    def findCorRVisits(self, findC: bool=True, findR: bool=True) -> typing.List[int]:
        """
        Recherche les étapes 'C' ou 'R' dans la liste de visites et renvoie la liste des index trouvés.

        :param findC: Sélectionner les étapes 'C' (par défaut True)
        :param findR: Sélectionner les étapes 'R' (par défaut True)
        :return: list(int)
        """
        res = []
        for i in range(len(self.visits)):
            if (self.visits[i].visitName == 'C' and findC) or (self.visits[i].visitName == 'R' and findR):
                res.append(i)
        return res

    def buildTour(self, mode: str, remainingVisits: typing.List[Visit], depot: Visit, distanceMatrix, timeMatrix)\
        -> typing.Tuple[typing.List[Visit], str]:
        """
        Fonction pour choisir le mode de construction d'un Tour.

        :raises ValueError : Le mode spécifié est inconnu
        """
        if mode == "Naif":
            return self.buildTourNaif(remainingVisits, depot, distanceMatrix, timeMatrix)
        elif mode == "Random":
            return self.buildTourRandom(remainingVisits, depot, distanceMatrix, timeMatrix)
        elif mode == "Glouton":
            return self.buildTourGlouton(remainingVisits, depot, distanceMatrix, timeMatrix)
        else:
            raise ValueError("Unknown mode for buildTour")

    def buildTourNaif(self, remainingVisits: typing.List[Visit], depot: Visit, distanceMatrix, timeMatrix)\
        -> typing.Tuple[typing.List[Visit], str]:
        """
        Construire un Tour en mode Naïf : On prend simplement la liste de visites dans l'ordre.

        :param remainingVisits:
        :param depot:
        :param distanceMatrix:
        :param timeMatrix:
        :return: Tuple(visites restantes, chaîne de caractères)
        """
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
        """
        Construire un Tour en mode Random : Sélectionne une visite aléatoire dans la liste à chaque fois.
        Cette méthode est NON-DETERMINISTE !

        :param remainingVisits:
        :param depot:
        :param distanceMatrix:
        :param timeMatrix:
        :return: Tuple(visites restantes, chaîne de caractères)
        """
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

    def buildTourGlouton(self, remainingVisits: typing.List[Visit], depot: Visit, distanceMatrix, timeMatrix)\
        -> typing.Tuple[typing.List[Visit], str]:
        """
        Construit un Tour en mode Glouton : Recherche la visite la plus proche dans la liste à chaque fois.

        :param remainingVisits:
        :param depot:
        :param distanceMatrix:
        :param timeMatrix:
        :return: Tuple(visites restantes, chaîne de caractères)
        """
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

    def __repr__(self):
        return "TOUR: visits=" + repr(self.visits) \
               + "\n vehicle=" + repr(self.vehicle) \
               + "\n"


def findNearestVisit(listVisit: typing.List[Visit], fromVisit: Visit, distanceMatrix) -> Visit:
    """
    A partir d'une liste de Visit, retourne la Visit ayant la distance la plus faible
    avec une Visit de départ spécifiée.

    :param listVisit:
    :param fromVisit:
    :param distanceMatrix:
    :return: Visit
    """
    distMin = distanceMatrix[fromVisit.visitId][listVisit[0].visitId]  #raises IndexError if listVisit is empty!
    futurVisit = listVisit[0]
    for j in range(0, len(listVisit) - 1):
        tempDist = distanceMatrix[fromVisit.visitId][listVisit[j].visitId]
        if distMin > tempDist:
            futurVisit = listVisit[j]
            distMin = tempDist
    return futurVisit

def findNearestDepot(listVisit: typing.List[Visit], fromVisit: Visit, distanceMatrix) -> Visit:
    """
    A partir d'une liste de Visit, retourne la Visit de type "Dépôt" ayant la distance la plus faible
    avec une Visit de départ spécifiée.

    :param listVisit:
    :param fromVisit:
    :param distanceMatrix:
    :return: Visit
    """
    listDepots = list(filter(lambda x: x.visitName == "Depot", listVisit))
    return findNearestVisit(listDepots, fromVisit, distanceMatrix)