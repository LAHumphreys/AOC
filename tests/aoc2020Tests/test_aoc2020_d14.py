from unittest import TestCase

from aoc2020.d14 import Mask, load_pogram, run_program, checksum_memory, run_program_version_2
from tests.aoc2020Tests.aoc2020_common import GetTestFilePath


class TestMask(TestCase):
    def test_example1(self):
        mask = Mask()
        mask.set_mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X")
        self.assertEqual(73, mask.get_masked_value(11))
        self.assertEqual(101, mask.get_masked_value(101))
        self.assertEqual(64, mask.get_masked_value(0))

    def test_update_mask(self):
        mask = Mask()
        self.assertEqual(11, mask.get_masked_value(11))
        self.assertEqual(101, mask.get_masked_value(101))
        self.assertEqual(0, mask.get_masked_value(0))
        mask.set_mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X")
        self.assertEqual(73, mask.get_masked_value(11))
        self.assertEqual(101, mask.get_masked_value(101))
        self.assertEqual(64, mask.get_masked_value(0))

    def test_load(self):
        program = load_pogram(GetTestFilePath("samples/d14/sample1.txt"))
        expected = [
            (-1, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"),
            (8, 11),
            (7, 101),
            (8, 0)
        ]
        self.assertListEqual(expected, program)

    def test_execute(self):
        program = load_pogram(GetTestFilePath("samples/d14/sample1.txt"))
        memory = run_program(program)
        expected = {
            8: 64,
            7: 101
        }
        self.assertDictEqual(expected, memory)
        self.assertEqual(165, checksum_memory(memory))

    def test_address_example_1(self):
        mask = Mask()
        mask.set_mask("000000000000000000000000000000X1001X")
        expected = [26, 27, 58, 59]
        addresses = mask.get_masked_addresses(42)
        addresses.sort()
        self.assertListEqual(expected, addresses)

    def test_address_example_2(self):
        mask = Mask()
        mask.set_mask("00000000000000000000000000000000X0XX")
        expected = [16, 17, 18, 19, 24, 25, 26, 27]
        addresses = mask.get_masked_addresses(26)
        addresses.sort()
        self.assertListEqual(expected, addresses)

    def test_execute_version_2(self):
        program = load_pogram(GetTestFilePath("samples/d14/sample2.txt"))
        memory = run_program_version_2(program)
        expected = {
            16: 1,
            17: 1,
            18: 1,
            19: 1,
            24: 1,
            25: 1,
            26: 1,
            27: 1,
            58: 100,
            59: 100,
        }
        self.assertDictEqual(expected, memory)
        self.assertEqual(208, checksum_memory(memory))
