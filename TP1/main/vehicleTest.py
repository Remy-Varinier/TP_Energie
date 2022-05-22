import unittest

from vehicle import ChargeEnum

from globals import Globals


class VehicleTest(unittest.TestCase):

    def setUp(self) -> None:
        self.my_globals = Globals()
        self.vehicle = self.my_globals.vehicle_model.clone()

    def testItCanAddCapacity(self):
        self.assertEqual(self.vehicle.current_capacity, 0)
        self.vehicle.addCapacity(10)
        self.assertEqual(self.vehicle.current_capacity, 10)

    def testItCannotAddCapacityWhenMaxCapacityIsReached(self):
        self.assertRaises(ValueError, self.vehicle.addCapacity)
        self.vehicle.addCapacity(self.vehicle.max_capacity + 1)

    def testItCanRemoveCapacity(self):
        self.vehicle.current_capacity = 10
        self.assertEqual(self.vehicle.current_capacity, 10)
        self.vehicle.removeCapacity(5)
        self.assertEqual(self.vehicle.current_capacity, 5)

    def testItCannotRemoveCapacityWhenMinCapacityIsReached(self):
        self.assertRaises(ValueError, self.vehicle.removeCapacity)
        self.vehicle.removeCapacity(10)

    def testItCanSetCapacity(self):
        self.assertEqual(self.vehicle.current_capacity, 0)
        self.vehicle.setCapacity(10)
        self.assertEqual(self.vehicle.current_capacity, 10)

    def testItCannotSetCapacityWhenMaxCapacityIsReached(self):
        self.assertRaises(ValueError, self.vehicle.setCapacity)
        self.vehicle.setCapacity(self.vehicle.max_capacity + 1)

    def testItCannotSetCapacityWhenMinCapacityIsReached(self):
        self.assertRaises(ValueError, self.vehicle.setCapacity)
        self.vehicle.setCapacity(-1)

    def testItCanResetCapacity(self):
        self.vehicle.resetCapacity()
        self.assertEqual(self.vehicle.current_capacity,
                         self.vehicle.max_capacity)

    def testItCanAddKilometer(self):
        self.assertEqual(self.vehicle.current_distance, 0)
        self.vehicle.addKilometer(10)
        self.assertEqual(self.vehicle.current_distance, 10)

    def testItCannotAddKilometerWhenMaxDistanceIsReached(self):
        self.assertRaises(ValueError, self.vehicle.addKilometer)
        self.vehicle.addKilometer(self.vehicle.max_distance + 1)

    def testItCanRemoveKilometer(self):
        self.vehicle.current_distance = 10
        self.assertEqual(self.vehicle.current_distance, 10)
        self.vehicle.removeKilometer(5)
        self.assertEqual(self.vehicle.current_distance, 5)

    def testItCannotRemoveKilometerWhenMinDistanceIsReached(self):
        self.assertRaises(ValueError, self.vehicle.removeKilometer)
        self.vehicle.removeKilometer(10)

    def testItCanSetKilometer(self):
        self.assertEqual(self.vehicle.current_distance, 0)
        self.vehicle.setKilometer(10)
        self.assertEqual(self.vehicle.current_distance, 10)

    def testItCannotSetKilometerWhenMaxDistanceIsReached(self):
        self.assertRaises(ValueError, self.vehicle.setKilometer)
        self.vehicle.setKilometer(self.vehicle.max_distance + 1)

    def testItCannotSetKilometerWhenMinDistanceIsReached(self):
        self.assertRaises(ValueError, self.vehicle.setKilometer)
        self.vehicle.setKilometer(-1)

    def testItCanResetKilometer(self):
        self.vehicle.resetKilometer()
        self.assertEqual(self.vehicle.current_distance, 0)

    def testItCanAddTime(self):
        self.assertEqual(self.vehicle.current_time, 0)
        self.vehicle.addTime(10)
        self.assertEqual(self.vehicle.current_time, 10)

    def testItCannotAddTimeWhenMaxTimeIsReached(self):
        self.assertRaises(ValueError, self.vehicle.addTime)
        self.vehicle.addTime(100000)

    def testItCanRemoveTime(self):
        self.vehicle.current_time = 10
        self.assertEqual(self.vehicle.current_time, 10)
        self.vehicle.removeTime(5)
        self.assertEqual(self.vehicle.current_time, 5)

    def testItCannotRemoveTimeWhenMinTimeIsReached(self):
        self.assertRaises(ValueError, self.vehicle.removeTime)
        self.vehicle.removeTime(10)

    def testItCanSetTime(self):
        self.assertEqual(self.vehicle.current_time, 0)
        self.vehicle.setTime(10)
        self.assertEqual(self.vehicle.current_time, 10)

    def testItCannotSetTimeWhenMaxTimeIsReached(self):
        self.assertRaises(ValueError, self.vehicle.setTime)
        self.vehicle.setTime(100000)

    def testItCannotSetTimeWhenMinTimeIsReached(self):
        self.assertRaises(ValueError, self.vehicle.setTime)
        self.vehicle.setTime(-1)

    def testItCanRechargeFast(self):
        self.vehicle.recharge(ChargeEnum.FAST)
        self.assertEqual(self.vehicle.current_time,
                         self.vehicle.charge_fast * 60)
        self.assertEqual(self.vehicle.current_distance, 0)

    def testItCanRechargeMedium(self):
        self.vehicle.recharge(ChargeEnum.MEDIUM)
        self.assertEqual(self.vehicle.current_time,
                         self.vehicle.charge_medium * 60)
        self.assertEqual(self.vehicle.current_distance, 0)

    def testItCanRechargeSlow(self):
        self.vehicle.recharge(ChargeEnum.SLOW)
        self.assertEqual(self.vehicle.current_time,
                         self.vehicle.charge_slow * 60)
        self.assertEqual(self.vehicle.current_distance, 0)

    def testItCannotRechargeWithInvalidCharge(self):
        self.assertRaises(ValueError, self.vehicle.recharge)
        self.vehicle.recharge("invalid")
