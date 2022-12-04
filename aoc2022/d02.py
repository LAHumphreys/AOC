from tools.file_loader import load_int_groups
from dataclasses import dataclass
from enum import Enum


class RPS(Enum):
    ROCK: int = 1
    PAPER: int = 2
    SCISSORS: int = 3


class Result(Enum):
    WIN: int = 6
    DRAW: int = 3
    LOSE: int = 0


@dataclass
class Round:
    you: RPS
    opponent: RPS


@dataclass
class Round2:
    opponent: RPS
    result: Result


code_to_rps = {
    'A': RPS.ROCK,
    'B': RPS.PAPER,
    'C': RPS.SCISSORS,
    'X': RPS.ROCK,
    'Y': RPS.PAPER,
    'Z': RPS.SCISSORS
}

code_to_win = {
    'X': Result.LOSE,
    'Y': Result.DRAW,
    'Z': Result.WIN
}


def load_rounds(path: str) -> list[Round]:
    with open(path, "r") as f:
        return [Round(opponent=code_to_rps[line[0]],
                      you=code_to_rps[line[2]]) for line in f.readlines()]


def load_rounds_2(path: str) -> list[Round2]:
    with open(path, "r") as f:
        return [Round2(opponent=code_to_rps[line[0]],
                       result=code_to_win[line[2]]) for line in f.readlines()]


def play(you: RPS, opponent: RPS) -> int:
    if you == opponent:
        return 3 + you.value
    elif (you.value % 3) + 1 == opponent.value:
        return you.value
    else:
        return 6 + you.value


def play_2(opponent: RPS, result: Result) -> int:
    if result == result.DRAW:
        return 3 + opponent.value
    elif result == result.LOSE:
        if opponent == RPS.ROCK:
            return 3
        else:
            return opponent.value - 1
    else:
        if opponent == RPS.SCISSORS:
            return 7
        else:
            return 6 + opponent.value + 1


def play_rounds(rounds: list[Round]) -> int:
    return sum(play(round.you, round.opponent) for round in rounds)


def play_rounds_2(rounds: list[Round2]) -> int:
    return sum(play_2(round.opponent, round.result) for round in rounds)


if __name__ == "__main__":
    def main():
        print(play_rounds(load_rounds("input/d02.txt")))
        print(play_rounds_2(load_rounds_2("input/d02.txt")))
    main()
