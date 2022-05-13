import random
import typing

from vehicle import Vehicle
from visit import Visit


#TODO comment gérer les exceptions renvoyés par replayTour() ??

class Tour:
    def __init__(self, visits: typing.List[Visit], vehicle: Vehicle):
        self.visits = visits  #Liste des objets Visit contenus dans ce tour
        self.vehicle = vehicle  #Véhicule parcourant ce tour
        self.str_tour = ""  #Représentation du tour en chaîne de caractères affichable

    def calcKilometre(self, distance) -> int:
        i = 0
        j = 1
        kilometer = 0
        while j < len(self.visits):
            dist = distance[self.visits[i].visit_id][self.visits[j].visit_id]
            kilometer += dist
            if not self.vehicle.canAddKilometer(dist):
                return -1
            if self.visits[i].visit_name == "Depot":
                self.vehicle.resetKilometer()
            i += 1
            j += 1
        return kilometer

    def addToVisits(self, new_visit: Visit, distance_matrix, time_matrix,
                    depot=None) -> bool:  #returns True if visit could be added

        if depot is None:
            depot = self.visits[0]
        current_visit = self.visits[-1]
        dist = distance_matrix[current_visit.visit_id][new_visit.visit_id]
        time = time_matrix[current_visit.visit_id][new_visit.visit_id]

        while True:
            #Tant que l'on n'a pas effectué la livraison, continuer
            if not (self.vehicle.canAddTime(time + time_matrix[new_visit.visit_id][depot.visit_id])):
                #La journée du véhicule est finie, impossible d'effectuer la livraison
                return False
            elif not (self.vehicle.canAddKilometer(dist + distance_matrix[new_visit.visit_id][depot.visit_id])):
                #Le véhicule ne peut pas effectuer la distance puis retourner au dépôt, il faut le recharger
                self.vehicle.addKilometer(distance_matrix[current_visit.visit_id][depot.visit_id])
                self.vehicle.addTime(time_matrix[current_visit.visit_id][depot.visit_id])
                self.str_tour += ",R"
                self.visits.append(depot.clone())
                self.visits[-1].visit_name = "R"
                self.vehicle.recharge()  #charge FAST
                current_visit = depot
            elif not (self.vehicle.canRemoveCapacity(new_visit.demand)):
                #La destination a une demande trop forte, il faut réapprovisionner le véhicule en allant au dépôt
                self.vehicle.addKilometer(distance_matrix[current_visit.visit_id][depot.visit_id])
                self.vehicle.addTime(time_matrix[current_visit.visit_id][depot.visit_id])
                self.str_tour += ",C"
                self.visits.append(depot.clone())
                self.visits[-1].visit_name = "C"
                self.vehicle.resetCapacity()
                current_visit = depot
            else:
                #On peut effectuer la livraison
                self.vehicle.addKilometer(dist)
                self.vehicle.addTime(time)
                self.vehicle.removeCapacity(new_visit.demand)
                self.str_tour += "," + str(new_visit.visit_id)
                current_visit = new_visit
                self.visits.append(new_visit)
                return True
            dist = distance_matrix[current_visit.visit_id][new_visit.visit_id]
            time = time_matrix[current_visit.visit_id][new_visit.visit_id]

    def removeLastVisit(self, distance_matrix, time_matrix):
        if len(self.visits) == 0:
            raise IndexError("Cannot remove a visit from an empty list")
        if len(self.visits) == 1:
            self.visits.pop()
            self.vehicle.resetVehicle()
        elif self.visits[-1].visit_name == 'C' or self.visits[-1].visit_name == 'R':
            while self.visits[-1].visit_name == 'C' or self.visits[-1].visit_name == 'R':
                self.visits.pop()
            self.visits.pop()
            #Si l'on trouve des étapes de retour au dépôt ou de rechargement, il faudra rejouer le Tour entier
            self.replayTour(distance_matrix, time_matrix)
        else:
            dist = distance_matrix[self.visits[-1].visit_id][self.visits[-2].visit_id]
            time = time_matrix[self.visits[-1].visit_id][self.visits[-2].visit_id]
            self.vehicle.removeKilometer(dist)
            self.vehicle.removeTime(time)
            self.vehicle.addCapacity(self.visits[-1].demand)
            split_str_tour = self.str_tour.split(',')
            split_str_tour.pop()
            self.str_tour = ','.join(split_str_tour)
            self.visits.pop()

    def replayTour(self, distance_matrix, time_matrix):
        """
        Fonction pour rejouer l'ensemble des tours de cet objet Tour tout en réinitialisant son véhicule.
        ATTENTION peut lever IndexError ou ValueError si la liste des visites n'est pas valide par exemple !

        :param distance_matrix:
        :param time_matrix:
        :return:
        """
        self.vehicle.resetVehicle()
        current_visit = self.visits[0]
        for futurVisit in self.visits[1:]:
            dist = distance_matrix[current_visit.visit_id][futurVisit.visit_id]
            time = time_matrix[current_visit.visit_id][futurVisit.visit_id]
            self.vehicle.addKilometer(dist)
            self.vehicle.addTime(time)
            if futurVisit.visit_name == "C":
                self.vehicle.setCapacity(self.vehicle.current_capacity)
            elif futurVisit.visit_name == "R":
                self.vehicle.recharge()
            else:
                self.vehicle.removeCapacity(futurVisit.demand)
            current_visit = futurVisit

    def isAValidTour(self, distance_matrix, time_matrix) -> bool:
        """
        Fonction de contrôle d'un Tour valide.
        Rejoue simplement le trajet et vérifie qu'il n'y a pas d'exceptions levées.

        :param distance_matrix: matrice des distances
        :param time_matrix: matrice des temps
        :return: bool
        """
        try:
            if len(self.visits) == 0:
                return True
            self.replayTour(distance_matrix, time_matrix)
            return True
        except (IndexError, ValueError):
            return False

    def swapVisits(self, i, j):
        """
        Echange les objets indiqués aux index i et j dans la liste de visites.
        Cette méthode ne REJOUE PAS le tour entier, ne pas oublier ensuite de le vérifier s'il reste valide !

        :param i: index 1
        :param j: index 2
        """
        temp = self.visits[i]
        self.visits[i] = self.visits[j]
        self.visits[j] = temp

    def findCorRVisits(self, find_c: bool = True, find_r: bool = True) -> typing.List[int]:
        """
        Recherche les étapes 'C' ou 'R' dans la liste de visites et renvoie la liste des index trouvés.

        :param find_c: Sélectionner les étapes 'C' (par défaut True)
        :param find_r: Sélectionner les étapes 'R' (par défaut True)
        :return: list(int)
        """
        res = []
        for i in range(len(self.visits)):
            if (self.visits[i].visit_name == 'C' and find_c) or (self.visits[i].visit_name == 'R' and find_r):
                res.append(i)
        return res

    def buildTour(self, mode: str, remaining_visits: typing.List[Visit], depot: Visit, distance_matrix, time_matrix) \
            -> typing.List[Visit]:
        """
        Fonction pour choisir le mode de construction d'un Tour.

        :raises ValueError : Le mode spécifié est inconnu
        """
        if mode == "Naif":
            return self.buildTourNaif(remaining_visits, depot, distance_matrix, time_matrix)
        elif mode == "Random":
            return self.buildTourRandom(remaining_visits, depot, distance_matrix, time_matrix)
        elif mode == "Glouton":
            return self.buildTourGlouton(remaining_visits, depot, distance_matrix, time_matrix)
        else:
            raise ValueError("Unknown mode for buildTour")

    def buildTourNaif(self, remaining_visits: typing.List[Visit], depot: Visit, distance_matrix, time_matrix) \
            -> typing.List[Visit]:
        """
        Construire un Tour en mode Naïf : On prend simplement la liste de visites dans l'ordre.

        :param remaining_visits:
        :param depot:
        :param distance_matrix:
        :param time_matrix:
        :return: Tuple(visites restantes, chaîne de caractères)
        """
        self.visits.append(depot)
        self.str_tour = str(depot.visit_id)
        self.vehicle.setCapacity(self.vehicle.current_capacity)
        while len(remaining_visits) > 0:
            future_visit = remaining_visits[0]

            visit_added = self.addToVisits(future_visit, distance_matrix, time_matrix)
            if not visit_added:
                #Cannot build the Tour further
                break
            remaining_visits.remove(future_visit)

        return remaining_visits

    def buildTourRandom(self, remaining_visits: typing.List[Visit], depot: Visit, distance_matrix, time_matrix) \
            -> typing.List[Visit]:
        """
        Construire un Tour en mode Random : Sélectionne une visite aléatoire dans la liste à chaque fois.
        Cette méthode est NON-DETERMINISTE !

        :param remaining_visits:
        :param depot:
        :param distance_matrix:
        :param time_matrix:
        :return: Tuple(visites restantes, chaîne de caractères)
        """
        self.visits.append(depot)
        self.str_tour = str(depot.visit_id)
        self.vehicle.setCapacity(self.vehicle.current_capacity)
        while len(remaining_visits) > 0:
            future_visit = remaining_visits[random.randint(0, len(remaining_visits) - 1)]

            visit_added = self.addToVisits(future_visit, distance_matrix, time_matrix)
            if not visit_added:
                #Cannot build the Tour further
                break
            remaining_visits.remove(future_visit)

        return remaining_visits

    def buildTourGlouton(self, remaining_visits: typing.List[Visit], depot: Visit, distance_matrix, time_matrix) \
            -> typing.List[Visit]:
        """
        Construit un Tour en mode Glouton : Recherche la visite la plus proche dans la liste à chaque fois.

        :param remaining_visits:
        :param depot:
        :param distance_matrix:
        :param time_matrix:
        :return: Tuple(visites restantes, chaîne de caractères)
        """
        self.visits.append(depot)
        self.str_tour = str(depot.visit_id)
        self.vehicle.setCapacity(self.vehicle.current_capacity)
        current_visit = depot
        while len(remaining_visits) > 0:
            future_visit = findNearestVisit(remaining_visits, current_visit, distance_matrix)
            """ TODO pour plus tard ? nearestDepot = findNearestDepot(listVisits, current_visit, distance_matrix)"""

            visit_added = self.addToVisits(future_visit, distance_matrix, time_matrix)
            if not visit_added:
                #Cannot build the Tour further
                break
            remaining_visits.remove(future_visit)
            current_visit = future_visit

        return remaining_visits

    def __repr__(self):
        return "TOUR: visits=" + repr(self.visits) \
               + "\n vehicle=" + repr(self.vehicle) \
               + "\n"


def findNearestVisit(list_visit: typing.List[Visit], from_visit: Visit, distance_matrix) -> Visit:
    """
    A partir d'une liste de Visit, retourne la Visit ayant la distance la plus faible
    avec une Visit de départ spécifiée.

    :param list_visit:
    :param from_visit:
    :param distance_matrix:
    :return: Visit
    """
    dist_min = distance_matrix[from_visit.visit_id][list_visit[0].visit_id]  #raises IndexError if listVisit is empty!
    future_visit = list_visit[0]
    for j in range(0, len(list_visit) - 1):
        temp_dist = distance_matrix[from_visit.visit_id][list_visit[j].visit_id]
        if dist_min > temp_dist:
            future_visit = list_visit[j]
            dist_min = temp_dist
    return future_visit


def findNearestDepot(list_visit: typing.List[Visit], from_visit: Visit, distance_matrix) -> Visit:
    """
    A partir d'une liste de Visit, retourne la Visit de type "Dépôt" ayant la distance la plus faible
    avec une Visit de départ spécifiée.

    :param list_visit:
    :param from_visit:
    :param distance_matrix:
    :return: Visit
    """
    list_depots = list(filter(lambda x: x.visit_name == "Depot", list_visit))
    return findNearestVisit(list_depots, from_visit, distance_matrix)
