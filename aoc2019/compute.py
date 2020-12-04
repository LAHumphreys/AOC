from enum import Enum

from tools.threading import MultiProdSingleConQueue, async_run


class ParamMode(Enum):
    POSITION = 0
    IMMEDIATE = 1


class UnknownMode(Exception):
    pass


class Instruction:
    def __init__(self, code: int):
        self.code = code
        self.opCode = None
        self.paramModes = None

    def get_op_code(self):
        if self.opCode is None:
            self.opCode = (self.code % 100)
        return self.opCode

    def get_value(self):
        return self.code

    def get_param_mode(self, param_idx):
        if self.paramModes is None:
            self.paramModes = [None, None, None]
            working_mask = int(self.code - self.get_op_code())
            working_mask = working_mask // 100
            for i in range(3):
                if working_mask < 1 or working_mask % 10 == 0:
                    self.paramModes[i] = ParamMode.POSITION
                elif working_mask % 10 == 1:
                    self.paramModes[i] = ParamMode.IMMEDIATE
                else:
                    raise UnknownMode
                working_mask = working_mask // 10

        return self.paramModes[param_idx]


def get_param(program: list, program_pointer: int, param_idx):
    val = None
    ins = program[program_pointer]
    mode = ins.get_param_mode(param_idx)
    if mode == ParamMode.IMMEDIATE:
        val = program[program_pointer + 1 + param_idx].get_value()
    elif mode == ParamMode.POSITION:
        idx = program[program_pointer + 1 + param_idx].get_value()
        val = program[idx].get_value()

    return val


def op_input(program, program_pointer, inp):
    out_index = program[program_pointer + 1].get_value()
    program[out_index] = Instruction(inp.pop(0))


def op_output(program, program_pointer, output):
    val = get_param(program, program_pointer, 0)
    output.append(val)


def op_add(program, program_pointer):
    out_index = program[program_pointer + 3].get_value()
    val = get_param(program, program_pointer, 0) + get_param(program, program_pointer, 1)
    program[out_index] = Instruction(val)


def op_less_than(program, program_pointer):
    out_index = program[program_pointer + 3].get_value()
    if get_param(program, program_pointer, 0) < get_param(program, program_pointer, 1):
        program[out_index] = Instruction(1)
    else:
        program[out_index] = Instruction(0)


def op_equal(program, program_pointer):
    out_index = program[program_pointer + 3].get_value()
    if get_param(program, program_pointer, 0) == get_param(program, program_pointer, 1):
        program[out_index] = Instruction(1)
    else:
        program[out_index] = Instruction(0)


def op_mul(program, program_pointer):
    out_index = program[program_pointer + 3].get_value()
    val = get_param(program, program_pointer, 0) * get_param(program, program_pointer, 1)
    program[out_index] = Instruction(val)


def op_jump_if_true(program, program_pointer):
    test_val = get_param(program, program_pointer, 0)
    next_exec = program_pointer + 3
    if test_val != 0:
        next_exec = get_param(program, program_pointer, 1)

    return next_exec


def op_jump_if_false(program, program_pointer):
    test_val = get_param(program, program_pointer, 0)
    next_exec = program_pointer + 3
    if test_val == 0:
        next_exec = get_param(program, program_pointer, 1)

    return next_exec


def encode(program):
    encoded_program = []
    for ins in program:
        encoded_program.append(Instruction(ins))

    return encoded_program


def decode(program):
    decoded_program = []
    for ins in program:
        decoded_program.append(ins.get_value())

    return decoded_program


class UnknownOp(Exception):
    pass


def encode_compute(program, inp=None, output=None):
    if output is None:
        output = []
    if inp is None:
        inp = []
    exec_i = 0
    op = program[exec_i].get_op_code()
    while op != 99:
        if op == 1:
            op_add(program, exec_i)
            exec_i += 4
        elif op == 2:
            op_mul(program, exec_i)
            exec_i += 4
        elif op == 3:
            op_input(program, exec_i, inp)
            exec_i += 2
        elif op == 4:
            op_output(program, exec_i, output)
            exec_i += 2
        elif op == 5:
            exec_i = op_jump_if_true(program, exec_i)
        elif op == 6:
            exec_i = op_jump_if_false(program, exec_i)
        elif op == 7:
            op_less_than(program, exec_i)
            exec_i += 4
        elif op == 8:
            op_equal(program, exec_i)
            exec_i += 4
        else:
            raise UnknownOp

        op = program[exec_i].get_op_code()

    return program


def compute(code, inp=None, output=None):
    if inp is None:
        inp = []
    if output is None:
        output = []
    program = encode_compute(encode(code), inp=inp, output=output)
    return decode(program)


def compute_pipeline(programs, inp, output, initial_inputs=None):
    lhs = inp
    rhs = MultiProdSingleConQueue()
    i = 0
    inputs = []
    outputs = []
    while i < len(programs):
        if initial_inputs is not None:
            for inp in initial_inputs[i]:
                lhs.push(inp)
        inputs.append(lhs)
        outputs.append(rhs)
        i += 1
        lhs = rhs
        if i == (len(programs) - 1):
            rhs = output
        else:
            rhs = MultiProdSingleConQueue()

    i = 0
    computers = []
    while i < len(programs):
        computers.append(
            async_run(
                lambda: compute(
                    programs[i],
                    inputs[i],
                    outputs[i])))
        i += 1

    for c in computers:
        c.join()
