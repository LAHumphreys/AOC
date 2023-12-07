from unittest import TestCase

from aoc2023.d07 import HandType, get_hand_type, load_hands, part_one, convert_jokers, part_two
from tests.aoc2023Tests.aoc2023_common import get_test_file_path


class TestCardType(TestCase):

    def test_high_card(self):
        self.assertEqual(get_hand_type("23456"), HandType.HIGH_CARD)

    def test_one_pair(self):
        self.assertEqual(get_hand_type("A23A4"), HandType.ONE_PAIR)

    def test_two_pair(self):
        self.assertEqual(get_hand_type("23432"), HandType.TWO_PAIR)

    def test_three_of_a_kind(self):
        self.assertEqual(get_hand_type("TTT98"), HandType.THREE_OF_A_KIND)

    def test_full_house(self):
        self.assertEqual(get_hand_type("23332"), HandType.FULL_HOUSE)

    def test_four_of_a_kind(self):
        self.assertEqual(get_hand_type("AA8AA"), HandType.FOUR_OF_A_KIND)

    def test_five_of_a_kind(self):
        self.assertEqual(get_hand_type("AAAAA"), HandType.FIVE_OF_A_KIND)


class TestLoad(TestCase):

    def test_first_hand(self):
        hands = load_hands(get_test_file_path("samples/d07.txt"))
        self.assertEqual(hands[0].bid, 765)
        self.assertEqual(hands[0].type, HandType.ONE_PAIR)
        self.assertEqual(hands[0].hand_str, "32T3K")

    def test_part_one(self):
        hands = load_hands(get_test_file_path("samples/d07.txt"))
        self.assertEqual(part_one(hands), 6440)


class TestJokers(TestCase):

    def test_first_hand(self):
        hands = load_hands(get_test_file_path("samples/d07.txt"))
        joker_hand = convert_jokers(hands[0])
        self.assertEqual(joker_hand.type, HandType.ONE_PAIR)
        self.assertEqual(joker_hand.priority_string, hands[0].priority_string)

    def test_second_hand(self):
        hands = load_hands(get_test_file_path("samples/d07.txt"))
        joker_hand = convert_jokers(hands[1])
        self.assertEqual(joker_hand.type, HandType.FOUR_OF_A_KIND)

    def test_third_hand(self):
        hands = load_hands(get_test_file_path("samples/d07.txt"))
        joker_hand = convert_jokers(hands[2])
        self.assertEqual(joker_hand.type, HandType.TWO_PAIR)

    def test_fourth_hand(self):
        hands = load_hands(get_test_file_path("samples/d07.txt"))
        joker_hand = convert_jokers(hands[3])
        self.assertEqual(joker_hand.type, HandType.FOUR_OF_A_KIND)

    def test_fith_hand(self):
        hands = load_hands(get_test_file_path("samples/d07.txt"))
        joker_hand = convert_jokers(hands[4])
        self.assertEqual(joker_hand.type, HandType.FOUR_OF_A_KIND)

    def test_part_two(self):
        hands = load_hands(get_test_file_path("samples/d07.txt"))
        self.assertEqual(part_two(hands), 5905)

