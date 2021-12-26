from unittest import TestCase

from aoc2021.d24 import Instruction, InstructionType, decode, track_dependencies, apply_bounded_instruction, reduce_bounds
from aoc2021.d24 import reduce_bounds_from_below
from aoc2021.d24 import BoundedValue
from tests.aoc2021Tests.aoc2021_common import get_test_file_path


class Loader(TestCase):
    def test_input(self):
        instruction = decode("inp x")
        self.assertEqual(instruction.type, InstructionType.INPUT)
        self.assertEqual(instruction.source_register, None)
        self.assertEqual(instruction.source_value, None)
        self.assertEqual(instruction.target_register, "x")
        self.assertEqual(instruction.source_value, None)

    def test_add(self):
        instruction = decode("add z w")
        self.assertEqual(instruction.type, InstructionType.ADD)
        self.assertEqual(instruction.source_register, "w")
        self.assertEqual(instruction.source_value, None)
        self.assertEqual(instruction.target_register, "z")
        self.assertEqual(instruction.source_value, None)

        instruction = decode("add z 2")
        self.assertEqual(instruction.type, InstructionType.ADD)
        self.assertEqual(instruction.source_register, None)
        self.assertEqual(instruction.source_value, 2)
        self.assertEqual(instruction.target_register, "z")

    def test_mul(self):
        instruction = decode("mul z w")
        self.assertEqual(instruction.type, InstructionType.MUL)
        self.assertEqual(instruction.source_register, "w")
        self.assertEqual(instruction.source_value, None)
        self.assertEqual(instruction.target_register, "z")
        self.assertEqual(instruction.source_value, None)

        instruction = decode("mul z 2")
        self.assertEqual(instruction.type, InstructionType.MUL)
        self.assertEqual(instruction.source_register, None)
        self.assertEqual(instruction.source_value, 2)
        self.assertEqual(instruction.target_register, "z")

    def test_mul_zero(self):
        instruction = decode("mul a 0")
        self.assertEqual(instruction.type, InstructionType.SET)
        self.assertEqual(instruction.source_register, None)
        self.assertEqual(instruction.source_value, 0)
        self.assertEqual(instruction.target_register, "a")

    def test_div(self):
        instruction = decode("div z w")
        self.assertEqual(instruction.type, InstructionType.DIV)
        self.assertEqual(instruction.source_register, "w")
        self.assertEqual(instruction.source_value, None)
        self.assertEqual(instruction.target_register, "z")
        self.assertEqual(instruction.source_value, None)

        instruction = decode("div z 2")
        self.assertEqual(instruction.type, InstructionType.DIV)
        self.assertEqual(instruction.source_register, None)
        self.assertEqual(instruction.source_value, 2)
        self.assertEqual(instruction.target_register, "z")

    def test_div_one(self):
        instruction = decode("div z z")
        self.assertEqual(instruction.type, InstructionType.SET)
        self.assertEqual(instruction.source_register, None)
        self.assertEqual(instruction.source_value, 1)
        self.assertEqual(instruction.target_register, "z")

    def test_mod(self):
        instruction = decode("mod z w")
        self.assertEqual(instruction.type, InstructionType.MOD)
        self.assertEqual(instruction.source_register, "w")
        self.assertEqual(instruction.source_value, None)
        self.assertEqual(instruction.target_register, "z")

        instruction = decode("mod z 2")
        self.assertEqual(instruction.type, InstructionType.MOD)
        self.assertEqual(instruction.source_register, None)
        self.assertEqual(instruction.source_value, 2)
        self.assertEqual(instruction.target_register, "z")

    def test_mod_zero(self):
        instruction = decode("mod z z")
        self.assertEqual(instruction.type, InstructionType.SET)
        self.assertEqual(instruction.source_register, None)
        self.assertEqual(instruction.source_value, 0)
        self.assertEqual(instruction.target_register, "z")

    def test_eql(self):
        instruction = decode("eql z w")
        self.assertEqual(instruction.type, InstructionType.EQUALS)
        self.assertEqual(instruction.source_register, "w")
        self.assertEqual(instruction.source_value, None)
        self.assertEqual(instruction.target_register, "z")

        instruction = decode("eql z 2")
        self.assertEqual(instruction.type, InstructionType.EQUALS)
        self.assertEqual(instruction.source_register, None)
        self.assertEqual(instruction.source_value, 2)
        self.assertEqual(instruction.target_register, "z")

    def test_eql_one(self):
        instruction = decode("eql y y")
        self.assertEqual(instruction.type, InstructionType.SET)
        self.assertEqual(instruction.source_register, None)
        self.assertEqual(instruction.source_value, 1)
        self.assertEqual(instruction.target_register, "y")


class Dependencies(TestCase):
    def test_trivial_example(self):
        code = [decode(line) for line in ["inp x", "mul x -1"]]
        registers = track_dependencies(code)
        self.assertListEqual(registers.reg_w.inputs, [])
        self.assertListEqual(registers.reg_x.inputs, [0])
        self.assertListEqual(registers.reg_y.inputs, [])
        self.assertListEqual(registers.reg_z.inputs, [])

    def test_two_registers(self):
        code = [decode(line) for line in ["inp z", "inp x", "mul z 3", "eql z x"]]
        registers = track_dependencies(code)
        self.assertListEqual(registers.reg_w.inputs, [])
        self.assertListEqual(registers.reg_x.inputs, [1])
        self.assertListEqual(registers.reg_y.inputs, [])
        self.assertListEqual(registers.reg_z.inputs, [0, 1])
        self.assertEqual(registers.reg_x.values.min, 1)
        self.assertEqual(registers.reg_x.values.max, 9)
        self.assertEqual(registers.reg_z.values.min, 0)
        self.assertEqual(registers.reg_z.values.max, 1)

    def test_simple_0_set(self):
        code = [decode(line) for line in ["mul x 0", "add x 3", "eql z x"]]
        registers = track_dependencies(code)
        self.assertListEqual(registers.reg_w.inputs, [])
        self.assertListEqual(registers.reg_x.inputs, [])
        self.assertListEqual(registers.reg_y.inputs, [])
        self.assertEqual(registers.reg_x.values.min, 3)
        self.assertEqual(registers.reg_x.values.max, 3)
        self.assertListEqual(registers.reg_z.inputs, [])

    def test_two_registers_with_zero(self):
        code = [decode(line) for line in ["inp z", "inp x", "mul z 3", "mul x 0", "add x 3", "eql z x"]]
        registers = track_dependencies(code)
        self.assertListEqual(registers.reg_w.inputs, [])
        self.assertListEqual(registers.reg_x.inputs, [])
        self.assertListEqual(registers.reg_y.inputs, [])
        self.assertEqual(registers.reg_x.values.min, 3)
        self.assertEqual(registers.reg_x.values.max, 3)
        self.assertEqual(registers.reg_z.values.min, 0)
        self.assertEqual(registers.reg_z.values.max, 1)
        self.assertListEqual(registers.reg_z.inputs, [0])

    def test_two_registers_single_value(self):
        code = [decode(line) for line in ["inp z", "inp x", "mul z 3", "mul x 0", "eql z x"]]
        registers = track_dependencies(code)
        self.assertListEqual(registers.reg_w.inputs, [])
        self.assertListEqual(registers.reg_x.inputs, [])
        self.assertListEqual(registers.reg_y.inputs, [])
        self.assertListEqual(registers.reg_z.inputs, [])

class AttemptReduction(TestCase):
    def test_star_two(self):
        code = [decode(line) for line in ["inp w", "inp x", "eql w 1", "eql x 2", "add z 1", "eql z x", "eql z 0"]]
        max_n = reduce_bounds(code, [9,9,9,9])
        self.assertListEqual(max_n, [9,2,9,9])

    def test_star_two_below(self):
        code = [decode(line) for line in ["inp w", "inp x", "eql w 1", "eql x 2", "add z 1", "eql z x", "eql z 0"]]
        max_n = reduce_bounds_from_below(code, [1,1,1,1])
        self.assertListEqual(max_n, [1,2,1,1])

    def test_backtrack_two(self):
        code = [decode(line) for line in ["inp w", "inp w", "inp x", "inp x", "inp x", "eql w x", "eql x 2", "add z w", "add z x", "eql z 2", "eql z 0"]]
        max_n = reduce_bounds(code, [9, 9,9,9,9,9, 9])
        self.assertListEqual(max_n, [9, 2, 9, 9, 2, 9, 9])

    def test_backtrack_two_below(self):
        code = [decode(line) for line in ["inp w", "inp w", "inp x", "inp x", "inp x", "eql w x", "eql x 2", "add z w", "add z x", "eql z 2", "eql z 0"]]
        max_n = reduce_bounds_from_below(code, [1, 1,1,1,1,1, 1])
        self.assertListEqual(max_n, [1, 2, 1, 1, 2, 1, 1])



class BoundedInstructions(TestCase):
    def test_add(self):
        target = BoundedValue(min=1, max=3)
        source = BoundedValue(min=2, max=5)
        apply_bounded_instruction(target, source, InstructionType.ADD)
        self.assertEqual(target.min, 3)
        self.assertEqual(target.max, 8)
        self.assertEqual(source.min, 2)
        self.assertEqual(source.max, 5)

    def test_div(self):
        target = BoundedValue(min=8, max=16)
        source = BoundedValue(min=2, max=4)
        apply_bounded_instruction(target, source, InstructionType.DIV)
        self.assertEqual(target.min, 2)
        self.assertEqual(target.max, 8)

    def test_div_round_to_zero(self):
        target = BoundedValue(min=9, max=17)
        source = BoundedValue(min=2, max=4)
        apply_bounded_instruction(target, source, InstructionType.DIV)
        self.assertEqual(target.min, 2)
        self.assertEqual(target.max, 8)

        target = BoundedValue(min=9, max=17)
        source = BoundedValue(min=-2, max=-4)
        apply_bounded_instruction(target, source, InstructionType.DIV)
        self.assertEqual(target.min, -8)
        self.assertEqual(target.max, -2)

        target = BoundedValue(min=-9, max=-17)
        source = BoundedValue(min=2, max=4)
        apply_bounded_instruction(target, source, InstructionType.DIV)
        self.assertEqual(target.min, -8)
        self.assertEqual(target.max, -2)

        target = BoundedValue(min=-17, max=9)
        source = BoundedValue(min=2, max=4)
        apply_bounded_instruction(target, source, InstructionType.DIV)
        self.assertEqual(target.min, -8)
        self.assertEqual(target.max, 4)

        target = BoundedValue(min=-17, max=9)
        source = BoundedValue(min=-2, max=4)
        apply_bounded_instruction(target, source, InstructionType.DIV)
        self.assertEqual(target.min, -4)
        self.assertEqual(target.max, 8)

    def test_eql_no_overlap(self):
        target = BoundedValue(min=8, max=16)
        source = BoundedValue(min=2, max=4)
        apply_bounded_instruction(target, source, InstructionType.EQUALS)
        self.assertEqual(target.min, 0)
        self.assertEqual(target.max, 0)

    def test_eql_overlap(self):
        target = BoundedValue(min=8, max=16)
        source = BoundedValue(min=2, max=8)
        apply_bounded_instruction(target, source, InstructionType.EQUALS)
        self.assertEqual(target.min, 0)
        self.assertEqual(target.max, 1)

    def test_eql_exact(self):
        target = BoundedValue(min=16, max=16)
        source = BoundedValue(min=16, max=16)
        apply_bounded_instruction(target, source, InstructionType.EQUALS)
        self.assertEqual(target.min, 1)
        self.assertEqual(target.max, 1)

    def test_mod_overlap(self):
        target = BoundedValue(min=0, max=100)
        source = BoundedValue(min=1, max=16)
        apply_bounded_instruction(target, source, InstructionType.MOD)
        self.assertEqual(target.min, 0)
        self.assertEqual(target.max, 15)

    def test_mod_reduced_range(self):
        target = BoundedValue(min=3, max=5)
        source = BoundedValue(min=8, max=16)
        apply_bounded_instruction(target, source, InstructionType.MOD)
        self.assertEqual(target.min, 3)
        self.assertEqual(target.max, 5)

    def test_mod_exact_source(self):
        target = BoundedValue(min=0, max=100)
        source = BoundedValue(min=8, max=8)
        apply_bounded_instruction(target, source, InstructionType.MOD)
        self.assertEqual(target.min, 0)
        self.assertEqual(target.max, 7)

    def test_mod_exact_target(self):
        target = BoundedValue(min=7, max=7)
        source = BoundedValue(min=1, max=8)
        apply_bounded_instruction(target, source, InstructionType.MOD)
        self.assertEqual(target.min, 0)
        self.assertEqual(target.max, 7)

    def test_mod_exact_both(self):
        target = BoundedValue(min=9, max=9)
        source = BoundedValue(min=8, max=8)
        apply_bounded_instruction(target, source, InstructionType.MOD)
        self.assertEqual(target.min, 1)
        self.assertEqual(target.max, 1)

    def test_mod_lhs_short(self):
        target = BoundedValue(min=0, max=8)
        source = BoundedValue(min=1, max=16)
        apply_bounded_instruction(target, source, InstructionType.MOD)
        self.assertEqual(target.min, 0)
        self.assertEqual(target.max, 8)

    def test_mul(self):
        target = BoundedValue(min=8, max=16)
        source = BoundedValue(min=2, max=4)
        apply_bounded_instruction(target, source, InstructionType.MUL)
        self.assertEqual(target.min, 16)
        self.assertEqual(target.max, 64)

        target = BoundedValue(min=9, max=17)
        source = BoundedValue(min=-2, max=-4)
        apply_bounded_instruction(target, source, InstructionType.MUL)
        self.assertEqual(target.min, -68)
        self.assertEqual(target.max, -18)

        target = BoundedValue(min=-9, max=-17)
        source = BoundedValue(min=2, max=4)
        apply_bounded_instruction(target, source, InstructionType.MUL)
        self.assertEqual(target.min, -68)
        self.assertEqual(target.max, -18)

        target = BoundedValue(min=-17, max=9)
        source = BoundedValue(min=2, max=4)
        apply_bounded_instruction(target, source, InstructionType.MUL)
        self.assertEqual(target.min, -68)
        self.assertEqual(target.max, 36)

        target = BoundedValue(min=-17, max=9)
        source = BoundedValue(min=-2, max=4)
        apply_bounded_instruction(target, source, InstructionType.MUL)
        self.assertEqual(target.min, -68)
        self.assertEqual(target.max, 36)
