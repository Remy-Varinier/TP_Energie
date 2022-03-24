class Vehicle:
    def __init__(self, max_dist: int, capacity: int, charge_fast: int, charge_medium: int, charge_slow: int, start_time: str, end_time: str):
        self.maxDist = max_dist #Distance max en kilomètres parcourable par le véhicule entre deux recharges
        self.capacity = capacity #Capacité max du véhicule en nombre de sacs
        self.chargeFast = charge_fast #Temps de recharge rapide, en minutes
        self.chargeMedium = charge_medium #Temps de recharge moyenne, en minutes
        self.chargeSlow = charge_slow #Temps de recharge lente, en minutes
        self.startTime = start_time #Heure de début d'une journée de livraison (str)
        self.endTime = end_time #Heure de fin de journée de livraison (str)
        self.totalTime = self.setTotalTime(start_time, end_time) #Durée de la journée de livraison en SECONDES, calculé à partir de start_time et end_time
        self.currentDist = 0 #Distance parcourue actuelle en kilomètres
        self.currentCapacity = 0 #Capacité actuelle en nombre de sacs
        self.currentTime = 0 #Temps passé actuel en livraison

    def addCapacity(self, charge: int) -> bool:
        if self.currentCapacity + charge > self.capacity:
            return False
        self.currentCapacity += charge
        return True

    def removeCapacity(self, charge: int) -> bool:
        if self.currentCapacity - charge < 0:
            return False
        self.currentCapacity -= charge
        return True

    def setCapacity(self, charge: int) -> bool:
        if charge < 0 or charge > self.capacity:
            return False
        self.currentCapacity = charge
        return True

    def addKilometer(self, kilometre: int) -> bool:
        if self.currentDist + kilometre > self.maxDist:
            return False
        self.currentDist += kilometre
        return True

    def resetKilometer(self):
        self.currentDist = 0

    def addTime(self, amount: int) -> bool:
        if self.currentTime + amount > self.totalTime:
            return False
        self.currentTime += amount
        return True

    def setTotalTime(self, start: str, end: str) -> int:
        [start_hour, start_minute] = start.split(":")
        [end_hour, end_minute] = end.split(":")
        return (int(end_hour)-int(start_hour))*3600+(int(end_minute)-int(start_minute))*60

    def __str__(self):
        return "VEHICLE: maxDist="+str(self.maxDist)\
        +" capacity="+str(self.capacity)\
        +" chargeFast="+str(self.chargeFast)\
        +" chargeMedium"+str(self.chargeMedium)\
        +" chargeSlow="+str(self.chargeSlow)\
        +" startTime="+self.startTime\
        +" endTime="+self.endTime\
        +" currentDist="+str(self.currentDist)\
        +" currentCapacity="+str(self.currentCapacity)

