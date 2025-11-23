from dataclasses import dataclass

from tools.file_loader import load_lists


@dataclass
class Elf:
    min: int
    max: int


def load_pairs(path: str) -> list[tuple[Elf, Elf]]:
    def make_elf(code: str) -> Elf:
        range_min, range_max = code.split("-")
        return Elf(min=int(range_min), max=int(range_max))

    return [(make_elf(elf_1), make_elf(elf_2))
            for elf_1, elf_2 in load_lists(path)]


def count_overlap(pairs: list[tuple[Elf, Elf]]) -> int:
    def check_overlap(elves: tuple[Elf, Elf]) -> bool:
        first, last = sorted(elves, key=lambda e: e.min)
        return first.min <= last.min and first.max >= last.max

    return sum(map(check_overlap, pairs))


def count_partial_overlap(pairs: list[tuple[Elf, Elf]]) -> int:
    def check_overlap(elves: tuple[Elf, Elf]) -> bool:
        first, last = sorted(elves, key=lambda e: e.min)
        return first.min <= last.min <= first.max

    return sum(map(check_overlap, pairs))


if __name__ == "__main__":
    def main():
        print(count_overlap(load_pairs("input/d04.txt")))
        print(count_partial_overlap(load_pairs("input/d04.txt")))

    main()
