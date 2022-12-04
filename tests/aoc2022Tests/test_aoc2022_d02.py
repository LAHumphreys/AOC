from unittest import TestCase

from aoc2022.d02 import RPS, play, load_rounds, Round, play_rounds
from aoc2022.d02 import load_rounds_2, Round2, Result, play_2, play_rounds_2
from tests.aoc2022Tests.aoc2022_common import get_test_file_path


class TestPlay(TestCase):
    def test_draw(self):
        self.assertEqual(play(RPS.ROCK, RPS.ROCK), 4)
        self.assertEqual(play(RPS.PAPER, RPS.PAPER), 5)
        self.assertEqual(play(RPS.SCISSORS, RPS.SCISSORS), 6)

    def test_win(self):
        self.assertEqual(play(RPS.ROCK, RPS.SCISSORS), 7)
        self.assertEqual(play(RPS.PAPER, RPS.ROCK), 8)
        self.assertEqual(play(RPS.SCISSORS, RPS.PAPER), 9)

    def test_lose(self):
        self.assertEqual(play(RPS.ROCK, RPS.PAPER), 1)
        self.assertEqual(play(RPS.PAPER, RPS.SCISSORS), 2)
        self.assertEqual(play(RPS.SCISSORS, RPS.ROCK), 3)


class TestPlay2(TestCase):
    def test_draw(self):
        self.assertEqual(play_2(RPS.ROCK, Result.DRAW), 4)
        self.assertEqual(play_2(RPS.PAPER, Result.DRAW), 5)
        self.assertEqual(play_2(RPS.SCISSORS, Result.DRAW), 6)

    def test_lose(self):
        self.assertEqual(play_2(RPS.ROCK, Result.LOSE), 3)
        self.assertEqual(play_2(RPS.PAPER, Result.LOSE), 1)
        self.assertEqual(play_2(RPS.SCISSORS, Result.LOSE), 2)

    def test_win(self):
        self.assertEqual(play_2(RPS.ROCK, Result.WIN), 8)
        self.assertEqual(play_2(RPS.PAPER, Result.WIN), 9)
        self.assertEqual(play_2(RPS.SCISSORS, Result.WIN), 7)


class TestLoad(TestCase):
    def test_sample_2(self):
        rounds = load_rounds_2(get_test_file_path("samples/d02.txt"))
        expected = [Round2(result=Result.DRAW, opponent=RPS.ROCK),
                    Round2(result=Result.LOSE, opponent=RPS.PAPER),
                    Round2(result=Result.WIN, opponent=RPS.SCISSORS)]
        self.assertListEqual(rounds, expected)

    def test_sample(self):
        rounds = load_rounds(get_test_file_path("samples/d02.txt"))
        expected = [Round(you=RPS.PAPER, opponent=RPS.ROCK),
                    Round(you=RPS.ROCK, opponent=RPS.PAPER),
                    Round(you=RPS.SCISSORS, opponent=RPS.SCISSORS)]
        self.assertListEqual(rounds, expected)


class TestPlayRounds(TestCase):
    def test_sample(self):
        rounds = load_rounds(get_test_file_path("samples/d02.txt"))
        self.assertEqual(play_rounds(rounds), 15)

    def test_sample_2(self):
        rounds = load_rounds_2(get_test_file_path("samples/d02.txt"))
        self.assertEqual(play_rounds_2(rounds), 12)

