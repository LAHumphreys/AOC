from typing import List

pairs = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}


def find_err_index(code: str) -> int:
    stack = []
    index = -1
    for i, token in enumerate(code):
        if token in pairs:
            stack.append(pairs[token])
        else:
            next_close = stack.pop()
            if next_close != token:
                index = i
                break
    return index


class InvalidCode(Exception):
    pass


def complete_line(code: str) -> List[str]:
    stack = []
    for token in code:
        if token in pairs:
            stack.append(pairs[token])
        else:
            next_close = stack.pop()
            if next_close != token:
                raise InvalidCode
    stack.reverse()
    return stack


def load_code(path: str) -> List[str]:
    with open(path, encoding="ascii") as file:
        lines = [line.replace("\n", "") for line in file.readlines()]
    return lines


scoring = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}


def part_one(program: List[str]) -> int:
    score = 0
    for line in program:
        index = find_err_index(line)
        if index > -1:
            score += scoring[line[index]]
    return score


completion_scoring = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}


def score_part_2(correction: str):
    score = 0
    for token in correction:
        score *= 5
        score += completion_scoring[token]
    return score


def part_two(program: List[str]) -> int:
    scores = []
    for line in program:
        if find_err_index(line) < 0:
            scores.append(score_part_2("".join(complete_line(line))))
    scores.sort()
    return scores[len(scores)//2]


if __name__ == "__main__":
    def main():
        data = load_code("input/d10.txt")
        print(part_one(data))
        print(part_two(data))
    main()
