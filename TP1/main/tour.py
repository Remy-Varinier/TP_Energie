import random
import typing

from globals import Globals
from vehicle import Vehicle
from visit import Visit


#TODO comment gérer les exceptions renvoyés par replayTour() ??

class Tour:
    def __init__(self, visits: typing.List[Visit], vehicle: Vehicle, globals: Globals):
        self.visits = visits  #Liste des objets Visit contenus dans ce tour
        self.vehicle = vehicle  #Véhicule parcourant ce tour
        self.str_tour = ""  #Représentation du tour en chaîne de caractères affichable
        self.distances = globals.distances #Référence aux variables globales
        self.times = globals.times #Référence aux variables globales

    def calcKilometre(self) -> float:
        """
        Calculer le nombre de kilomètres parcourus dans ce Tour au total.
        Cette fonction est utile dans notre contexte pour comparer deux solutions différentes.

        :return: sum(distance entre chaque visite)
        """
        if len(self.visits) < 2:
            return 0
        i = 0
        j = 1
        total = 0
        while j < len(self.visits):
            total += self.distances[self.visits[i].visit_id][self.visits[j].visit_id]
            i += 1
            j += 1
        return total

    def addToVisits(self, new_visit: Visit, depot=None) -> bool:  #returns True if visit could be added
        """
        Fonction pour ajouter une visite à la liste de visites.
        Cette logique est commune à toutes les constructions de tours possibles.
        Elle prend en compte les retours au dépôt (C) et rechargements (R).

        :param new_visit: Visit à effectuer
        :param depot: (Optionnel) Visit représentant le dépôt.
        Par défaut c'est la Visit de départ dans la liste. Attention peut renvoyer IndexError si cette liste est vide !
        :return: La visite a pu être effectuée ou non.
        Si ce n'est pas le cas, c'est parce que le véhicule associé a fini sa journée.
        """

        if depot is None:
            depot = self.visits[0]
        current_visit = self.visits[-1]
        dist = self.distances[current_visit.visit_id][new_visit.visit_id]
        time = self.times[current_visit.visit_id][new_visit.visit_id]

        while True:
            #Tant que l'on n'a pas effectué la livraison, continuer
            if not (self.vehicle.canAddTime(time + self.times[new_visit.visit_id][depot.visit_id])):
                #La journée du véhicule est finie, impossible d'effectuer la livraison
                return False
            elif not (self.vehicle.canAddKilometer(dist + self.distances[new_visit.visit_id][depot.visit_id])):
                #Le véhicule ne peut pas effectuer la distance puis retourner au dépôt, il faut le recharger
                self.vehicle.addKilometer(self.distances[current_visit.visit_id][depot.visit_id])
                self.vehicle.addTime(self.times[current_visit.visit_id][depot.visit_id])
                self.str_tour += ",R"
                self.visits.append(depot.clone())
                self.visits[-1].visit_name = "R"
                self.vehicle.recharge()  #charge FAST
                current_visit = depot
            elif not (self.vehicle.canRemoveCapacity(new_visit.demand)):
                #La destination a une demande trop forte, il faut réapprovisionner le véhicule en allant au dépôt
                self.vehicle.addKilometer(self.distances[current_visit.visit_id][depot.visit_id])
                self.vehicle.addTime(self.times[current_visit.visit_id][depot.visit_id])
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
            dist = self.distances[current_visit.visit_id][new_visit.visit_id]
            time = self.times[current_visit.visit_id][new_visit.visit_id]

    def removeLastVisit(self):
        """
        Fonction pour retirer la dernière visite de la liste tout en recalculant les attributs
        véhicule et str_tour.
        """
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
            self.replayTour(self.distances, self.times)
        else:
            dist = self.distances[self.visits[-1].visit_id][self.visits[-2].visit_id]
            time = self.times[self.visits[-1].visit_id][self.visits[-2].visit_id]
            self.vehicle.removeKilometer(dist)
            self.vehicle.removeTime(time)
            self.vehicle.addCapacity(self.visits[-1].demand)
            split_str_tour = self.str_tour.split(',')
            split_str_tour.pop()
            self.str_tour = ','.join(split_str_tour)
            self.visits.pop()

    def replayTour(self):
        """
        Fonction pour rejouer l'ensemble des tours de cet objet Tour tout en réinitialisant son véhicule
        et en reconstruisant la chaîne de caractères.
        ATTENTION peut lever IndexError ou ValueError si la liste des visites n'est pas valide par exemple !
        Les attributs du tour sont modifiés uniquement si le tour a été rejoué avec succès.
        :return:
        """
        new_vehicle = self.vehicle.clone()
        new_str_tour = str(self.visits[0].visit_id)
        current_visit = self.visits[0]
        for future_visit in self.visits[1:]:
            dist = self.distances[current_visit.visit_id][future_visit.visit_id]
            time = self.times[current_visit.visit_id][future_visit.visit_id]
            new_vehicle.addKilometer(dist)
            new_vehicle.addTime(time)
            if future_visit.visit_name == "C":
                new_vehicle.setCapacity(new_vehicle.current_capacity)
                new_str_tour += ",C"
            elif future_visit.visit_name == "R":
                new_vehicle.recharge()
                new_str_tour += ",R"
            else:
                new_vehicle.removeCapacity(future_visit.demand)
                new_str_tour += "," + str(future_visit.visit_id)
            current_visit = future_visit
        self.vehicle = new_vehicle
        self.str_tour = new_str_tour

    def isAValidTour(self) -> bool:
        """
        Fonction de contrôle d'un Tour valide.
        Rejoue simplement le trajet et vérifie qu'il n'y a pas d'exceptions levées.

        :return: bool
        """
        try:
            if len(self.visits) == 0:
                return True
            self.replayTour()
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

    def buildTour(self, mode: str, remaining_visits: typing.List[Visit], depot: Visit) -> typing.List[Visit]:
        """
        Fonction pour choisir le mode de construction d'un Tour.

        :param mode: Naif | Random | Glouton
        :param remaining_visits: Liste de visites à effectuer
        :param depot: Visit de départ
        :raises ValueError : Le mode spécifié est inconnu
        :return: List(Visit) le tour construit
        """
        if mode == "Naif":
            return self.buildTourNaif(remaining_visits, depot)
        elif mode == "Random":
            return self.buildTourRandom(remaining_visits, depot)
        elif mode == "Glouton":
            return self.buildTourGlouton(remaining_visits, depot)
        else:
            raise ValueError("Unknown mode for buildTour")

    def buildTourNaif(self, remaining_visits: typing.List[Visit], depot: Visit) -> typing.List[Visit]:
        """
        Construire un Tour en mode Naïf : On prend simplement la liste de visites dans l'ordre.

        :param remaining_visits:
        :param depot:
        :return: Tuple(visites restantes, chaîne de caractères)
        """
        self.visits.append(depot)
        self.str_tour = str(depot.visit_id)
        self.vehicle.setCapacity(self.vehicle.current_capacity)
        while len(remaining_visits) > 0:
            future_visit = remaining_visits[0]

            visit_added = self.addToVisits(future_visit)
            if not visit_added:
                #Cannot build the Tour further
                break
            remaining_visits.remove(future_visit)

        return remaining_visits

    def buildTourRandom(self, remaining_visits: typing.List[Visit], depot: Visit) -> typing.List[Visit]:
        """
        Construire un Tour en mode Random : Sélectionne une visite aléatoire dans la liste à chaque fois.
        Cette méthode est NON-DETERMINISTE !

        :param remaining_visits:
        :param depot:
        :return: Tuple(visites restantes, chaîne de caractères)
        """
        self.visits.append(depot)
        self.str_tour = str(depot.visit_id)
        self.vehicle.setCapacity(self.vehicle.current_capacity)
        while len(remaining_visits) > 0:
            future_visit = remaining_visits[random.randint(0, len(remaining_visits) - 1)]

            visit_added = self.addToVisits(future_visit)
            if not visit_added:
                #Cannot build the Tour further
                break
            remaining_visits.remove(future_visit)

        return remaining_visits

    def buildTourGlouton(self, remaining_visits: typing.List[Visit], depot: Visit) -> typing.List[Visit]:
        """
        Construit un Tour en mode Glouton : Recherche la visite la plus proche dans la liste à chaque fois.

        :param remaining_visits:
        :param depot:
        :return: Tuple(visites restantes, chaîne de caractères)
        """
        self.visits.append(depot)
        self.str_tour = str(depot.visit_id)
        self.vehicle.setCapacity(self.vehicle.current_capacity)
        current_visit = depot
        while len(remaining_visits) > 0:
            future_visit = self.findNearestVisit(remaining_visits, current_visit)
            """ TODO pour plus tard ? nearestDepot = findNearestDepot(listVisits, current_visit)"""

            visit_added = self.addToVisits(future_visit)
            if not visit_added:
                #Cannot build the Tour further
                break
            remaining_visits.remove(future_visit)
            current_visit = future_visit

        return remaining_visits

    def findNearestVisit(self, list_visit: typing.List[Visit], from_visit: Visit) -> Visit:
        """
        A partir d'une liste de Visit, retourne la Visit ayant la distance la plus faible
        avec une Visit de départ spécifiée.

        :param list_visit:
        :param from_visit:
        :return: Visit
        """
        dist_min = self.distances[from_visit.visit_id][
            list_visit[0].visit_id]  #raises IndexError if listVisit is empty!
        future_visit = list_visit[0]
        for j in range(0, len(list_visit) - 1):
            temp_dist = self.distances[from_visit.visit_id][list_visit[j].visit_id]
            if dist_min > temp_dist:
                future_visit = list_visit[j]
                dist_min = temp_dist
        return future_visit

    def findNearestDepot(self, list_visit: typing.List[Visit], from_visit: Visit) -> Visit:
        """
        A partir d'une liste de Visit, retourne la Visit de type "Dépôt" ayant la distance la plus faible
        avec une Visit de départ spécifiée.

        :param list_visit:
        :param from_visit:
        :return: Visit
        """
        list_depots = list(filter(lambda x: x.visit_name == "Depot", list_visit))
        return self.findNearestVisit(list_depots, from_visit)


    def __repr__(self):
        return "TOUR: visits=" + repr(self.visits) \
               + "\n vehicle=" + repr(self.vehicle) \
               + "\n"

