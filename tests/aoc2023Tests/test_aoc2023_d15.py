from unittest import TestCase

from aoc2023.d15 import quick_hash, load_tokens, part_one, parse_instruction, Operation
from aoc2023.d15 import apply_instruction, new_boxes, Lense, part_two
from tests.aoc2023Tests.aoc2023_common import get_test_file_path


class TestInstruction(TestCase):
    def test_parse_remove(self):
        instruction = parse_instruction("qp-")
        self.assertEqual(instruction.box_no, 1)
        self.assertEqual(instruction.lense, "qp")
        self.assertEqual(instruction.operation, Operation.REMOVE)

    def test_parse_add(self):
        instruction = parse_instruction("qp=3")
        self.assertEqual(instruction.box_no, 1)
        self.assertEqual(instruction.lense, "qp")
        self.assertEqual(instruction.operation, Operation.ADD)
        self.assertEqual(instruction.focal_length, 3)

class TestBoxes(TestCase):

    def test_single_add(self):
        instruction = parse_instruction("qp=3")
        boxes = new_boxes()
        apply_instruction(boxes, [instruction])
        self.assertEqual(boxes[1][0].label, "qp")
        self.assertEqual(boxes[1][0].focal_length, 3)

    def test_single_remove(self):
        instruction = parse_instruction("qp-")
        boxes = new_boxes()
        boxes[1] = [Lense(label="other", focal_length=1),
                    Lense(label="qp", focal_length=3),
                    Lense(label="trailing", focal_length=2)]
        apply_instruction(boxes, [instruction])
        self.assertEqual(boxes[1][0].label, "other")
        self.assertEqual(boxes[1][1].label, "trailing")

    def test_part_2_boxes(self):
        tokens = load_tokens(get_test_file_path("samples/d15.txt"))
        instructions = [parse_instruction(token) for token in tokens]
        boxes = new_boxes()
        apply_instruction(boxes, instructions)
        self.assertEqual(boxes[0][0].label, "rn")
        self.assertEqual(boxes[0][1].label, "cm")

        self.assertEqual(boxes[3][0].label, "ot")
        self.assertEqual(boxes[3][1].label, "ab")
        self.assertEqual(boxes[3][2].label, "pc")

    def test_part_two(self):
        tokens = load_tokens(get_test_file_path("samples/d15.txt"))
        self.assertEqual(part_two(tokens), 145)
class TestHash(TestCase):
    def test_hash(self):
        self.assertEqual(quick_hash("HASH"), 52)

    def test_load_tokens(self):
        tokens = load_tokens(get_test_file_path("samples/d15.txt"))
        self.assertEqual(tokens[0], "rn=1")
        self.assertEqual(tokens[-1], "ot=7")

    def test_part_one(self):
        tokens = load_tokens(get_test_file_path("samples/d15.txt"))
        self.assertEqual(part_one(tokens), 1320)
