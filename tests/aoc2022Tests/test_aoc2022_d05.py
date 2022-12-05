from unittest import TestCase

from aoc2022.d05 import load_stacks, Instruction, move_stack
from aoc2022.d05 import SupplyStacks, get_code, move_full_stack
from tests.aoc2022Tests.aoc2022_common import get_test_file_path


class TestLoad(TestCase):
    def setUp(self) -> None:
        self.instructions = [
            Instruction(count=1, source=2, destination=1),
            Instruction(count=3, source=1, destination=3),
            Instruction(count=2, source=2, destination=1),
            Instruction(count=1, source=1, destination=2)
        ]

    def test_load_all_stacks(self):
        stacks, _ = load_stacks(get_test_file_path("samples/d05.txt"))
        self.assertDictEqual(stacks.stacks, {
            1: ["Z", "N"],
            2: ["M", "C", "D"],
            3: ["P"],
        })

    def test_load_all_instructions(self):
        _, instructions = load_stacks(get_test_file_path("samples/d05.txt"))
        self.assertListEqual(self.instructions, instructions)


class TestMove(TestCase):
    def test_step_1(self):
        stacks = SupplyStacks(stacks={
            1: ["Z", "N"],
            2: ["M", "C", "D"],
            3: ["P"],
        })
        expected = {
            1: ["Z", "N", "D"],
            2: ["M", "C"],
            3: ["P"],
        }
        instruction = Instruction(count=1, source=2, destination=1)
        move_stack(instruction, stacks)
        self.assertDictEqual(stacks.stacks, expected)

    def test_step_2(self):
        stacks = SupplyStacks(stacks={
            1: ["Z", "N", "D"],
            2: ["M", "C"],
            3: ["P"],
        })
        expected = {
            1: [],
            2: ["M", "C"],
            3: ["P", "D", "N", "Z"],
        }
        instruction = Instruction(count=3, source=1, destination=3)
        move_stack(instruction, stacks)
        self.assertDictEqual(stacks.stacks, expected)

    def test_step_3(self):
        stacks = SupplyStacks(stacks={
            1: [],
            2: ["M", "C"],
            3: ["P", "D", "N", "Z"],
        })
        expected = {
            1: ["C", "M"],
            2: [],
            3: ["P", "D", "N", "Z"],
        }
        instruction = Instruction(count=2, source=2, destination=1)
        move_stack(instruction, stacks)
        self.assertDictEqual(stacks.stacks, expected)

    def test_step_4(self):
        stacks = SupplyStacks(stacks={
            1: ["C", "M"],
            2: [],
            3: ["P", "D", "N", "Z"],
        })
        expected = {
            1: ["C"],
            2: ["M"],
            3: ["P", "D", "N", "Z"],
        }
        instruction = Instruction(count=1, source=1, destination=2)
        move_stack(instruction, stacks)
        self.assertDictEqual(stacks.stacks, expected)


class TestMoveFull(TestCase):
    def test_step_1(self):
        stacks = SupplyStacks(stacks={
            1: ["Z", "N"],
            2: ["M", "C", "D"],
            3: ["P"],
        })
        expected = {
            1: ["Z", "N", "D"],
            2: ["M", "C"],
            3: ["P"],
        }
        instruction = Instruction(count=1, source=2, destination=1)
        move_full_stack(instruction, stacks)
        self.assertDictEqual(stacks.stacks, expected)

    def test_step_2(self):
        stacks = SupplyStacks(stacks={
            1: ["Z", "N", "D"],
            2: ["M", "C"],
            3: ["P"],
        })
        expected = {
            1: [],
            2: ["M", "C"],
            3: ["P", "Z", "N", "D"],
        }
        instruction = Instruction(count=3, source=1, destination=3)
        move_full_stack(instruction, stacks)
        self.assertDictEqual(stacks.stacks, expected)

    def test_step_3(self):
        stacks = SupplyStacks(stacks={
            1: [],
            2: ["M", "C"],
            3: ["P", "Z", "N", "D"],
        })
        expected = {
            1: ["M", "C"],
            2: [],
            3: ["P", "Z", "N", "D"],
        }
        instruction = Instruction(count=2, source=2, destination=1)
        move_full_stack(instruction, stacks)
        self.assertDictEqual(stacks.stacks, expected)

    def test_step_4(self):
        stacks = SupplyStacks(stacks={
            1: ["M", "C"],
            2: [],
            3: ["P", "D", "N", "Z"],
        })
        expected = {
            1: ["M"],
            2: ["C"],
            3: ["P", "D", "N", "Z"],
        }
        instruction = Instruction(count=1, source=1, destination=2)
        move_full_stack(instruction, stacks)
        self.assertDictEqual(stacks.stacks, expected)


class TestCode(TestCase):
    def test_step_4(self):
        stacks = SupplyStacks(stacks={
            1: ["C"],
            2: ["M"],
            3: ["P", "D", "N", "Z"],
        })
        self.assertEqual(get_code(stacks), "CMZ")
