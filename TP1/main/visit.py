class Visit:
    def __init__(self, visit_id: int, visit_name: str, visit_lat: float, visit_lon: float, demand: int):
        self.visitId = visit_id
        self.visitName = visit_name
        self.visitLat = visit_lat
        self.visitLon = visit_lon
        self.demand = demand
