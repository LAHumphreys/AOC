from aoc2019.d06 import parentChildRegex, OrbitCounter

from unittest import TestCase

class Test_Splitter(TestCase):
    def test_example(self):
        m = parentChildRegex.match("COM)B")
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), "COM")
        self.assertEqual(m.group(2), "B")

class Test_OrbitCounter(TestCase):
    def test_SingleOrbit(self):
        counter = OrbitCounter()
        counter.Add("COM", "B")
        self.assertEqual(counter.GetOrbits(), 1)

    def test_TwoSingleOrbit2(self):
        counter = OrbitCounter()
        counter.Add("COM", "B")
        counter.Add("COM", "C")
        self.assertEqual(counter.GetOrbits(), 2)

    def test_PlanetWithMoon(self):
        counter = OrbitCounter()
        counter.Add("SUN", "EARTH")
        counter.Add("EARTH", "MOON")
        self.assertEqual(counter.GetOrbits(), 3)

    def test_example(self):
        counter = OrbitCounter()
        counter.Add("COM", "B")
        counter.Add("B", "C")
        counter.Add("C", "D")
        counter.Add("D", "E")
        counter.Add("E", "F")
        counter.Add("B", "G")
        counter.Add("G", "H")
        counter.Add("D", "I")
        counter.Add("E", "J")
        counter.Add("J", "K")
        counter.Add("K", "L")

        self.assertEqual(counter.GetOrbits(), 42)

    def test_example2(self):
        counter = OrbitCounter()
        counter.Add("COM", "B")
        counter.Add("B", "C")
        counter.Add("C", "D")
        counter.Add("D", "E")
        counter.Add("E", "F")
        counter.Add("B", "G")
        counter.Add("G", "H")
        counter.Add("D", "I")
        counter.Add("E", "J")
        counter.Add("J", "K")
        counter.Add("K", "L")
        counter.Add("K", "YOU")
        counter.Add("I", "SAN")

        self.assertEqual(counter.GetHops("YOU", "SAN"), 4)
