from unittest import TestCase

from aoc2023.d11 import load_galaxy, find_galaxies, galaxy_distance, expand_universe, part_one, part_two
from tests.aoc2023Tests.aoc2023_common import get_test_file_path


class TestGalaxies(TestCase):

    def test_expansion(self):
        universe = expand_universe(load_galaxy(get_test_file_path("samples/d11.txt")))
        galaxies = find_galaxies(universe)
        self.assertEqual(len(galaxies), 9)

    def test_distance(self):
        universe = expand_universe(load_galaxy(get_test_file_path("samples/d11.txt")))
        galaxies = find_galaxies(universe)
        self.assertEqual(galaxy_distance(galaxies[4], galaxies[8]), 9)
        self.assertEqual(galaxy_distance(galaxies[0], galaxies[6]), 15)
        self.assertEqual(galaxy_distance(galaxies[2], galaxies[5]), 17)
        self.assertEqual(galaxy_distance(galaxies[7], galaxies[8]), 5)

    def test_part_one(self):
        universe = load_galaxy(get_test_file_path("samples/d11.txt"))
        self.assertEqual(part_one(universe), 374)

    def test_part_two(self):
        universe = load_galaxy(get_test_file_path("samples/d11.txt"))
        self.assertEqual(part_two(universe, 10), 1030)
        self.assertEqual(part_two(universe, 100), 8410)

