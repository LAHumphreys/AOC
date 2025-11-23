from dataclasses import dataclass
from typing import List, Type, Dict, Optional
from enum import Enum
from copy import copy
from bisect import insort_left


class Unhandled(Exception):
    pass


class AmphipodType(Enum):
    AMBER = "A"
    BRONZE = "B"
    COPPER = "C"
    DESERT = "D"


@dataclass
class Amphipod:
    type: AmphipodType
    unit_cost: int


@dataclass
class Room:
    type: AmphipodType
    spaces: List[Optional[Amphipod]]
    join_index: int


@dataclass
class Cave:
    rooms: List[Room]
    corridor: List[Optional[Amphipod]]
    total_cost: int = 0
    idealised_cost: Optional[int] = None

    def get_idealised_cost(self):
        if not self.idealised_cost:
            self.idealised_cost = get_idealised_completion_cost(self)
        return self.idealised_cost

    def __lt__(self: Type['Cave'], other: Type['Cave']):
        return self.get_idealised_cost() < other.get_idealised_cost()


def get_empty_cave():
    cave = Cave(
        corridor=[None]*11,
        rooms=[
            Room(type=AmphipodType.AMBER,  spaces=[None] * 2, join_index=2),
            Room(type=AmphipodType.BRONZE, spaces=[None] * 2, join_index=4),
            Room(type=AmphipodType.COPPER, spaces=[None] * 2, join_index=6),
            Room(type=AmphipodType.DESERT, spaces=[None] * 2, join_index=8),
        ]
    )
    return cave


def get_cave_hash(cave: Cave) -> str:
    cave_hash = ""
    for space in cave.corridor:
        if space:
            cave_hash += space.type.value
        else:
            cave_hash += "."
    for room in cave.rooms:
        for space in room.spaces:
            if space:
                cave_hash += space.type.value
            else:
                cave_hash += "."
    return cave_hash


def get_amber() -> Amphipod:
    return Amphipod(type=AmphipodType.AMBER, unit_cost=1)


def get_bronze() -> Amphipod:
    return Amphipod(type=AmphipodType.BRONZE, unit_cost=10)


def get_copper() -> Amphipod:
    return Amphipod(type=AmphipodType.COPPER, unit_cost=100)


def get_desert() -> Amphipod:
    return Amphipod(type=AmphipodType.DESERT, unit_cost=1000)


def get_idealised_completion_cost(cave: Cave) -> int:
    def home_index(pod_type: AmphipodType):
        if pod_type == AmphipodType.AMBER:
            return 2
        if pod_type == AmphipodType.BRONZE:
            return 4
        if pod_type == AmphipodType.COPPER:
            return 6
        if pod_type == AmphipodType.DESERT:
            return 8
        raise Unhandled
    room_costs = (1, 10, 100, 1000)
    cost = 0
    num_spaces = len(cave.rooms[0].spaces)
    for i, amphipod in enumerate(cave.corridor):
        if amphipod:
            cost += amphipod.unit_cost * (abs(home_index(amphipod.type)-i) + 1)
    for i, room in enumerate(cave.rooms):
        for space_index, amphipod in enumerate(room.spaces):
            if amphipod and amphipod.type != room.type:
                spaces_to_move = (1 + num_spaces - space_index) +\
                                 abs(room.join_index - home_index(amphipod.type))
                cost += spaces_to_move * amphipod.unit_cost
            if space_index < (num_spaces - 1) and (not amphipod or amphipod.type != room.type):
                cost += room_costs[i] * (num_spaces - space_index - 1)
    return cave.total_cost + cost


def get_amphipod(code: str) -> Amphipod:
    if code == "A":
        return get_amber()
    if code == "B":
        return get_bronze()
    if code == "C":
        return get_copper()
    if code == "D":
        return get_desert()
    if code == ".":
        return None
    raise Unhandled


def load_cave(path: str) -> Cave:
    with open(path, encoding="ascii") as file:
        lines = [line.replace("\n", "") for line in file.readlines()]

    if lines[0] != "#############":
        raise Unhandled

    cave = get_empty_cave()

    for i in range(1, 12):
        cave.corridor[i-1] = get_amphipod(lines[1][i])

    i = 2
    loaded_rooms = [[] for _ in cave.rooms]
    while lines[i] != "  #########":
        for room_index, room in enumerate(cave.rooms):
            loaded_rooms[room_index].append(get_amphipod(lines[i][room.join_index+1]))
        i += 1
    for room_index, room in enumerate(cave.rooms):
        room.spaces = list(reversed(loaded_rooms[room_index]))

    return cave


def clone_cave(cave: Cave) -> Cave:
    new_cave = get_empty_cave()
    new_cave.total_cost = cave.total_cost
    new_cave.corridor = copy(cave.corridor)
    new_cave.rooms = [
        Room(join_index=cave.rooms[0].join_index,
             type=cave.rooms[0].type,
             spaces=copy(cave.rooms[0].spaces)),
        Room(join_index=cave.rooms[1].join_index,
             type=cave.rooms[1].type,
             spaces=copy(cave.rooms[1].spaces)),
        Room(join_index=cave.rooms[2].join_index,
             type=cave.rooms[2].type,
             spaces=copy(cave.rooms[2].spaces)),
        Room(join_index=cave.rooms[3].join_index,
             type=cave.rooms[3].type,
             spaces=copy(cave.rooms[3].spaces)),
    ]
    return new_cave


def auto_shunt(cave: Cave):
    for room in cave.rooms:
        i = 0
        last_filled = -1
        all_valid = True
        while all_valid and i < len(room.spaces):
            if room.spaces[i] and room.spaces[i].type == room.type:
                amphipod = room.spaces[i]
                room.spaces[i] = None
                room.spaces[last_filled + 1] = amphipod
                last_filled += 1
                cave.total_cost += amphipod.unit_cost * (i - last_filled)
            elif room.spaces[i] and room.spaces[i].type != room.type:
                all_valid = False
            i += 1
        i = room.join_index
        while all_valid and last_filled < (len(room.spaces) - 1) and i < len(cave.corridor):
            if cave.corridor[i]:
                amphipod = cave.corridor[i]
                if amphipod.type == room.type:
                    cave.corridor[i] = None
                    room.spaces[last_filled+1] = amphipod
                    last_filled += 1
                    cave.total_cost += amphipod.unit_cost *\
                                       (i - room.join_index + len(room.spaces) - last_filled)
                else:
                    break
            i += 1
        i = room.join_index
        while all_valid and last_filled < (len(room.spaces) - 1) and i > 0:
            if cave.corridor[i]:
                amphipod = cave.corridor[i]
                if amphipod.type == room.type:
                    cave.corridor[i] = None
                    room.spaces[last_filled+1] = amphipod
                    last_filled += 1
                    cave.total_cost += amphipod.unit_cost *\
                                       (abs(i - room.join_index) + len(room.spaces) - last_filled)
                else:
                    break
            i -= 1


def get_valid_corridor_exits(cave: Cave) -> List[Cave]:
    possible_caves = []

    def move_to_room(corridor_index: int, to_room: Room, slot: int) -> Cave:
        spaces = abs(to_room.join_index - corridor_index)
        new_cave = clone_cave(cave)
        new_room = [cloned_room for cloned_room in new_cave.rooms
                                if cloned_room.join_index == to_room.join_index][0]
        amphipod = new_cave.corridor[corridor_index]
        new_cave.corridor[corridor_index] = None
        new_room.spaces[slot] = amphipod
        new_cave.total_cost += ((len(to_room.spaces)-slot) + spaces) * amphipod.unit_cost
        return new_cave

    def _get_space_index(_room: Room):
        all_correct = True
        greatest_taken_index = -1
        for index, amphipod in enumerate(_room.spaces):
            if amphipod:
                greatest_taken_index = index
                if amphipod.type != _room.type:
                    all_correct = False
        if all_correct:
            return greatest_taken_index+1
        return len(_room.spaces)-1

    def room_is_open(_room):
        is_open = True
        if _room.spaces[-1] is not None:
            is_open = False
        for amphipod in _room.spaces:
            if amphipod and amphipod.type != _room.type:
                is_open = False
        return is_open

    # Only interested in open rooms
    for room in (room for room in cave.rooms if room_is_open(room)):
        i = room.join_index
        while i >= 0:
            if cave.corridor[i]:
                if cave.corridor[i].type == room.type:
                    space_index = _get_space_index(room)
                    possible_caves.append(move_to_room(i, room, space_index))
                break
            i -= 1

        i = room.join_index
        while i < len(cave.corridor):
            if cave.corridor[i]:
                if cave.corridor[i].type == room.type:
                    space_index = _get_space_index(room)
                    possible_caves.append(move_to_room(i, room, space_index))
                break
            i += 1

    return possible_caves


def get_valid_room_exits(cave: Cave, room: Room) -> List[Cave]:
    caves = []
    amphipod = None
    spaces_moved = 0
    new_room = Room(
        type=room.type,
        join_index=room.join_index,
        spaces=copy(room.spaces))
    i = len(room.spaces) - 1
    while i >= 0 and not amphipod:
        if room.spaces[i]:
            amphipod = room.spaces[i]
            new_room.spaces[i] = None
            spaces_moved = len(room.spaces) - 1 - i
        i -= 1

    if amphipod:
        max_below = -1
        min_above = 20
        for i, space in enumerate(cave.corridor):
            if space and room.join_index > i > max_below:
                max_below = i
            if space and room.join_index < i < min_above:
                min_above = i
        for i in (0, 1, 3, 5, 7, 9, 10):
            if max_below < i < min_above:
                new_cave = clone_cave(cave)
                for cloned_room in new_cave.rooms:
                    if cloned_room.join_index == new_room.join_index:
                        cloned_room.spaces = copy(new_room.spaces)
                new_cave.corridor[i] = copy(amphipod)
                new_spaces_moved = spaces_moved + abs(i - room.join_index) + 1
                new_cave.total_cost += new_spaces_moved*amphipod.unit_cost
                caves.append(new_cave)
    return caves


class SortedCaveList:
    def __init__(self):
        self.caves: List[Cave] = []
        self.cost_by_id: Dict[str, int] = {}
        self.best_completion = None

    def has_completion(self) -> bool:
        return self.best_completion is not None

    def get_completion(self) -> Optional[Cave]:
        return self.best_completion

    def pop(self) -> Cave:
        self._prune()
        return self.caves.pop(0)

    def has_more(self) -> bool:
        self._prune()
        return bool(self.caves)

    def _is_valid_cave_to_add(self, cave: Cave):
        valid: bool = False
        if not self.has_completion() or (
                self.get_completion().total_cost > cave.total_cost and
                self.get_completion().total_cost >= cave.get_idealised_cost()):
            cave_id = get_cave_hash(cave)
            if cave_id not in self.cost_by_id or self.cost_by_id[cave_id] > cave.total_cost:
                valid = True
        return valid

    def _is_still_valid(self, cave: Cave):
        valid: bool = False
        if not self.has_completion() or\
                (self.get_completion().total_cost >= cave.total_cost and
                 self.get_completion().total_cost >= cave.get_idealised_cost()):
            cave_id = get_cave_hash(cave)
            if cave_id not in self.cost_by_id or self.cost_by_id[cave_id] >= cave.total_cost:
                valid = True
        return valid

    def _prune(self):
        i = 0
        while i < len(self.caves) and not self._is_still_valid(self.caves[i]):
            i += 1
        self.caves = self.caves[i:]

    def add(self, cave: Cave):
        if self._is_valid_cave_to_add(cave):
            cave_id = get_cave_hash(cave)
            insort_left(self.caves, cave)
            self.cost_by_id[cave_id] = cave.total_cost
            if is_complete(cave):
                self.best_completion = cave


def is_complete(cave: Cave) -> bool:
    count = 0
    for room in cave.rooms:
        for slot in room.spaces:
            if slot and slot.type == room.type:
                count += 1
    return count == len(cave.rooms) * len(cave.rooms[0].spaces)


def add_possible_caves(cave: Cave, known_caves: SortedCaveList):
    for room in cave.rooms:
        for possibility in get_valid_room_exits(cave, room):
            auto_shunt(possibility)
            known_caves.add(possibility)
    for possibility in get_valid_corridor_exits(cave):
        auto_shunt(possibility)
        known_caves.add(possibility)


def find_completion_cost(cave: Cave) -> int:
    sorted_caves: SortedCaveList = SortedCaveList()
    auto_shunt(cave)
    sorted_caves.add(cave)
    checked = 0
    while sorted_caves.has_more():
        next_cave = sorted_caves.pop()
        if checked % 1000 == 0:
            if sorted_caves.has_completion():
                print(f"Checked: {checked}, best: {sorted_caves.get_completion().total_cost}")
            else:
                print(f"Checked: {checked}, next idealised: {next_cave.idealised_cost}")
        checked += 1
        add_possible_caves(next_cave, sorted_caves)
    return sorted_caves.get_completion().total_cost


if __name__ == "__main__":
    def main():
        cave = load_cave("input/d23.txt")
        print(find_completion_cost(cave))
        extended_cave = load_cave("input/d23_extended.txt")
        print(find_completion_cost(extended_cave))
    main()
