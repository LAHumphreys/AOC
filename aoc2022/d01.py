from dataclasses import dataclass

from tools.file_loader import load_int_groups


@dataclass
class Elf:
    carrying: list[int]
    total: int

    def __lt__(self, other):
        return self.total < other.total


def load_elves(path: str):
    return [Elf(carrying=group,
                total=sum(group)) for group in load_int_groups(path)]


def get_elves_with_most(elves: list[Elf], n: int) -> list[Elf]:
    return sorted(elves)[n*-1:]


if __name__ == "__main__":
    def main():
        elves = load_elves("input/d01.txt")
        print(get_elves_with_most(elves, 1))
        print(sum(elf.total for elf in get_elves_with_most(elves, 3)))
    main()
