from dataclasses import dataclass
from itertools import product


@dataclass
class Problem:
    inputs: list[int]
    raw_inputs: list[str]
    operation: str

def solve_part_one(problem: Problem) -> int:
    result = 0
    if problem.operation == "*":
        result = 1
        for x in problem.inputs:
            result *= x
    elif problem.operation == "+":
        result = sum(problem.inputs)
    else:
        raise ValueError(f"Unknown operation: {problem.operation}")
    print(f"Result: {result} from {problem.inputs} with operation {problem.operation}")
    return result

def solve_part_two(problem: Problem) -> int:
    converted_inputs: list[str] = ["" for _ in problem.inputs]
    reversed_inputs = [x[::-1] for x in problem.raw_inputs]
    for input in reversed_inputs:
        for digit_index, digit in enumerate(input):
            if digit != " ":
                converted_inputs[digit_index] += digit
    print(f"Converted Problem: {converted_inputs}  {problem.raw_inputs}")
    converted_problem = Problem(inputs=[int(x) for x in converted_inputs if x != ""],
                                raw_inputs=converted_inputs,
                                operation=problem.operation)
    return solve_part_one(converted_problem)

def load_sample(file: str) -> list[Problem]:
    problems: list[Problem] = []
    with open(file, "r", encoding="utf-8") as f:
        lines: list[str] = [line.strip("\n") for line in f.readlines()]
        num_starts = []
        for index, char in enumerate(lines[-1]):
            if char != "" and char != ' ':
                problems.append(Problem(inputs=[], operation=char, raw_inputs=[]))
                num_starts.append(index)
        for line in lines[:-1]:
            print(f"Starting {line}")
            problem_index = 0
            this_index = 0
            for next_index in num_starts[1:]:
                slice: str = line[this_index:next_index-1]
                print(f"slice {slice} from {this_index} to {next_index} using {line}")
                problems[problem_index].inputs.append(int(slice))
                problems[problem_index].raw_inputs.append(slice)
                problem_index += 1
                this_index = next_index
            slice = line[this_index:]
            problems[problem_index].inputs.append(int(slice))
            problems[problem_index].raw_inputs.append(slice)
    return problems



def part1(data: list[Problem]) -> int:
    return sum(solve_part_one(problem) for problem in data)


def part2(data: list[Problem]) -> int:
    return sum(solve_part_two(problem) for problem in data)


def main():
    try:
        data = load_sample("input/d06.txt")
        print(f"Part 1: {part1(data)}")
        print(f"Part 2: {part2(data)}")
    except FileNotFoundError:
        print("Input file not found.")


if __name__ == "__main__":
    main()
