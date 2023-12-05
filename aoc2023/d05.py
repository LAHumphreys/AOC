from dataclasses import dataclass
from tools.file_loader import load_string_groups
from copy import deepcopy, copy


@dataclass
class Range:
    start: int
    end: int

    def __lt__(self, other):
        return self.start < other.start


@dataclass
class MapRange:
    source_start: int
    source_end: int
    offset: int

    def __lt__(self, other):
        return self.source_start < other.source_start


@dataclass
class MapBlock:
    map_to: str
    ranges: list[MapRange]


@dataclass
class Instructions:
    seeds: list[int]
    seed_ranges: list[Range]
    maps: dict[str, MapBlock]


def parse_map_range(line: str) -> MapRange:
    destination, source, length = [int(token) for token in line.split()]
    return MapRange(source_start=source,
                    source_end=(source + length -1),
                    offset=(destination-source))


def parse_map_set(lines: [list[str]]) -> list[MapRange]:
    maps = sorted([parse_map_range(line) for line in lines])
    # Note these can overlap
    return maps


def consolidate_ranges(ranges: list[Range]) -> list[Range]:
    result: list[Range] = []
    for next_range in sorted(ranges):
        if result and result[-1].end >= next_range.start:
            raise ValueError
        if result and result[-1].end == (next_range.start -1):
            result[-1].end = next_range.end
        else:
            result += [next_range]
    return result

def apply_map_to_range(start_range: Range, mapper: MapBlock) -> list[Range]:
    unmapped = [deepcopy(start_range)]
    out_ranges: list[Range] = []
    for block in mapper.ranges:
        still_unmapped = []
        for range_to_map in unmapped:
            if range_to_map.start < block.source_start:
                # Still not mapped
                still_unmapped.append(Range(start=range_to_map.start,
                                        end=min(range_to_map.end, block.source_start-1)))
                range_to_map.start = still_unmapped[-1].end + 1
            if block.source_start <= range_to_map.start <= range_to_map.end and \
               range_to_map.start <= block.source_end:
                out_ranges.append(
                    Range(start=range_to_map.start + block.offset,
                          end=min(range_to_map.end, block.source_end) +block.offset))
                range_to_map.start = out_ranges[-1].end - block.offset + 1

            if range_to_map.start <= range_to_map.end:
                still_unmapped.append(range_to_map)
        unmapped = still_unmapped
    # no more maps left to apply
    out_ranges += unmapped

    return consolidate_ranges(out_ranges)




def parse_input(file_name: str) -> Instructions:
    blocks = load_string_groups(file_name)
    seeds = [int(tok) for tok in blocks[0][0].split()[1:]]
    seeds_ranges = []
    for i in range(0, len(seeds), 2):
        seeds_ranges += [Range(start=seeds[i], end=seeds[i] + seeds[i+1])]
    maps = {}
    for block in blocks[1:]:
        source_id, destination_id = block[0].split("-to-")
        destination_id = destination_id.split()[0]
        map_range = parse_map_set(block[1:])
        if source_id in maps:
            raise ValueError
        maps[source_id] = MapBlock(map_to=destination_id, ranges=map_range)
    return Instructions(maps=maps, seeds=seeds, seed_ranges=seeds_ranges)


def locate_range(seeds: list[Range], instructions: Instructions) -> list[Range]:
    source_id = "seed"
    values: list[Range] = copy(seeds)
    while source_id != "location":
        mapper = instructions.maps[source_id]
        new_values = []
        for value in values:
            for new_value in apply_map_to_range(value, mapper):
                new_values += [new_value]
        values = consolidate_ranges(new_values)
        source_id = mapper.map_to

    return values

def locate_seed(seed: int, instructions: Instructions) -> int:
    source_id = "seed"
    value = seed
    while source_id != "location":
        mapper = instructions.maps[source_id]
        valid_maps = []
        for map in mapper.ranges:
            if map.source_start <= value <= map.source_end:
                valid_maps.append(map)
        if len(valid_maps) > 1:
            raise ValueError
        elif len(valid_maps) == 1:
            value += valid_maps[0].offset
        source_id = mapper.map_to

    return value


def part_one(instructions: Instructions) -> int:
    return min(locate_seed(seed, instructions) for seed in instructions.seeds)


def part_two(instructions: Instructions) -> int:
    return locate_range(instructions.seed_ranges, instructions)[0].start


def main():
    instructions = parse_input("input/d05.txt")
    print(part_one(instructions))
    instructions = parse_input("input/d05.txt")
    print(part_two(instructions))
    pass


if __name__ == "__main__":
    main()
