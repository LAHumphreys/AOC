from collections import namedtuple
from typing import List

PowerVars = namedtuple("PowerVars", ["gamma", "epsilon"])
LifeVars = namedtuple("LifeVars", ["o2", "co2"])


def decode_binary_str(number: str):
    num = 0
    num_digits = len(number)
    for i in range(num_digits):
        if number[i] == "1":
            num += 2**(num_digits-i-1)
    return num


def calc_power_vars(lines: List[str]) -> PowerVars:
    count = [0] * len(lines[0])
    for line in lines:
        for i, bit in enumerate(line):
            if bit == "1":
                count[i] += 1
    num_inputs: int = len(lines)
    num_digits: int = len(count)
    threshold: int = num_inputs / 2
    gamma: int = 0
    epsilon: int = 0
    for i in range (num_digits):
        if count[i] > threshold:
            gamma += 2**(num_digits-i-1)
        else:
            epsilon += 2**(num_digits-i-1)

    return PowerVars(gamma=gamma, epsilon=epsilon)


def filter_o2(lines: List[str], pos: int,  mode_value: str = "1"):
    return [line for line in lines if line[pos] == mode_value]


def filter_co2(lines: List[str], pos: int,  mode_value: str = "1"):
    return [ln for ln in lines if ln[pos] != mode_value]


def filter_by_mode(lines: List[str], pos: int, filt):
    num_inputs: int = len(lines)
    threshold: int = num_inputs / 2
    pos_sum: int = 0
    for line in lines:
        if line[pos] == "1":
            pos_sum += 1

    if pos_sum >= threshold:
        result = filt(lines, pos, "1")
    elif pos_sum < threshold:
        result = filt(lines, pos, "0")
    else:
        result = filt(lines, pos)

    return result


def recursive_mode_filter(lines: List[str], filter_func):
    pos = 0
    while len(lines) > 1:
        lines = filter_by_mode(lines, pos, filter_func)
        pos += 1
    return lines[0]


def calc_life_vars(lines) -> LifeVars:
    o2ln = recursive_mode_filter(lines, filter_o2)
    co2ln = recursive_mode_filter(lines, filter_co2)

    o2_score = decode_binary_str(o2ln)
    co2_score = decode_binary_str(co2ln)

    return LifeVars(o2=o2_score, co2=co2_score)


if __name__ == "__main__":
    def main():
        with open("input/d03.txt", encoding="ascii") as file:
            lines = [l[:-1] for l in file.readlines()]
        power_vars = calc_power_vars(lines)
        life_vars = calc_life_vars(lines)
        print (power_vars)
        print (power_vars.gamma * power_vars.epsilon)
        print (life_vars)
        print (life_vars.co2 * life_vars.o2)
    main()
