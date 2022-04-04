import typing


class Vehicle:
    def __init__(self, max_dist: int, capacity: int, charge_fast: int, charge_medium: int, charge_slow: int, start_time: str, end_time: str):
        self.maxDist = max_dist
        self.capacity = capacity
        self.chargeFast = charge_fast
        self.chargeMedium = charge_medium
        self.chargeSlow = charge_slow
        self.startTime = start_time
        self.endTime = end_time
        self.distDone = 0
        self.charge = 0

    def addCharge(self, charge) -> bool:
        if self.charge + charge > self.capacity:
            return False
        self.charge += charge
        return True

    def removeCharge(self, charge) -> bool:
        if self.charge - charge < 0:
            return False
        self.charge -= charge
        return True

    def addKilometer(self, kilometre) -> bool:
        if self.distDone + kilometre > self.maxDist:
            return False
        self.distDone += kilometre
        return True

    def resetKilometer(self):
        self.distDone = 0

    def clone(self):
        return Vehicle(self.maxDist, self.capacity, self.chargeFast, self.chargeMedium, self.chargeSlow, self.startTime, self.endTime)
