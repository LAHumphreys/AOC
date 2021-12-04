from unittest import TestCase

from aoc2021.d04 import BingoCard, load_input, part_one, GameResult, Input, part_two
from tests.aoc2021Tests.aoc2021_common import get_test_file_path


class TestCount(TestCase):
    def test_mid_row(self):
        sample = [
            "10 16 15 9  19",
            "18 8  23 26 20",
            "14 21 17 24 4",
            "22 11 13 6  5",
            "2  0  12 3  7"
        ]
        card = BingoCard(sample)
        self.assertFalse(card.board_complete())

        self.assertFalse(card.call_number(14))
        self.assertFalse(card.call_number(4))
        self.assertFalse(card.call_number(17))
        self.assertFalse(card.call_number(21))
        self.assertTrue(card.call_number(24))

    def test_mid_col(self):
        sample = [
            "10 16 15 9  19",
            "18 8  23 26 20",
            "14 21 17 24 4",
            "22 11 13 6  5",
            "2  0  12 3  7"
        ]
        card = BingoCard(sample)
        self.assertFalse(card.board_complete())

        self.assertFalse(card.call_number(15))
        self.assertFalse(card.call_number(23))
        self.assertFalse(card.call_number(17))
        self.assertFalse(card.call_number(13))
        self.assertTrue(card.call_number(12))

    def test_sample_sum(self):
        sample = [
            "14 21 17 24 4",
            "10 16 15 9  19",
            "18 8  23 26 20",
            "22 11 13 6  5",
            "2  0  12 3  7"
        ]
        card = BingoCard(sample)
        for number in [7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21]:
            self.assertFalse(card.call_number(number))
        self.assertTrue(card.call_number(24))
        self.assertEqual(sum(card.uncalled_numbers()), 188)

    def test_leading_whitespace(self):
        sample = [
            " 4 21 17 24 4",
            "10 16 15 9  19",
            "18 8  23 26 20",
            "22 11 13 6  5",
            "2  0  12 3  7"
        ]
        card = BingoCard(sample)
        for number in [7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21]:
            self.assertFalse(card.call_number(number))
        self.assertTrue(card.call_number(24))
        self.assertEqual(sum(card.uncalled_numbers()), 188)

    def testLoad(self):
        input = load_input(get_test_file_path("samples/d04.txt"))
        self.assertListEqual(input.numbers, [7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1])
        self.assertEqual(len(input.cards), 3)

        sample_card:BingoCard = input.cards[2]
        for number in input.numbers[0:11]:
            self.assertFalse(sample_card.call_number(number))
        self.assertTrue(sample_card.call_number(24))
        self.assertEqual(sum(sample_card.uncalled_numbers()), 188)

    def test_sample_game(self):
        game_input: Input = load_input(get_test_file_path("samples/d04.txt"))
        result: GameResult = part_one(game_input)

        self.assertEqual(result.final_number, 24)
        self.assertEqual(result.score, 4512)

    def test_sample_last_game(self):
        game_input: Input = load_input(get_test_file_path("samples/d04.txt"))
        result: GameResult = part_two(game_input)

        self.assertEqual(result.final_number, 13)
        self.assertEqual(result.score, 1924)


