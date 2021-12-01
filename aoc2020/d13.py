import math


def time_to_wait(bus_period, start_time):
    last_bus = start_time % bus_period
    end_time = 0
    if last_bus != 0:
        end_time = bus_period - last_bus
    return end_time


def calc_part_one(bus_ids, start_time):
    wait_time, bus_id = \
        min((time_to_wait(bus_id, start_time), bus_id) for bus_id in bus_ids)
    return wait_time * bus_id


def load_notes(path):
    with open(path, encoding="ascii") as file:
        lines = file.readlines()
        if len(lines) != 2:
            raise ValueError
        start_time = int(lines[0])
        bus_ids = [int(id) for id in lines[1].split(",") if id != "x"]
    return start_time, bus_ids


def load_notes_with_offset(path):
    with open(path, encoding="ascii") as file:
        lines = file.readlines()
        if len(lines) != 2:
            raise ValueError
        bus_ids = [(int(id), offset) for offset, id in enumerate(lines[1].split(",")) if id != "x"]
    return bus_ids


def find_lcm(first, second):
    return (first * second) // math.gcd(first, second)


def find_next_departure(start_time, bus_1_period, bus_2_period, bus_2_delay):
    """
    Find the first time (t) at, or after) the start_time that:
        bus1 leaves at time t
        bus2 leaves at time t + bus_2_delay

    Subject to the following constraints:
        - bus1 leaves for the first time at start_time, and thereafter every
          bus_1_period minutes
        - bus1 leaves for the first time at t = 0, and thereafter every
          bus_2_period minutes
    """
    current_time = start_time

    # If we're asked to wait for longer than bus_2's departure period,
    # we actually need to wait for several busses to depart...
    bus_2_period = (bus_2_period * (1 + bus_2_delay // bus_2_period))

    while time_to_wait(bus_2_period, current_time) != bus_2_delay:
        current_time += bus_1_period

    return current_time


def find_common_departure_point(busses):
    current_time = 0
    common_departure_period = 1
    for period, delay in busses:
        current_time =\
            find_next_departure(current_time, common_departure_period, period, delay)
        common_departure_period = find_lcm(common_departure_period, period)
    return current_time


if __name__ == "__main__":
    def main():
        start_time, bus_ids = load_notes("input/d13.txt")
        print("Next bus: {0}".format(calc_part_one(bus_ids, start_time)))
        bus_offsets = load_notes_with_offset("input/d13.txt")
        print("Busses will align at: {0}".format(find_common_departure_point(bus_offsets)))
    main()
