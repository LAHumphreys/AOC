from unittest import TestCase

from aoc2020.d16 import TicketData, number_is_valid, validate_fields, sum_invalid
from aoc2020.d16 import determine_fields
from tests.aoc2020Tests.aoc2020_common import GetTestFilePath


class PartOne(TestCase):
    def test_parser_your_ticket(self):
        path = GetTestFilePath("samples/d16/sample1.txt")
        with open(path) as file:
            lines = file.read().split("\n")
        data = TicketData(lines)
        self.assertListEqual(data.get_ticket(), [7, 1, 14])

    def test_parser_other_tickets(self):
        path = GetTestFilePath("samples/d16/sample1.txt")
        with open(path) as file:
            lines = file.read().split("\n")
        data = TicketData(lines)
        tickets = [
            [7, 3, 47],
            [40, 4, 50],
            [55, 2, 20],
            [38, 6, 12]
        ]
        self.assertListEqual(tickets, data.get_other_tickets())

    def test_parser_all_tickets(self):
        path = GetTestFilePath("samples/d16/sample1.txt")
        with open(path) as file:
            lines = file.read().split("\n")
        data = TicketData(lines)
        tickets = [
            [7, 1, 14],
            [7, 3, 47],
            [40, 4, 50],
            [55, 2, 20],
            [38, 6, 12]
        ]
        self.assertListEqual(tickets, data.get_all_tickets())

    def test_parser_rules(self):
        path = GetTestFilePath("samples/d16/sample1.txt")
        with open(path) as file:
            lines = file.read().split("\n")
        data = TicketData(lines)
        rules = {
            "class": ((1, 3), (5, 7)),
            "row": ((6, 11), (33, 44)),
            "seat": ((13, 40), (45, 50))
        }
        self.assertDictEqual(rules, data.get_rules())

    def test_number_is_valid(self):
        rule = ((1, 3), (5, 7))
        self.assertFalse(number_is_valid(rule, 0))
        self.assertTrue(number_is_valid(rule, 1))
        self.assertTrue(number_is_valid(rule, 2))
        self.assertTrue(number_is_valid(rule, 3))
        self.assertFalse(number_is_valid(rule, 4))
        self.assertTrue(number_is_valid(rule, 5))
        self.assertTrue(number_is_valid(rule, 6))
        self.assertTrue(number_is_valid(rule, 7))
        self.assertFalse(number_is_valid(rule, 8))

    def test_validate_fields(self):
        rules = {
            "class": ((1, 3), (5, 7)),
            "row": ((6, 11), (33, 44)),
            "seat": ((13, 40), (45, 50))
        }
        ticket = [40, 4, 50]
        valid = [["row", "seat"], [], ["seat"]]
        self.assertListEqual(valid, validate_fields(rules, ticket))

    def test_sum_invalid(self):
        path = GetTestFilePath("samples/d16/sample1.txt")
        with open(path) as file:
            lines = file.read().split("\n")
        data = TicketData(lines)
        self.assertEqual(71, sum_invalid(data))

    def test_determine_fields(self):
        path = GetTestFilePath("samples/d16/sample2.txt")
        with open(path) as file:
            lines = file.read().split("\n")
        data = TicketData(lines)
        expected = ["row", "class", "seat"]
        self.assertListEqual(expected, determine_fields(data))

    def test_determine_fields_recursive(self):
        path = GetTestFilePath("samples/d16/sample3.txt")
        with open(path) as file:
            lines = file.read().split("\n")
        data = TicketData(lines)
        expected = ['zone',
                    'departure time',
                    'departure platform',
                    'train',
                    'arrival track',
                    'departure track',
                    'arrival station',
                    'seat',
                    'price',
                    'wagon',
                    'route',
                    'type',
                    'row',
                    'departure location',
                    'class',
                    'departure date',
                    'arrival location',
                    'arrival platform',
                    'duration',
                    'departure station']

        self.assertListEqual(expected, determine_fields(data))
