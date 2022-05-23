import copy
import unittest

import main
from globals import Globals
from tour import Tour
from visit import Visit


class TestTour(unittest.TestCase):

    def setUp(self) -> None:
        self.my_globals = Globals()
        self.my_globals.define("../Data/lyon_40_1_1/")
        self.my_visits = copy.deepcopy(self.my_globals.list_visits)
        self.my_vehicle = self.my_globals.vehicle_model.clone()
        self.depot = self.my_visits.pop(0)
        self.visit_R = Visit(0, "R", 45.7640211, 4.8901678, 0)
        self.visit_C = Visit(0, "C", 45.7640211, 4.8901678, 0)
        self.tour_empty = Tour([], self.my_vehicle, self.my_globals)
        self.tour_sans_depot = Tour([self.my_visits[0]], self.my_vehicle, self.my_globals)
        self.tour_1_visit = Tour([self.my_visits[1]], self.my_vehicle, self.my_globals)
        self.tour_1_visit.starting_visit = self.depot
        (self.tours_test, self.str_tours_test) = main.buildTours(self.my_globals, mode="Naif")

    def testCalcKilometre(self):
        self.assertEqual(self.tour_empty.calcKilometre(), 0)
        #Echoue si le starting_visit n'est pas defini
        self.assertRaises(AttributeError, self.tour_sans_depot.calcKilometre)
        self.assertNotEqual(self.tour_1_visit.calcKilometre(), 0)
        self.assertNotEqual(sum(x.calcKilometre() for x in self.tours_test), 0)

    def testAddToVisits(self):
        self.assertEqual(len(self.tour_1_visit.visits), 1)
        self.assertEqual(self.tour_1_visit.addToVisits(self.my_visits[3]), True)
        self.assertEqual(len(self.tour_1_visit.visits), 2)
        self.assertEqual(self.tour_1_visit.visits[1], self.my_visits[3])

    def testRemoveLastVisit(self):
        self.assertRaises(IndexError, self.tour_empty.removeLastVisit)
        self.tour_1_visit.removeLastVisit()
        self.assertEqual(len(self.tour_1_visit.visits), 0)

    def testReplayTour(self):
        tours_test_copy = copy.deepcopy(self.tours_test)
        for t in self.tours_test:
            t.replayTour()
        #Object contents do not change when replaying the tour immediately
        self.assertEqual(repr(self.tours_test), repr(tours_test_copy))

    def testIsAValidTour(self):
        self.assertTrue(self.tour_empty.isAValidTour())
        self.assertFalse(self.tour_sans_depot.isAValidTour())
        self.assertTrue(self.tour_1_visit.isAValidTour())

    def testSwapVisits(self):
        self.tour_1_visit.addToVisits(self.my_visits[3])
        #New visit has been added to index 1
        self.assertEqual(self.tour_1_visit.visits[1], self.my_visits[3])
        self.tour_1_visit.swapVisits(0, 1)
        #New visit is now on index 0
        self.assertEqual(self.tour_1_visit.visits[0], self.my_visits[3])

    def testFindCorRVisits(self):
        self.tour_1_visit.visits.append(self.visit_C)
        self.tour_1_visit.visits.append(self.my_visits[3])
        self.tour_1_visit.visits.append(self.visit_R)
        self.assertEqual(self.tour_1_visit.findCorRVisits(True, False), [1])
        self.assertEqual(self.tour_1_visit.findCorRVisits(False, True), [3])
        self.assertEqual(self.tour_1_visit.findCorRVisits(True, True), [1,3])
        self.assertEqual(self.tour_1_visit.findCorRVisits(False, False), [])

    def testBuildTour(self):
        self.assertRaises(ValueError, self.tour_1_visit.buildTour, "aaa", self.my_globals.list_visits, self.depot) #Cas mode invalide

    """
    def testFindNearestVisit(self):
        visit_near = Visit(998, "V998", 45.7640205, 4.8901686, 10)
        visit_far = Visit(999, "V999", 35.7640211, 14.8901678, 10)
        future_visits = [visit_near, visit_far]
        self.assertEqual(self.tour_1_visit.findNearestVisit(future_visits, self.tour_1_visit.starting_visit),
                         visit_near)

    def testFindNearestDepot(self):
        visit_near = Visit(998, "V998", 45.7640205, 4.8901686, 10)
        visit_far = Visit(999, "V999", 40.7640211, 9.8901678, 10)
        depot_near = Visit(0, "Depot", 35.7640211, 14.8901678, 10)
        future_visits = [visit_near, depot_near, visit_far]
        self.assertEqual(self.tour_1_visit.findNearestDepot(future_visits, self.tour_1_visit.starting_visit),
                         depot_near)
    """
