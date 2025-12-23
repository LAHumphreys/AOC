from dataclasses import dataclass
from itertools import product


@dataclass
class Problem:
    inputs: list[int]
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

def load_sample(file: str) -> list[Problem]:
    problems: list[Problem] = []
    with open(file, "r", encoding="utf-8") as f:
        lines = [line.strip().split(" ") for line in f.readlines()]
        for char in lines[-1]:
            if char != "":
                problems.append(Problem(inputs=[], operation=char))
        for line in lines[:-1]:
            problem_index = 0
            for input_num in line:
                if input_num != "":
                    problems[problem_index].inputs.append(int(input_num))
                    problem_index += 1
    return problems



def part1(data: list[Problem]) -> int:
    return sum(solve_part_one(problem) for problem in data)


def part2(data: list[Problem]) -> int:
    return len(data)


def main():
    try:
        data = load_sample("input/d06.txt")
        print(f"Part 1: {part1(data)}")
        print(f"Part 2: {part2(data)}")
    except FileNotFoundError:
        print("Input file not found.")


if __name__ == "__main__":
    main()
