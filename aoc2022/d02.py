from dataclasses import dataclass
from enum import IntEnum


class RPS(IntEnum):
    ROCK: int = 1
    PAPER: int = 2
    SCISSORS: int = 3


class Result(IntEnum):
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
        return 3 + you
    elif (you % 3) + 1 == opponent:
        return you
    else:
        return 6 + you


def play_2(opponent: RPS, result: Result) -> int:
    if result == result.DRAW:
        return 3 + opponent
    elif result == result.LOSE:
        if opponent == RPS.ROCK:
            return 3
        else:
            return opponent - 1
    else:
        if opponent == RPS.SCISSORS:
            return 7
        else:
            return 6 + opponent + 1


def play_rounds(games: list[Round]) -> int:
    return sum(play(game.you, game.opponent) for game in games)


def play_rounds_2(games: list[Round2]) -> int:
    return sum(play_2(game.opponent, game.result) for game in games)


if __name__ == "__main__":
    def main():
        print(play_rounds(load_rounds("input/d02.txt")))
        print(play_rounds_2(load_rounds_2("input/d02.txt")))
    main()
