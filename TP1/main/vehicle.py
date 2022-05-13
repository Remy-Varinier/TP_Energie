from enum import Enum


class ChargeEnum(Enum):
    FAST = 1
    MEDIUM = 2
    SLOW = 3


class Vehicle:
    def __init__(self, max_dist: int, capacity: int, charge_fast: int, charge_medium: int, charge_slow: int,
                 start_time: str, end_time: str):
        self.max_distance = max_dist  #Distance maximale entre deux recharges, en kilomètres
        self.max_capacity = capacity  #Capacité maximale en nombre de sacs
        self.charge_fast = charge_fast  #Temps de charge rapide, en minutes
        self.charge_medium = charge_medium  #Temps de charge moyenne, en minutes
        self.charge_slow = charge_slow  #Temps de charge lente, en minutes
        self.start_time = start_time  #Heure de début, hh:mm
        self.end_time = end_time  #Heure de fin, hh:mm
        self.current_distance = 0  #Distance parcourue par le véhicule depuis sa dernière recharge, en kilomètres
        self.current_capacity = self.max_capacity  #Capacité actuelle du véhicule en nombre de sacs
        start_time_split = self.start_time.split(":")
        self.current_time = int(start_time_split[0]) * 3600 + int(
            start_time_split[1]) * 60  #Moment de la journée en SECONDES (correspond à hh:mm:ss)

    #Utility functions for capacity
    def addCapacity(self, charge):
        if not (self.canAddCapacity(charge)):
            raise ValueError("Too much capacity to add for this vehicle : " + repr(self))
        self.current_capacity += charge

    def canAddCapacity(self, charge) -> bool:
        return self.current_capacity + charge <= self.max_capacity

    def removeCapacity(self, charge):
        if not (self.canRemoveCapacity(charge)):
            raise ValueError("Too much capacity to remove for this vehicle : " + repr(self))
        self.current_capacity -= charge

    def canRemoveCapacity(self, charge) -> bool:
        return self.current_capacity - charge >= 0

    def setCapacity(self, charge):
        if not (charge >= 0 or charge <= self.max_capacity):
            raise ValueError("Incorrect capacity set for this vehicle : " + repr(self))
        self.current_capacity = charge

    def resetCapacity(self):
        self.current_capacity = self.max_capacity

    #Utility functions for distance
    def addKilometer(self, kilometre):
        if not (self.canAddKilometer(kilometre)):
            raise ValueError("Too many kilometers to add for this vehicle : " + repr(self))
        self.current_distance += kilometre

    def canAddKilometer(self, kilometre) -> bool:
        return self.current_distance + kilometre <= self.max_distance

    def removeKilometer(self, kilometre):
        if not (self.canRemoveKilometer(kilometre)):
            raise ValueError("Too many kilometers to remove for this vehicle : " + repr(self))
        self.current_distance -= kilometre

    def canRemoveKilometer(self, kilometre):
        return self.current_distance - kilometre >= 0

    def setKilometer(self, kilometre):
        if not (kilometre >= 0 or kilometre <= self.max_distance):
            raise ValueError("Incorrect kilometers amount set for this vehicle : " + repr(self))
        self.current_distance = kilometre

    def resetKilometer(self):
        self.current_distance = 0

    #Utility functions for time
    def addTime(self, time):
        if not (self.canAddTime(time)):
            raise ValueError("Too much time to add for this vehicle : " + repr(self))
        self.current_time += time

    def canAddTime(self, time) -> bool:
        split_end_time = self.end_time.split(":")
        return self.current_time + time <= int(split_end_time[0]) * 3600 + int(split_end_time[1]) * 60

    def removeTime(self, time):
        if not (self.canRemoveTime(time)):
            raise ValueError("Too much time to remove for this vehicle : " + repr(self))
        self.current_time -= time

    def canRemoveTime(self, time):
        split_start_time = self.start_time.split(":")
        return self.current_time - time >= int(split_start_time[0]) * 3600 + int(split_start_time[1]) * 60

    def setTime(self, time):
        split_start_time = self.start_time.split(":")
        split_end_time = self.end_time.split(":")
        if not (time >= int(split_start_time[0]) * 3600 + int(split_start_time[1]) * 60
                or time <= int(split_end_time[0]) * 3600 + int(split_end_time[1]) * 60):
            raise ValueError("Incorrect time set for this vehicle : " + repr(self))
        self.current_time = time

    def resetTime(self):
        start_time_split = self.start_time.split(":")
        self.current_time = int(start_time_split[0]) * 3600 + int(start_time_split[1]) * 60

    def resetVehicle(self):
        self.resetCapacity()
        self.resetKilometer()
        self.resetTime()

    def recharge(self, recharge_mode=ChargeEnum.FAST):
        """
        Recharger le véhicule selon le mode spécifié (par défaut FAST).
        Cela réinitialise son compteur kilométrique et ajoute le temps de charge.
        Note : Pour éviter une exception, on considère que le véhicule peut terminer sa journée
        au cours d'un rechargement, il n'y a donc pas de contrôle du temps ajouté.

        :param recharge_mode:
        :raises ValueError : Le mode spécifié est inconnu
        """
        if recharge_mode == ChargeEnum.FAST:
            self.current_time += self.charge_fast
        elif recharge_mode == ChargeEnum.MEDIUM:
            self.current_time += self.charge_medium
        elif recharge_mode == ChargeEnum.SLOW:
            self.current_time += self.charge_slow
        else:
            raise ValueError("Invalid ChargeEnum")
        self.resetKilometer()

    def clone(self):
        return Vehicle(self.max_distance, self.max_capacity, self.charge_fast, self.charge_medium, self.charge_slow,
                       self.start_time, self.end_time)

    def __repr__(self):
        second = int(self.current_time % 60)
        minute = int((self.current_time // 60) % 60)
        hour = int((self.current_time // 3600) % 24)
        return "VEHICLE: maxDist=" + str(self.max_distance) \
               + " capacity=" + str(self.current_capacity) \
               + " chargeFast=" + str(self.charge_fast) \
               + " chargeMedium" + str(self.charge_medium) \
               + " chargeSlow=" + str(self.charge_slow) \
               + " startTime=" + self.start_time \
               + " endTime=" + self.end_time \
               + " currentDistance=" + str(self.current_distance) \
               + " currentCapacity=" + str(self.current_capacity) \
               + " currentTime=" + str(hour) + ":" + str(minute) + ":" + str(second) \
               + "\n"
