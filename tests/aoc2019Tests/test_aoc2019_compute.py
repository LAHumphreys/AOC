import copy
from unittest import TestCase

from aoc2019.compute import compute, op_add, op_mul, Instruction, ParamMode, get_param, encode, decode, op_input, \
    op_output
from aoc2019.compute import op_jump_if_true, op_jump_if_false, op_less_than, op_equal, encode_compute, compute_pipeline
from tools.threading import MultiProdSingleConQueue, async_run


class TestInstruction(TestCase):
    def test_OpCode(self):
        self.assertEqual(Instruction(2).get_op_code(), 2)
        self.assertEqual(Instruction(6).get_op_code(), 6)
        self.assertEqual(Instruction(1002).get_op_code(), 2)
        self.assertEqual(Instruction(1102).get_op_code(), 2)
        self.assertEqual(Instruction(1106).get_op_code(), 6)
        self.assertEqual(Instruction(11101).get_op_code(), 1)
        self.assertEqual(Instruction(11000).get_op_code(), 0)
        self.assertEqual(Instruction(11099).get_op_code(), 99)

    def test_Value(self):
        self.assertEqual(Instruction(2).get_value(), 2)
        self.assertEqual(Instruction(6).get_value(), 6)
        self.assertEqual(Instruction(1002).get_value(), 1002)
        self.assertEqual(Instruction(1102).get_value(), 1102)
        self.assertEqual(Instruction(11101).get_value(), 11101)
        self.assertEqual(Instruction(11000).get_value(), 11000)
        self.assertEqual(Instruction(11099).get_value(), 11099)

    def test_ParamMode_DefaultPosition(self):
        self.assertEqual(Instruction(6).get_param_mode(0), ParamMode.POSITION)
        self.assertEqual(Instruction(2).get_param_mode(0), ParamMode.POSITION)
        self.assertEqual(Instruction(1).get_param_mode(0), ParamMode.POSITION)
        self.assertEqual(Instruction(99).get_param_mode(0), ParamMode.POSITION)

        self.assertEqual(Instruction(2).get_param_mode(1), ParamMode.POSITION)
        self.assertEqual(Instruction(1).get_param_mode(2), ParamMode.POSITION)
        self.assertEqual(Instruction(99).get_param_mode(2), ParamMode.POSITION)
        self.assertEqual(Instruction(6).get_param_mode(2), ParamMode.POSITION)

    def test_ParamMode_ImmediateMode_FirstOnly(self):
        self.assertEqual(Instruction(102).get_param_mode(0), ParamMode.IMMEDIATE)
        self.assertEqual(Instruction(102).get_param_mode(1), ParamMode.POSITION)
        self.assertEqual(Instruction(102).get_param_mode(2), ParamMode.POSITION)

    def test_ParamMode_ImmediateMode_LastOnly(self):
        self.assertEqual(
            Instruction(10002).get_param_mode(0),
            ParamMode.POSITION)
        self.assertEqual(
            Instruction(10002).get_param_mode(1),
            ParamMode.POSITION)
        self.assertEqual(
            Instruction(10002).get_param_mode(2),
            ParamMode.IMMEDIATE)

    def test_ParamMode_ImmediateMode_AllImmediate(self):
        self.assertEqual(
            Instruction(11102).get_param_mode(0),
            ParamMode.IMMEDIATE)
        self.assertEqual(
            Instruction(11102).get_param_mode(1),
            ParamMode.IMMEDIATE)
        self.assertEqual(
            Instruction(11102).get_param_mode(2),
            ParamMode.IMMEDIATE)


class TestGetParam(TestCase):
    def test_DefaultPosition(self):
        inp = encode([1, 0, 1, 2, 99])
        self.assertEqual(get_param(inp, 0, 0), 1)
        self.assertEqual(get_param(inp, 0, 1), 0)
        self.assertEqual(get_param(inp, 0, 2), 1)

    def test_AllImmediate(self):
        inp = encode([2, 2, 2, 2, 11101, 0, 1, 2, 99])
        self.assertEqual(get_param(inp, 4, 0), 0)
        self.assertEqual(get_param(inp, 4, 1), 1)
        self.assertEqual(get_param(inp, 3, 2), 2)


class TestCompute(TestCase):
    def test_Compute_Example1(self):
        self.assertListEqual(compute([1, 0, 0, 0, 99]), [2, 0, 0, 0, 99])

    def test_Compute_Example2(self):
        self.assertListEqual(compute([2, 3, 0, 3, 99]), [2, 3, 0, 6, 99])

    def test_Compute_Example3(self):
        self.assertListEqual(compute([2, 4, 4, 5, 99, 0]), [
            2, 4, 4, 5, 99, 9801])

    def test_Compute_Example4(self):
        self.assertListEqual(compute([1, 1, 1, 4, 99, 5, 6, 0, 99]), [
            30, 1, 1, 4, 2, 5, 6, 0, 99])

    def test_Compute_EarlyStop(self):
        self.assertListEqual(compute([1, 1, 1, 5, 99, 5, 6, 0, 99]), [
            1, 1, 1, 5, 99, 2, 6, 0, 99])

    def test_Compute_InputOutput(self):
        prog = [3, 0, 4, 0, 99]
        inp = [55]
        output = []
        expected = [55, 0, 4, 0, 99]
        self.assertListEqual(compute(prog, inp=inp, output=output), expected)
        self.assertListEqual(inp, [])
        self.assertListEqual(output, [55])

    def test_Compute_MultipleInput(self):
        prog = [3, 0, 3, 1, 2, 0, 1, 2, 4, 2, 99]
        inp = [55, 5]
        output = []
        expected = [55, 5, 5 * 55, 1, 2, 0, 1, 2, 4, 2, 99]
        self.assertListEqual(compute(prog, inp=inp, output=output), expected)
        self.assertListEqual(inp, [])
        self.assertListEqual(output, [55 * 5])

    def test_Compute_MultipleOutput(self):
        prog = [4, 0, 4, 1, 4, 2, 99]
        inp = []
        output = []
        expected = prog
        self.assertListEqual(compute(prog, inp=inp, output=output), expected)
        self.assertListEqual(inp, [])
        self.assertListEqual(output, [4, 0, 4])

    def test_Compute_NegativeVals(self):
        prog = [1101, 100, -1, 4, 0]
        expected = [1101, 100, -1, 4, 100 - 1]
        self.assertListEqual(compute(prog), expected)


class TestAdd(TestCase):
    def test_Compute_Example1(self):
        inp = encode([1, 0, 0, 0, 99])
        op_add(inp, 0)
        self.assertListEqual(decode(inp), [2, 0, 0, 0, 99])

    def test_Compute_ImmediateExample(self):
        inp = encode([1001, 4, 45, 4, 45])
        op_add(inp, 0)
        self.assertListEqual(decode(inp), [1001, 4, 45, 4, 90])


class TestLT(TestCase):
    def test_LT_True(self):
        inp = encode([1107, 1, 2, 3, 99])
        op_less_than(inp, 0)
        self.assertListEqual(decode(inp), [1107, 1, 2, 1, 99])

    def test_LT_False(self):
        inp = encode([1107, 2, 1, 3, 99])
        op_less_than(inp, 0)
        self.assertListEqual(decode(inp), [1107, 2, 1, 0, 99])


class TestEQ(TestCase):
    def test_EQ_True(self):
        inp = encode([1108, 2, 2, 3, 99])
        op_equal(inp, 0)
        self.assertListEqual(decode(inp), [1108, 2, 2, 1, 99])

    def test_EQ_False(self):
        inp = encode([1108, 2, 1, 3, 99])
        op_equal(inp, 0)
        self.assertListEqual(decode(inp), [1108, 2, 1, 0, 99])


class TestJumpIf(TestCase):
    def test_Compute_IfTrue_True(self):
        code = encode([5, 1, 3, 4, 99])
        nextExec = op_jump_if_true(code, 0)
        self.assertListEqual(decode(code), [5, 1, 3, 4, 99])
        self.assertEqual(nextExec, 4)

    def test_Compute_IfFalse_True(self):
        code = encode([6, 1, 3, 4, 99])
        nextExec = op_jump_if_false(code, 0)
        self.assertListEqual(decode(code), [6, 1, 3, 4, 99])
        self.assertEqual(nextExec, 3)

    def test_Compute_IfTrue_NonBool(self):
        code = encode([105, 3, 3, 4, 99])
        nextExec = op_jump_if_true(code, 0)
        self.assertListEqual(decode(code), [105, 3, 3, 4, 99])
        self.assertEqual(nextExec, 4)

    def test_Compute_IfFalse_NonBool(self):
        code = encode([106, 3, 3, 4, 99])
        nextExec = op_jump_if_false(code, 0)
        self.assertListEqual(decode(code), [106, 3, 3, 4, 99])
        self.assertEqual(nextExec, 3)

    def test_Compute_IfTrue_False(self):
        code = encode([105, 0, 99, 4, 99])
        nextExec = op_jump_if_true(code, 0)
        self.assertListEqual(decode(code), [105, 0, 99, 4, 99])
        self.assertEqual(nextExec, 3)

    def test_Compute_IfFalse_False(self):
        code = encode([106, 0, 3, 4, 99])
        nextExec = op_jump_if_false(code, 0)
        self.assertListEqual(decode(code), [106, 0, 3, 4, 99])
        self.assertEqual(nextExec, 4)


class TestInput(TestCase):
    def test_Compute_Example1(self):
        prog = encode([3, 4, 0, 0, 0])
        inp = [99]
        op_input(prog, 0, inp)
        self.assertListEqual(decode(prog), [3, 4, 0, 0, 99])
        self.assertListEqual(inp, [])


class TestOutput(TestCase):
    def test_Compute_Example1(self):
        prog = encode([4, 2, 99, 0, 0])
        output = []
        op_output(prog, 0, output)
        self.assertListEqual(decode(prog), [4, 2, 99, 0, 0])
        self.assertListEqual(output, [99])

    def test_Compute_ImmediateVal(self):
        prog = encode([104, 2, 99, 0, 0])
        output = []
        op_output(prog, 0, output)
        self.assertListEqual(decode(prog), [104, 2, 99, 0, 0])
        self.assertListEqual(output, [2])


class TestMul(TestCase):
    def test_Compute_Example1(self):
        inp = encode([2, 3, 0, 3, 99])
        op_mul(inp, 0)
        self.assertListEqual(decode(inp), [2, 3, 0, 6, 99])

    def test_Compute_ImmediateExample(self):
        inp = encode([1002, 4, 3, 4, 33])
        op_mul(inp, 0)
        self.assertListEqual(decode(inp), [1002, 4, 3, 4, 99])


class TestComputeBranching(TestCase):
    def test_EqPosBranch_InputMatches(self):
        inp = [8]
        output = []
        code = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
        compute(code, inp=inp, output=output)
        self.assertEqual(output, [1])

    def test_EqPosBranch_InputMisMatches(self):
        inp = [7]
        output = []
        code = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
        compute(code, inp=inp, output=output)
        self.assertEqual(output, [0])

    def test_EqImmBranch_InputMatches(self):
        inp = [8]
        output = []
        code = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
        compute(code, inp=inp, output=output)
        self.assertEqual(output, [1])

    def test_EqImmBranch_InputMisMatches(self):
        inp = [7]
        output = []
        code = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
        compute(code, inp=inp, output=output)
        self.assertEqual(output, [0])

    def test_LtPosBranch_InputLT(self):
        inp = [7]
        output = []
        code = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
        compute(code, inp=inp, output=output)
        self.assertEqual(output, [1])

    def test_LtPosBranch_InputMatches(self):
        inp = [8]
        output = []
        code = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
        compute(code, inp=inp, output=output)
        self.assertEqual(output, [0])

    def test_LtPosBranch_InputGT(self):
        inp = [9]
        output = []
        code = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
        compute(code, inp=inp, output=output)
        self.assertEqual(output, [0])

    def test_LtImmBranch_InputLT(self):
        inp = [7]
        output = []
        code = [3, 3, 1107, -1, 8, 3, 4, 3, 99]
        compute(code, inp=inp, output=output)
        self.assertEqual(output, [1])

    def test_LtImmBranch_InputGT(self):
        inp = [9]
        output = []
        code = [3, 3, 1107, -1, 8, 3, 4, 3, 99]
        compute(code, inp=inp, output=output)
        self.assertEqual(output, [0])

    def test_JumpIfZero_zero(self):
        inp = [0]
        output = []
        code = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
        compute(code, inp=inp, output=output)
        self.assertEqual(output, [0])

    def test_JumpIfZero_nonzero(self):
        inp = [3]
        output = []
        code = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
        compute(code, inp=inp, output=output)
        self.assertEqual(output, [1])

    def test_JumpIfZero_imm_zero(self):
        inp = [0]
        output = []
        code = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]
        compute(code, inp=inp, output=output)
        self.assertEqual(output, [0])

    def test_JumpIfZero_imm_nonzero(self):
        inp = [6]
        output = []
        code = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]
        compute(code, inp=inp, output=output)
        self.assertEqual(output, [1])

    def test_ComplexBranching(self):
        code = encode([
            3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
            1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
            999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99
        ])
        for i in range(10):
            inp = [i]
            output = []
            encode_compute(code, inp=inp, output=output)
            if i < 8:
                self.assertEqual(output, [999])
            elif i == 8:
                self.assertEqual(output, [1000])
            else:
                self.assertEqual(output, [1001])


class Test_Pipeline(TestCase):
    trippleProg = [3, 9, 1002, 9, -3, 10, 4, 10, 99, 0, 0]
    minusThreeProg = [3, 9, 1001, 9, -3, 10, 4, 10, 99, 0, 0]
    mulTwoInputs = [3, 11, 3, 12, 2, 11, 12, 13, 4, 13, 99, 0, 0, 0]

    def test_Compute_TrippleInput(self):
        prog = self.trippleProg
        expected = [3, 9, 1002, 9, -3, 10, 4, 10, 99, 55, -165]
        inp = [55]
        output = []
        self.assertListEqual(compute(prog, inp=inp, output=output), expected)
        self.assertListEqual(inp, [])
        self.assertListEqual(output, [-165])

        inp = [10]
        output = []
        prog = expected
        expected = [3, 9, 1002, 9, -3, 10, 4, 10, 99, 10, -30]
        self.assertListEqual(compute(prog, inp=inp, output=output), expected)
        self.assertListEqual(inp, [])
        self.assertListEqual(output, [-30])

    def test_Compute_Minus3(self):
        prog = self.minusThreeProg
        expected = [3, 9, 1001, 9, -3, 10, 4, 10, 99, 55, 52]
        inp = [55]
        output = []
        self.assertListEqual(compute(prog, inp=inp, output=output), expected)
        self.assertListEqual(inp, [])
        self.assertListEqual(output, [52])

    def test_Compute_Multiply2(self):
        prog = self.mulTwoInputs
        expected = [3, 11, 3, 12, 2, 11, 12, 13, 4, 13, 99, 55, 5, 55 * 5]
        inp = [55, 5]
        output = []
        self.assertListEqual(compute(prog, inp=inp, output=output), expected)
        self.assertListEqual(inp, [])
        self.assertListEqual(output, [55 * 5])

    def test_Compute_AsyncIO(self):
        inp = MultiProdSingleConQueue()
        output = MultiProdSingleConQueue()
        computer = async_run(
            lambda: compute(
                self.trippleProg,
                inp=inp,
                output=output))
        inp.push(3)
        self.assertEqual(output.pop(), -9)
        computer.join()

    def test_Compute_Pipeline(self):
        pipeline = [self.trippleProg, self.minusThreeProg]
        inp = MultiProdSingleConQueue()
        output = MultiProdSingleConQueue()
        inp.push(5)
        compute_pipeline(pipeline, inp, output)
        self.assertEqual(output.pop(), (5 * -3) - 3)

    def test_Compute_Pipeline_3(self):
        pipeline = [self.trippleProg, self.minusThreeProg, self.trippleProg]
        inp = MultiProdSingleConQueue()
        output = MultiProdSingleConQueue()
        inp.push(5)
        compute_pipeline(pipeline, inp, output)
        self.assertEqual(output.pop(), ((5 * -3) - 3) * -3)

    def test_Compute_Pipeline_Input(self):
        pipeline = [
            self.trippleProg,
            self.minusThreeProg,
            self.trippleProg,
            self.mulTwoInputs]
        initialInputs = [[5], [], [], [2]]
        inp = MultiProdSingleConQueue()
        output = MultiProdSingleConQueue()
        compute_pipeline(pipeline, inp, output, initial_inputs=initialInputs)
        self.assertEqual(output.pop(), 2 * (((5 * -3) - 3) * -3))

    def test_Compute_Example1(self):
        code = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27,
                26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5]
        phases = [9, 8, 7, 6, 5]
        initialInputs = []
        pipeline = []
        for phase in phases:
            pipeline.append(copy.copy(code))
            initialInputs.append([phase])
        initialInputs[0].append(0)
        inp = MultiProdSingleConQueue()
        output = inp
        compute_pipeline(pipeline, inp, output, initial_inputs=initialInputs)
        self.assertEqual(output.pop(), 139629729)

    def test_Compute_Example2(self):
        code = [
            3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55,
            1005, 55, 26, 1001, 54, -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008,
            54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001, 56, -1, 56,
            1005, 56, 6, 99, 0, 0, 0, 0, 10]
        phases = [9, 7, 8, 5, 6]
        initialInputs = []
        pipeline = []
        for phase in phases:
            pipeline.append(copy.copy(code))
            initialInputs.append([phase])
        initialInputs[0].append(0)
        inp = MultiProdSingleConQueue()
        output = inp
        compute_pipeline(pipeline, inp, output, initial_inputs=initialInputs)
        self.assertEqual(output.pop(), 18216)
