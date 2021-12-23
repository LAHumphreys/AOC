from unittest import TestCase

from aoc2021.d21 import get_new_deterministic_die, play, Game, Player
from aoc2021.d21 import advance_player, score_game
from aoc2021.d21 import starting_universe, dirac_turn, possible_rolls, run_dirac_game
from tests.aoc2021Tests.aoc2021_common import get_test_file_path

class Dice(TestCase):
    def test_dice(self):
        first = get_new_deterministic_die()
        second = get_new_deterministic_die()
        self.assertEqual(next(first), 1)
        self.assertEqual(next(first), 2)
        self.assertEqual(next(first), 3)
        self.assertEqual(next(second), 1)
        self.assertEqual(next(second), 2)
        self.assertEqual(next(second), 3)
        self.assertEqual(next(first), 4)
        self.assertEqual(next(second), 4)
        for i in range(5, 100):
            self.assertEqual(next(first), i)
            self.assertEqual(next(second), i)
        self.assertEqual(next(first), 100)
        self.assertEqual(next(second), 100)
        self.assertEqual(next(first), 1)
        self.assertEqual(next(second), 1)

    def test_advance(self):
        game = Game(player_1=Player(space=4), player_2=Player(space=8))
        die = get_new_deterministic_die()
        advance_player(game.player_1, die)
        self.assertEqual(game.player_1.space, 10)
        self.assertEqual(game.player_1.score, 10)
        advance_player(game.player_2, die)
        self.assertEqual(game.player_2.space, 3)
        self.assertEqual(game.player_2.score, 3)

    def test_play(self):
        game = Game(player_1=Player(space=4), player_2=Player(space=8))
        play(get_new_deterministic_die(), game)
        self.assertEqual(game.player_1.score, 1000)
        self.assertEqual(game.player_2.score, 745)
        self.assertEqual(game.rolls, 993)
        self.assertEqual(score_game(game), 739785)


class DiractGame(TestCase):
    def test_diract_turn(self):
        game = next(iter(starting_universe(1, 2).in_play))
        multiverse = dirac_turn(game, possible_rolls())
        self.assertEqual(len(multiverse), 7)
        # There is exactly 1 universe where player 1 gets a total of 3 1s
        expected_games = {
            Game(rolls=3, player_1=Player(space=4, score=4), player_2=Player(space=2, score=0)): 1,
            Game(rolls=3, player_1=Player(space=5, score=5), player_2=Player(space=2, score=0)): 3,
            Game(rolls=3, player_1=Player(space=6, score=6), player_2=Player(space=2, score=0)): 6,
            Game(rolls=3, player_1=Player(space=7, score=7), player_2=Player(space=2, score=0)): 7,
            Game(rolls=3, player_1=Player(space=8, score=8), player_2=Player(space=2, score=0)): 6,
            Game(rolls=3, player_1=Player(space=9, score=9), player_2=Player(space=2, score=0)): 3,
            Game(rolls=3, player_1=Player(space=10, score=10), player_2=Player(space=2, score=0)): 1
        }
        self.assertEqual(expected_games, multiverse)

    def test_diract_turn_player_2(self):
        game = next(iter(starting_universe(1, 2).in_play))
        game.rolls = 3
        multiverse = dirac_turn(game, possible_rolls())
        self.assertEqual(len(multiverse), 7)
        # There is exactly 1 universe where player 1 gets a total of 3 1s
        expected_games = {
            Game(rolls=6, player_2=Player(space=5, score=5), player_1=Player(space=1, score=0)): 1,
            Game(rolls=6, player_2=Player(space=6, score=6), player_1=Player(space=1, score=0)): 3,
            Game(rolls=6, player_2=Player(space=7, score=7), player_1=Player(space=1, score=0)): 6,
            Game(rolls=6, player_2=Player(space=8, score=8), player_1=Player(space=1, score=0)): 7,
            Game(rolls=6, player_2=Player(space=9, score=9), player_1=Player(space=1, score=0)): 6,
            Game(rolls=6, player_2=Player(space=10, score=10), player_1=Player(space=1, score=0)): 3,
            Game(rolls=6, player_2=Player(space=1, score=1), player_1=Player(space=1, score=0)): 1
        }
        self.assertEqual(expected_games, multiverse)

    def test_dirac_game(self):
        the_game = starting_universe(4, 8)
        run_dirac_game(the_game)
        self.assertEqual(444356092776315, sum((num_universes) for _, num_universes in the_game.player1_victories.items()))
        self.assertEqual(341960390180808, sum((num_universes) for _, num_universes in the_game.player2_victories.items()))



