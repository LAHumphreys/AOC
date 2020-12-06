import copy

from aoc2019.compute import encode, encode_compute, compute_pipeline
from tools.combinations import generate_permutations
from tools.file_loader import load_int_list
from tools.threading import MultiProdSingleConQueue


class Amplifier:
    def __init__(self, code):
        self.program = encode(code)

    def get_code(self):
        return copy.copy(self.program)

    def amplify(self, phase, input_signal):
        program = self.get_code()
        inp = [phase, input_signal]
        output = []
        encode_compute(program, inp=inp, output=output)

        return output[0]


class PhaseAmpMismatch(Exception):
    pass


class Thruster:
    def __init__(self, code):
        self.amp = Amplifier(code)
        self.number_amps = 5

    def get_amp(self):
        return self.amp

    def compute_thrust(self, phases):
        if len(phases) != self.number_amps:
            raise PhaseAmpMismatch
        thrust = 0
        i = 0
        while i < self.number_amps:
            thrust = self.get_amp().amplify(phases[i], thrust)
            i += 1

        return thrust


class FeedbackThruster:
    def __init__(self, code):
        self.code = code
        self.number_amps = 5

    def get_code(self):
        return copy.copy(self.code)

    def compute_thrust(self, phases):
        if len(phases) != self.number_amps:
            raise PhaseAmpMismatch

        initial_inputs = []
        pipeline = []
        for phase in phases:
            pipeline.append(self.get_code())
            initial_inputs.append([phase])
        initial_inputs[0].append(0)
        inp = MultiProdSingleConQueue()
        output = inp
        compute_pipeline(pipeline, inp, output, initial_inputs=initial_inputs)
        return output.pop()


def find_max_thrust(code):
    thruster = Thruster(code)
    max_thrust = -1
    for phase in generate_permutations([0, 1, 2, 3, 4], 5):
        thrust = thruster.compute_thrust(phase)
        if thrust > max_thrust:
            max_thrust = thrust

    return max_thrust


def find_max_feedback_thrust(code):
    thruster = FeedbackThruster(code)
    max_thrust = -1
    for phase in generate_permutations([5, 6, 7, 8, 9], 5):
        thrust = thruster.compute_thrust(phase)
        if thrust > max_thrust:
            max_thrust = thrust

    return max_thrust


if __name__ == "__main__":
    def main():
        code = load_int_list("input/d07.txt")
        print("Max thrust: {0}".format(find_max_thrust(code)))

        print("Max Feedback thrust: {0}".format(find_max_feedback_thrust(code)))

    main()
