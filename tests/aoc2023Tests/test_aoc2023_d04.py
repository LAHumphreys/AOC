from unittest import TestCase

from aoc2023.d04 import load_cards, parse_card, get_winning
from aoc2023.d04 import part_two
from tests.aoc2023Tests.aoc2023_common import get_test_file_path


class TestCount(TestCase):
    def test_valid_parts(self):
        cards = load_cards(get_test_file_path("samples/d04.txt"))
        self.assertEqual(len(cards), 6)
        self.assertEqual(cards[4].id, 5)
        self.assertEqual(cards[4].card_numbers, [87, 83, 26, 28, 32 ])
        self.assertEqual(cards[4].winning_numbers, [88, 30, 70, 12, 93, 22, 82, 36])

    def test_parse(self):
        card = parse_card("Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36")
        self.assertEqual(card.id, 5)
        self.assertEqual(card.card_numbers, [87, 83, 26, 28, 32 ])
        self.assertEqual(card.winning_numbers, [88, 30, 70, 12, 93, 22, 82, 36])

    def test_winning(self):
        cards = load_cards(get_test_file_path("samples/d04.txt"))
        self.assertEqual(get_winning(cards[1]), [32, 61])
        self.assertEqual(get_winning(cards[5]), [])

    def test_part_two(self):
        cards = load_cards(get_test_file_path("samples/d04.txt"))
        self.assertEqual(part_two(cards), 30)



