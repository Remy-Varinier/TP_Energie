from enum import Enum

class ChargeEnum(Enum):
    FAST = 1
    MEDIUM = 2
    SLOW = 3


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
        self.currentCapacity = 0

        startTimeSplit = self.startTime.split(":")
        self.time = int(startTimeSplit[0]) * 3600 + int(startTimeSplit[1]) * 60 #Moment de la journée en SECONDES

    def addCapacity(self, charge):
        if not(self.canAddCapacity(charge)):
            raise ValueError("Too much capacity to add for this vehicle : "+repr(self))
        self.currentCapacity += charge

    def canAddCapacity(self, charge) -> bool:
        return self.currentCapacity + charge <= self.capacity

    def removeCapacity(self, charge):
        if not(self.canRemoveCapacity(charge)):
            raise ValueError("Too much capacity to remove for this vehicle : "+repr(self))
        self.currentCapacity -= charge

    def canRemoveCapacity(self, charge) -> bool:
        return self.currentCapacity - charge >= 0

    def setCapacity(self, charge):
        if not(charge >= 0 or charge <= self.capacity):
            raise ValueError("Incorrect capacity set for this vehicle : "+repr(self))
        self.currentCapacity = charge

    def addKilometer(self, kilometre):
        if not(self.canAddKilometer(kilometre)):
            raise ValueError("Too many kilometers to add for this vehicle : "+repr(self))
        self.distDone += kilometre

    def canAddKilometer(self, kilometre) -> bool:
        return self.distDone + kilometre <= self.maxDist

    def addTime(self, time):
        if not(self.canAddTime(time)):
            raise ValueError("Too much time to add for this vehicle : "+repr(self))
        self.time += time

    def canAddTime(self, timeAdded: int) -> bool:
        splitEndTime = self.endTime.split(":")
        return int(splitEndTime[0]) * 3600 + int(splitEndTime[1]) * 60 >= self.time + timeAdded

    def resetKilometer(self):
        self.distDone = 0

    def recharge(self, rechargeMode=ChargeEnum.FAST):
        """
        Recharger le véhicule selon le mode spécifié (par défaut FAST).
        Cela réinitialise son compteur kilométrique et ajoute le temps de charge.
        Note : Pour éviter une exception, on considère que le véhicule peut terminer sa journée
        au cours d'un rechargement, il n'y a donc pas de contrôle du temps ajouté.

        :param rechargeMode:
        :raises ValueError : Le mode spécifié est inconnu
        """
        if rechargeMode == ChargeEnum.FAST:
            self.time += self.chargeFast
        elif rechargeMode == ChargeEnum.MEDIUM:
            self.time += self.chargeMedium
        elif rechargeMode == ChargeEnum.SLOW:
            self.time += self.chargeSlow
        else:
            raise ValueError("Invalid ChargeEnum")
        self.resetKilometer()

    def clone(self):
        return Vehicle(self.maxDist, self.capacity, self.chargeFast, self.chargeMedium, self.chargeSlow, self.startTime, self.endTime)

    def __repr__(self):
        second = int(self.time%60)
        minute = int((self.time//60)%60)
        hour = int((self.time//3600)%24)
        return "VEHICLE: maxDist=" + str(self.maxDist) \
               + " capacity=" + str(self.capacity) \
               + " chargeFast=" + str(self.chargeFast) \
               + " chargeMedium" + str(self.chargeMedium) \
               + " chargeSlow=" + str(self.chargeSlow) \
               + " startTime=" + self.startTime \
               + " endTime=" + self.endTime \
               + " distDone=" + str(self.distDone) \
               + " currentCapacity=" + str(self.currentCapacity) \
               + " currentTime=" + str(hour) + ":" + str(minute) + ":" + str(second)\
               + "\n"