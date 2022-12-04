from tools.file_loader import load_string_groups
from dataclasses import dataclass
from enum import Enum
from typing import Iterator


@dataclass
class RuckSack:
    all_items: list[int]
    first: list[int]
    last: list[int]


def load_rucksacks(path: str) -> list[RuckSack]:
    packs = []
    with open(path, "r") as f:
        for line in [line.replace("\n", "") for line in f.readlines()]:
            pocket_size = len(line) // 2
            packs.append(RuckSack(
                all_items=sorted(score(x) for x in line),
                first=sorted(score(x) for x in line[:pocket_size]),
                last=sorted(score(x) for x in line[pocket_size:])
            ))
    return packs


def get_groups(packs: list[RuckSack]) -> list[tuple[RuckSack, RuckSack, RuckSack]]:
    return [(packs[i], packs[i+1], packs[i+2]) for i in range (0, len(packs), 3)]


def get_badge(packs: tuple[RuckSack]) -> int:
    iters = [iter(pack.all_items) for pack in packs]

    iter_values = tuple([next(i), i] for i in iters)

    def get_value(pair):
        return pair[0]

    def advance(pair):
        pair[0] = next(pair[1])

    while True:
        first_value = get_value(iter_values[0])
        if all(get_value(pair) == first_value for pair in iter_values):
            return first_value
        advance(min(iter_values, key=get_value))


def score(item: str) -> int:
    if item < 'a':
        return ord(item) - 38
    else:
        return ord(item) - 96


def get_repeat(pack: RuckSack) -> int:
    first_iter = iter(pack.first)
    last_iter = iter(pack.last)

    first = next(first_iter)
    last = next(last_iter)
    while True:
        if first == last:
            return first
        elif first < last:
            first = next(first_iter)
        else:
            last = next(last_iter)


if __name__ == "__main__":
    def main():
        packs = load_rucksacks("input/d03.txt")
        print(sum(get_repeat(pack) for pack in packs))
        print(sum(get_badge(group) for group in get_groups(packs)))


    main()
