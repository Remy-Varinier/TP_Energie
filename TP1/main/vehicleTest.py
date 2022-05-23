import unittest

from vehicle import ChargeEnum

from globals import Globals


class VehicleTest(unittest.TestCase):

    def setUp(self) -> None:
        self.my_globals = Globals()
        self.my_globals.define("../Data/lyon_40_1_1/")
        self.vehicle = self.my_globals.vehicle_model.clone()
        self.start_time_value = self.vehicle.start_time.split(":")
        self.start_time_value = int(self.start_time_value[0]) * 3600 + int(self.start_time_value[1]) * 60
        self.end_time_value = self.vehicle.end_time.split(":")
        self.end_time_value = int(self.end_time_value[0]) * 3600 + int(self.end_time_value[1]) * 60

    def testItCanAddCapacity(self):
        self.vehicle.current_capacity = 0
        self.assertEqual(self.vehicle.current_capacity, 0)
        self.vehicle.addCapacity(10)
        self.assertEqual(self.vehicle.current_capacity, 10)

    def testItCannotAddCapacityWhenMaxCapacityIsReached(self):
        self.assertRaises(ValueError, self.vehicle.addCapacity, self.vehicle.max_capacity + 1)

    def testItCanRemoveCapacity(self):
        self.vehicle.current_capacity = 10
        self.assertEqual(self.vehicle.current_capacity, 10)
        self.vehicle.removeCapacity(5)
        self.assertEqual(self.vehicle.current_capacity, 5)

    def testItCannotRemoveCapacityWhenMinCapacityIsReached(self):
        self.assertRaises(ValueError, self.vehicle.removeCapacity, self.vehicle.max_capacity + 1)

    def testItCanSetCapacity(self):
        #Le véhicule commence à une capacité égal à max_capacity
        self.assertEqual(self.vehicle.current_capacity, self.vehicle.max_capacity)
        self.vehicle.setCapacity(10)
        self.assertEqual(self.vehicle.current_capacity, 10)

    def testItCannotSetCapacityWhenMaxCapacityIsReached(self):
        self.assertRaises(ValueError, self.vehicle.setCapacity, self.vehicle.max_capacity + 1)

    def testItCannotSetCapacityWhenMinCapacityIsReached(self):
        self.assertRaises(ValueError, self.vehicle.setCapacity, -1)

    def testItCanResetCapacity(self):
        self.vehicle.current_capacity = 0
        self.vehicle.resetCapacity()
        self.assertEqual(self.vehicle.current_capacity,
                         self.vehicle.max_capacity)

    def testItCanAddKilometer(self):
        self.vehicle.current_distance = 0
        self.assertEqual(self.vehicle.current_distance, 0)
        self.vehicle.addKilometer(10)
        self.assertEqual(self.vehicle.current_distance, 10)

    def testItCannotAddKilometerWhenMaxDistanceIsReached(self):
        self.assertRaises(ValueError, self.vehicle.addKilometer, self.vehicle.max_distance + 1)

    def testItCanRemoveKilometer(self):
        self.vehicle.current_distance = 10
        self.assertEqual(self.vehicle.current_distance, 10)
        self.vehicle.removeKilometer(5)
        self.assertEqual(self.vehicle.current_distance, 5)

    def testItCannotRemoveKilometerWhenMinDistanceIsReached(self):
        self.assertRaises(ValueError, self.vehicle.removeKilometer, 10)

    def testItCanSetKilometer(self):
        #Le véhicule commence à un kilométrage à 0
        self.assertEqual(self.vehicle.current_distance, 0)
        self.vehicle.setKilometer(10)
        self.assertEqual(self.vehicle.current_distance, 10)

    def testItCannotSetKilometerWhenMaxDistanceIsReached(self):
        self.assertRaises(ValueError, self.vehicle.setKilometer, self.vehicle.max_distance + 1)

    def testItCannotSetKilometerWhenMinDistanceIsReached(self):
        self.assertRaises(ValueError, self.vehicle.setKilometer, -1)

    def testItCanResetKilometer(self):
        self.vehicle.current_distance = 10
        self.vehicle.resetKilometer()
        self.assertEqual(self.vehicle.current_distance, 0)

    def testItCanAddTime(self):
        self.assertEqual(self.vehicle.current_time, self.start_time_value)
        self.vehicle.addTime(10)
        self.assertEqual(self.vehicle.current_time, self.start_time_value + 10)

    def testItCannotAddTimeWhenMaxTimeIsReached(self):
        self.assertRaises(ValueError, self.vehicle.addTime, 100000)

    def testItCanRemoveTime(self):
        self.vehicle.current_time = self.start_time_value + 10
        self.assertEqual(self.vehicle.current_time, self.start_time_value + 10)
        self.vehicle.removeTime(5)
        self.assertEqual(self.vehicle.current_time, self.start_time_value + 5)

    def testItCannotRemoveTimeWhenMinTimeIsReached(self):
        self.assertRaises(ValueError, self.vehicle.removeTime, 10)

    def testItCanSetTime(self):
        self.assertEqual(self.vehicle.current_time, self.start_time_value)
        self.vehicle.setTime(self.start_time_value + 300)
        self.assertEqual(self.vehicle.current_time, self.start_time_value + 300)

    def testItCannotSetTimeWhenMaxTimeIsReached(self):
        self.assertRaises(ValueError, self.vehicle.setTime, 100000)

    def testItCannotSetTimeWhenMinTimeIsReached(self):
        self.assertRaises(ValueError, self.vehicle.setTime, -1)

    def testItCanRechargeFast(self):
        self.vehicle.recharge(ChargeEnum.FAST)
        self.assertEqual(self.vehicle.current_time,
                         self.start_time_value + self.vehicle.charge_fast * 60)
        self.assertEqual(self.vehicle.current_distance, 0)

    def testItCanRechargeMedium(self):
        self.vehicle.recharge(ChargeEnum.MEDIUM)
        self.assertEqual(self.vehicle.current_time,
                         self.start_time_value + self.vehicle.charge_medium * 60)
        self.assertEqual(self.vehicle.current_distance, 0)

    def testItCanRechargeSlow(self):
        self.vehicle.recharge(ChargeEnum.SLOW)
        self.assertEqual(self.vehicle.current_time,
                         self.start_time_value + self.vehicle.charge_slow * 60)
        self.assertEqual(self.vehicle.current_distance, 0)

    def testItCannotRechargeWithInvalidCharge(self):
        self.assertRaises(ValueError, self.vehicle.recharge, "invalid")
