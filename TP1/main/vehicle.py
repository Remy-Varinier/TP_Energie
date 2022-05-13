from enum import Enum

class ChargeEnum(Enum):
    FAST = 1
    MEDIUM = 2
    SLOW = 3


class Vehicle:
    def __init__(self, max_dist: int, capacity: int, charge_fast: int, charge_medium: int, charge_slow: int, start_time: str, end_time: str):
        self.maxDistance = max_dist
        self.maxCapacity = capacity
        self.chargeFast = charge_fast
        self.chargeMedium = charge_medium
        self.chargeSlow = charge_slow
        self.startTime = start_time
        self.endTime = end_time
        self.currentDistance = 0
        self.currentCapacity = 0
        startTimeSplit = self.startTime.split(":")
        self.currentTime = int(startTimeSplit[0]) * 3600 + int(startTimeSplit[1]) * 60 #Moment de la journée en SECONDES

    #Utility functions for capacity
    def addCapacity(self, charge):
        if not(self.canAddCapacity(charge)):
            raise ValueError("Too much capacity to add for this vehicle : "+repr(self))
        self.currentCapacity += charge

    def canAddCapacity(self, charge) -> bool:
        return self.currentCapacity + charge <= self.maxCapacity

    def removeCapacity(self, charge):
        if not(self.canRemoveCapacity(charge)):
            raise ValueError("Too much capacity to remove for this vehicle : "+repr(self))
        self.currentCapacity -= charge

    def canRemoveCapacity(self, charge) -> bool:
        return self.currentCapacity - charge >= 0

    def setCapacity(self, charge):
        if not(charge >= 0 or charge <= self.maxCapacity):
            raise ValueError("Incorrect capacity set for this vehicle : "+repr(self))
        self.currentCapacity = charge

    def resetCapacity(self):
        self.currentCapacity = self.maxCapacity

    #Utility functions for distance
    def addKilometer(self, kilometre):
        if not(self.canAddKilometer(kilometre)):
            raise ValueError("Too many kilometers to add for this vehicle : "+repr(self))
        self.currentDistance += kilometre

    def canAddKilometer(self, kilometre) -> bool:
        return self.currentDistance + kilometre <= self.maxDistance

    def removeKilometer(self, kilometre):
        if not(self.canRemoveKilometer(kilometre)):
            raise ValueError("Too many kilometers to remove for this vehicle : " + repr(self))
        self.currentDistance -= kilometre

    def canRemoveKilometer(self, kilometre):
        return self.currentDistance - kilometre >= 0

    def setKilometer(self, kilometre):
        if not(kilometre >= 0 or kilometre <= self.maxDistance):
            raise ValueError("Incorrect kilometers amount set for this vehicle : "+repr(self))
        self.currentDistance = kilometre

    def resetKilometer(self):
        self.currentDistance = 0

    #Utility functions for time
    def addTime(self, time):
        if not(self.canAddTime(time)):
            raise ValueError("Too much time to add for this vehicle : "+repr(self))
        self.currentTime += time

    def canAddTime(self, time) -> bool:
        splitEndTime = self.endTime.split(":")
        return self.currentTime + time <= int(splitEndTime[0]) * 3600 + int(splitEndTime[1]) * 60

    def removeTime(self, time):
        if not(self.canRemoveTime(time)):
            raise ValueError("Too much time to remove for this vehicle : " + repr(self))
        self.currentTime -= time

    def canRemoveTime(self, time):
        splitStartTime = self.startTime.split(":")
        return self.currentTime - time >= int(splitStartTime[0]) * 3600 + int(splitStartTime[1]) * 60

    def setTime(self, time):
        splitStartTime = self.startTime.split(":")
        splitEndTime = self.endTime.split(":")
        if not(time >= int(splitStartTime[0]) * 3600 + int(splitStartTime[1]) * 60
               or time <= int(splitEndTime[0]) * 3600 + int(splitEndTime[1]) * 60):
            raise ValueError("Incorrect time set for this vehicle : " + repr(self))
        self.currentTime = time

    def resetTime(self):
        startTimeSplit = self.startTime.split(":")
        self.currentTime = int(startTimeSplit[0]) * 3600 + int(startTimeSplit[1]) * 60

    def resetVehicle(self):
        self.resetCapacity()
        self.resetKilometer()
        self.resetTime()


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
            self.currentTime += self.chargeFast
        elif rechargeMode == ChargeEnum.MEDIUM:
            self.currentTime += self.chargeMedium
        elif rechargeMode == ChargeEnum.SLOW:
            self.currentTime += self.chargeSlow
        else:
            raise ValueError("Invalid ChargeEnum")
        self.resetKilometer()

    def clone(self):
        return Vehicle(self.maxDistance, self.maxCapacity, self.chargeFast, self.chargeMedium, self.chargeSlow, self.startTime, self.endTime)

    def __repr__(self):
        second = int(self.currentTime % 60)
        minute = int((self.currentTime // 60) % 60)
        hour = int((self.currentTime // 3600) % 24)
        return "VEHICLE: maxDist=" + str(self.maxDistance) \
               + " capacity=" + str(self.currentCapacity) \
               + " chargeFast=" + str(self.chargeFast) \
               + " chargeMedium" + str(self.chargeMedium) \
               + " chargeSlow=" + str(self.chargeSlow) \
               + " startTime=" + self.startTime \
               + " endTime=" + self.endTime \
               + " distDone=" + str(self.currentDistance) \
               + " currentCapacity=" + str(self.currentCapacity) \
               + " currentTime=" + str(hour) + ":" + str(minute) + ":" + str(second)\
               + "\n"
