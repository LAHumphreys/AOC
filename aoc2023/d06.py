from dataclasses import dataclass
from math import sqrt, floor, ceil


@dataclass
class Race:
    race_time: int
    max_distance: int


def load_races(file_name: str) -> list[Race]:
    with open(file_name, encoding='utf-8') as input_file:
        times, distances = [line.split(":")[1].strip().strip("\n").split()
                            for line in input_file.readlines()]
        return [Race(race_time=int(time),
                     max_distance=int(distance)) for time, distance in zip(times, distances)]


def calculate_times(race_time: int, record_distance: int) -> int:
    # Distance = (race_time - charge_time) * charge_time
    #=> -1*change_time^2 + race_time*charge_time - Distance = 0
    #=> change_time^2 - race_time*charge_time + Distance = 0
    # charge_time => (race_time +/- sqrt(race_time^2 - 4*Distance) / 2
    #
    max_time = int(floor(race_time + sqrt(race_time**2 - 4*record_distance)) / 2)
    min_time = int(ceil(race_time - sqrt(race_time**2 - 4*record_distance)) / 2)
    if max_time * (race_time - max_time) == record_distance:
        max_time -= 1
    if min_time * (race_time - min_time) <= record_distance:
        min_time += 1

    return max_time - min_time +1


def part_one(races: list[Race]) -> int:
    product = 1
    for race in races:
        product *= calculate_times(race.race_time, race.max_distance)
    return product


def main():
    races = load_races("input/d06.txt")
    print(part_one(races))
    print(calculate_times(race_time=42899189, record_distance=308117012911467))


if __name__ == "__main__":
    main()
