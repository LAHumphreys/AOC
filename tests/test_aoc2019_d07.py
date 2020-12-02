from aoc2019.d07 import Thruster, PhaseAmpMismatch, FindMaxThrust, FeedbackThruster, FindMaxFeedbackThrust

from unittest import TestCase

class Test_ThrusterCompute(TestCase):
    def test_InvalidPhases(self):
        thruster = Thruster([])
        self.assertRaises(PhaseAmpMismatch, lambda: thruster.ComputeThrust([]))
        self.assertRaises(PhaseAmpMismatch, lambda: thruster.ComputeThrust([1]))
        self.assertRaises(PhaseAmpMismatch, lambda: thruster.ComputeThrust([1,2]))
        self.assertRaises(PhaseAmpMismatch, lambda: thruster.ComputeThrust([1,2,3]))
        self.assertRaises(PhaseAmpMismatch, lambda: thruster.ComputeThrust([1,2,3,4]))
        self.assertRaises(PhaseAmpMismatch, lambda: thruster.ComputeThrust([1,2,3,4,5,6]))

    def test_Example1(self):
        thruster = Thruster([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0])
        self.assertEqual(thruster.ComputeThrust([4,3,2,1,0]), 43210)

    def test_Example2(self):
        code = [3,23,3,24,1002,24,10,24,1002,23,-1,23, 101,5,23,23,1,24,23,23,4,23,99,0,0]
        thruster = Thruster(code)
        self.assertEqual(thruster.ComputeThrust([0,1,2,3,4]), 54321)

    def test_Example3(self):
        code = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33, 1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
        thruster = Thruster(code)
        self.assertEqual(thruster.ComputeThrust([1,0,4,3,2]), 65210)

class Test_MaxThrust(TestCase):
    def test_Example1(self):
        code = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
        self.assertEqual(FindMaxThrust(code), 43210)

    def test_Example2(self):
        code = [3,23,3,24,1002,24,10,24,1002,23,-1,23, 101,5,23,23,1,24,23,23,4,23,99,0,0]
        self.assertEqual(FindMaxThrust(code), 54321)

    def test_Example3(self):
        code = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33, 1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
        self.assertEqual(FindMaxThrust(code), 65210)

class Test_FeedbackThruster(TestCase):
    def test_InvalidPhases(self):
        thruster = FeedbackThruster([])
        self.assertRaises(PhaseAmpMismatch, lambda: thruster.ComputeThrust([]))
        self.assertRaises(PhaseAmpMismatch, lambda: thruster.ComputeThrust([1]))
        self.assertRaises(PhaseAmpMismatch, lambda: thruster.ComputeThrust([1,2]))
        self.assertRaises(PhaseAmpMismatch, lambda: thruster.ComputeThrust([1,2,3]))
        self.assertRaises(PhaseAmpMismatch, lambda: thruster.ComputeThrust([1,2,3,4]))
        self.assertRaises(PhaseAmpMismatch, lambda: thruster.ComputeThrust([1,2,3,4,5,6]))

    def test_Example1(self):
        thruster = FeedbackThruster([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26, 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5])
        self.assertEqual(thruster.ComputeThrust([9,8,7,6,5]), 139629729)

    def test_Example2(self):
        thruster = FeedbackThruster([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54, -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4, 53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10])
        self.assertEqual(thruster.ComputeThrust([9,7,8,5,6]), 18216)

class Test_MaxFeedbackThruster(TestCase):
    def test_Example1(self):
        code = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26, 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
        self.assertEqual(FindMaxFeedbackThrust(code), 139629729)

    def test_Example1(self):
        code = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54, -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4, 53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
        self.assertEqual(FindMaxFeedbackThrust(code), 18216)

