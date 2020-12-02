from aoc2019.compute import Encode, EncodedCompute, ComputePipeline
from tools.combinations import GeneratePermutations
from tools.fileLoader import LoadIntList
from tools.threading import MultiProdSingleConQueue
import copy


class Amplifier:
    def __init__(self, code):
        self.prog = Encode(code)

    def amplify(self, phase, inputSignal):
        prog = copy.copy(self.prog)
        input = [phase, inputSignal]
        output = []
        EncodedCompute(prog, input=input, output=output)

        return output[0]

class PhaseAmpMismatch(Exception):
    pass

class Thruster:
    def __init__(self, code):
        self.amp = Amplifier(code)
        self.numAmps = 5

    def ComputeThrust(self, phases):
        if len(phases) != self.numAmps:
            raise PhaseAmpMismatch
        thrust = 0
        i = 0
        while i < self.numAmps:
            thrust = self.amp.amplify(phases[i], thrust)
            i += 1

        return thrust

class FeedbackThruster:
    def __init__(self, code):
        self.code = code
        self.numAmps = 5

    def ComputeThrust(self, phases):
        if len(phases) != self.numAmps:
            raise PhaseAmpMismatch

        initialInputs = []
        pipeline = []
        for phase in phases:
            pipeline.append(copy.copy(self.code))
            initialInputs.append([phase])
        initialInputs[0].append(0)
        input = MultiProdSingleConQueue()
        output = input
        ComputePipeline(pipeline, input, output, initialInputs=initialInputs)
        return output.Pop()

def FindMaxThrust(code):
    thruster = Thruster(code)
    maxThrust = -1
    for phase in GeneratePermutations([0,1,2,3,4], 5):
        thrust = thruster.ComputeThrust(phase)
        if thrust > maxThrust:
            maxThrust = thrust

    return maxThrust

def FindMaxFeedbackThrust(code):
    thruster = FeedbackThruster(code)
    maxThrust = -1
    for phase in GeneratePermutations([5,6,7,8,9], 5):
        thrust = thruster.ComputeThrust(phase)
        if thrust > maxThrust:
            maxThrust = thrust

    return maxThrust

if __name__ == "__main__":
    code = LoadIntList("input/d07.txt")
    print ("Max thrust: {0}".format(FindMaxThrust(code)))

    print ("Max Feedback thrust: {0}".format(FindMaxFeedbackThrust(code)))
