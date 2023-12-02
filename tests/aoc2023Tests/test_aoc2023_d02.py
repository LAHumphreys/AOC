from unittest import TestCase

from aoc2023.d02 import load_games, Round, parse_round, part_one, game_power, part_two
from tests.aoc2023Tests.aoc2023_common import get_test_file_path


class TestCount(TestCase):
    def test_load_ids(self):
        games = load_games(get_test_file_path("samples/d02.txt"))
        self.assertEqual([game.id for game in games], [i for i in range(1, 6)])

    def test_load_rounds(self):
        games = load_games(get_test_file_path("samples/d02.txt"))
        expected = {
            0: [Round(blue=3, red=4), Round(red=1, green=2, blue=6), Round(green=2)],
            2: [Round(green=8, blue=6, red=20), Round(red=4, green=13, blue=5), Round(green=5, red=1)],
            4: [Round(green=3, blue=1, red=6), Round(red=1, green=2, blue=2)]
        }
        for idx, expected_rounds in expected.items():
            self.assertEqual(games[idx].rounds, expected_rounds)

    def test_round_parser(self):
        self.assertEqual(parse_round("3 blue, 4 red"), Round(blue=3, red=4))
        self.assertEqual(parse_round("8 green, 6 blue, 20 red"), Round(green=8, blue=6, red=20))
        self.assertEqual(parse_round("8 green"), Round(green=8, blue=0, red=0))
        pass

    def test_part_one(self):
        games = load_games(get_test_file_path("samples/d02.txt"))
        self.assertEqual(part_one(games), 8)

    def test_power(self):
        games = load_games(get_test_file_path("samples/d02.txt"))
        self.assertEqual(game_power(games[0]), 48)
        self.assertEqual(game_power(games[1]), 12)
        self.assertEqual(game_power(games[2]), 1560)
        self.assertEqual(game_power(games[3]), 630)
        self.assertEqual(game_power(games[4]), 36)

    def test_part_two(self):
        games = load_games(get_test_file_path("samples/d02.txt"))
        self.assertEqual(part_two(games), 2286)


