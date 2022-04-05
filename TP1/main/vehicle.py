from cgitb import reset
from posixpath import split
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

        startTimeSplit = self.startTime.split(":")
        self.time = int(startTimeSplit[0]) * 3600 + \
            int(startTimeSplit[1]) * 60

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

    def canAddKilometer(self, kilometre) -> bool:
        if self.distDone + kilometre > self.maxDist:
            return False
        return True

    def addTime(self, time) -> bool:
        if self.canAddTime(time) == False:
            return False
        self.time += time
        return True

    def canAddTime(self, time) -> bool:
        splitEndTime = self.endTime.split(":")
        if (int(splitEndTime[0]) * 3600 + int(splitEndTime[1]) * 60 < self.time + time):
            return False
        return True

    def resetKilometer(self):
        self.distDone = 0

    def recharge(self):
        self.addTime(self.chargeFast)
        self.resetKilometer()

    def clone(self):
        return Vehicle(self.maxDist, self.capacity, self.chargeFast, self.chargeMedium, self.chargeSlow, self.startTime, self.endTime)

    def __str__(self):
        return "VEHICLE: maxDist=" + str(self.maxDist) \
               + " capacity=" + str(self.capacity) \
               + " chargeFast=" + str(self.chargeFast) \
               + " chargeMedium" + str(self.chargeMedium) \
               + " chargeSlow=" + str(self.chargeSlow) \
               + " startTime=" + self.startTime \
               + " endTime=" + self.endTime \
               + " distDone=" + str(self.distDone) \
               + " charge=" + str(self.charge)