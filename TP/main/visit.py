class Visit:
    def __init__(self, visit_id: int, visit_name: str, visit_lat: float, visit_lon: float, demand: int):
        self.visit_id = visit_id  #Id
        self.visit_name = visit_name  #Nom
        self.visit_lat = visit_lat  #Latitude
        self.visit_lon = visit_lon  #Longitude
        self.demand = demand  #Demande en nombre de sacs à livrer

    def clone(self):
        """
        Retourne une copie de l'objet Visit.
        :return: Visit
        """
        return Visit(self.visit_id, self.visit_name, self.visit_lat, self.visit_lon, self.demand)

    def __repr__(self):
        return "VISIT: visitId=" + str(self.visit_id) \
               + " visitName=" + self.visit_name \
               + " visitLat=" + str(self.visit_lat) \
               + " visitLon=" + str(self.visit_lon) \
               + " demand=" + str(self.demand) \
               + "\n"
