from tools.file_loader import load_int_groups
from dataclasses import dataclass


@dataclass
class Elf:
    carrying: list[int]
    total: int


def load_elves(path: str):
    return [Elf(carrying=group,
                total=sum(group)) for group in load_int_groups(path)]
