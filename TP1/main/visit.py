class Visit:
    def __init__(self, visit_id: int, visit_name: str, visit_lat: float, visit_lon: float, demand: int):
        self.visitId = visit_id #Id
        self.visitName = visit_name #Nom
        self.visitLat = visit_lat #Latitude
        self.visitLon = visit_lon #Longitude
        self.demand = demand #Demande en nombre de sacs à livrer

    def __str__(self):
        return "VISIT: visitId=" + str(self.visitId) \
               + " visitName=" + self.visitName \
               + " visitLat=" + str(self.visitLat) \
               + " visit_lon=" + str(self.visitLon) \
               + " demand=" + str(self.demand)