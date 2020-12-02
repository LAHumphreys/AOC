from enum import Enum
from tools.threading import MultiProdSingleConQueue, AsyncRun

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

    def GetOpCode(self):
        if self.opCode is None:
            self.opCode = (self.code % 100)
        return self.opCode

    def GetValue(self):
        return self.code

    def GetParamMode(self, paramIdx):
        if self.paramModes is None:
            self.paramModes = [None, None, None]
            workingMask = int(self.code  - self.GetOpCode())
            workingMask = workingMask //  100
            for i in range(3):
                if workingMask < 1 or workingMask%10 == 0:
                    self.paramModes[i] = ParamMode.POSITION
                elif workingMask%10 == 1:
                    self.paramModes[i] = ParamMode.IMMEDIATE
                else:
                    raise UnknownMode
                workingMask = workingMask // 10

        return self.paramModes[paramIdx]

def GetParam(prog: list, progPtr: int, paramIdx):
    val = None
    ins = prog[progPtr]
    mode = ins.GetParamMode(paramIdx)
    if mode == ParamMode.IMMEDIATE:
        val = prog[progPtr + 1 + paramIdx].GetValue()
    elif mode == ParamMode.POSITION:
        idx = prog[progPtr + 1 + paramIdx].GetValue()
        val = prog[idx].GetValue()

    return val

def Input(prog, progPtr, input):
    outIndx = prog[progPtr+1].GetValue()
    prog[outIndx] = Instruction(input.pop(0))

def Output(prog, progPtr, output):
    val = GetParam(prog, progPtr, 0)
    output.append(val)

def Add(prog, progPtr):
    outIndx = prog[progPtr+3].GetValue()
    val = GetParam(prog, progPtr, 0) + GetParam(prog, progPtr, 1)
    prog[outIndx] = Instruction(val)

def LT(prog, progPtr):
    outIndx = prog[progPtr+3].GetValue()
    if GetParam(prog, progPtr, 0) < GetParam(prog, progPtr, 1):
        prog[outIndx] = Instruction(1)
    else:
        prog[outIndx] = Instruction(0)

def EQ(prog, progPtr):
    outIndx = prog[progPtr+3].GetValue()
    if GetParam(prog, progPtr, 0) == GetParam(prog, progPtr, 1):
        prog[outIndx] = Instruction(1)
    else:
        prog[outIndx] = Instruction(0)

def Mul(prog, progPtr):
    outIndx = prog[progPtr+3].GetValue()
    val = GetParam(prog, progPtr, 0) * GetParam(prog, progPtr, 1)
    prog[outIndx] = Instruction(val)

def JumpIfTrue(prog, progPtr):
    testVal = GetParam(prog, progPtr, 0)
    nextExec = progPtr + 3
    if testVal != 0:
        nextExec = GetParam(prog, progPtr, 1)

    return nextExec

def JumpIfFalse(prog, progPtr):
    testVal = GetParam(prog, progPtr, 0)
    nextExec = progPtr + 3
    if testVal == 0:
        nextExec = GetParam(prog, progPtr, 1)

    return nextExec


def Encode(prog):
    encodedProg = []
    for ins in prog:
        encodedProg.append(Instruction(ins))

    return encodedProg

def Decode(prog):
    decodedProg = []
    for ins in prog:
        decodedProg.append(ins.GetValue())

    return decodedProg

class UnknownOp(Exception):
    pass

def EncodedCompute(prog, input=[], output=[]):
    exec = 0
    op = prog[exec].GetOpCode()
    while (op != 99):
        if op == 1:
            Add(prog, exec)
            exec += 4
        elif op == 2:
            Mul(prog, exec)
            exec += 4
        elif op == 3:
            Input(prog, exec, input)
            exec += 2
        elif op == 4:
            Output(prog, exec, output)
            exec += 2
        elif op == 5:
            exec =  JumpIfTrue(prog, exec)
        elif op == 6:
            exec = JumpIfFalse(prog, exec)
        elif op == 7:
            LT(prog, exec)
            exec += 4
        elif op == 8:
            EQ(prog, exec)
            exec += 4
        else:
            raise UnknownOp

        op = prog[exec].GetOpCode()

    return prog

def Compute(code, input=[], output=[]):
    prog = EncodedCompute(Encode(code), input=input, output=output)
    return Decode(prog)


def ComputePipeline(programs, input, output, initialInputs = None):
    # TODO: Check sane input
    lhs = input
    rhs = MultiProdSingleConQueue()
    i = 0
    inputs = []
    outputs = []
    while i < len(programs):
        if initialInputs is not None:
            for input in initialInputs[i]:
                lhs.Push(input)
        inputs.append(lhs)
        outputs.append(rhs)
        i += 1
        lhs = rhs
        if i == (len(programs) -1):
            rhs = output
        else:
            rhs = MultiProdSingleConQueue()

    i = 0
    computers = []
    while i < len(programs):
        computers.append(AsyncRun(lambda: Compute(programs[i], inputs[i], outputs[i])))
        i += 1

    for c in computers:
        c.join()
