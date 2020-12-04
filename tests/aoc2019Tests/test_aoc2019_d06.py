from unittest import TestCase

from aoc2019.d06 import parentChildRegex, OrbitCounter


class Test_Splitter(TestCase):
    def test_example(self):
        m = parentChildRegex.match("COM)B")
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), "COM")
        self.assertEqual(m.group(2), "B")


class Test_OrbitCounter(TestCase):
    def test_SingleOrbit(self):
        counter = OrbitCounter()
        counter.add("COM", "B")
        self.assertEqual(counter.get_orbits(), 1)

    def test_TwoSingleOrbit2(self):
        counter = OrbitCounter()
        counter.add("COM", "B")
        counter.add("COM", "C")
        self.assertEqual(counter.get_orbits(), 2)

    def test_PlanetWithMoon(self):
        counter = OrbitCounter()
        counter.add("SUN", "EARTH")
        counter.add("EARTH", "MOON")
        self.assertEqual(counter.get_orbits(), 3)

    def test_example(self):
        counter = OrbitCounter()
        counter.add("COM", "B")
        counter.add("B", "C")
        counter.add("C", "D")
        counter.add("D", "E")
        counter.add("E", "F")
        counter.add("B", "G")
        counter.add("G", "H")
        counter.add("D", "I")
        counter.add("E", "J")
        counter.add("J", "K")
        counter.add("K", "L")

        self.assertEqual(counter.get_orbits(), 42)

    def test_example2(self):
        counter = OrbitCounter()
        counter.add("COM", "B")
        counter.add("B", "C")
        counter.add("C", "D")
        counter.add("D", "E")
        counter.add("E", "F")
        counter.add("B", "G")
        counter.add("G", "H")
        counter.add("D", "I")
        counter.add("E", "J")
        counter.add("J", "K")
        counter.add("K", "L")
        counter.add("K", "YOU")
        counter.add("I", "SAN")

        self.assertEqual(counter.get_hops("YOU", "SAN"), 4)
