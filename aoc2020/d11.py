import copy
from enum import Enum


class SeatState(Enum):
    NO_SEAT = 0
    EMPTY = 1
    FILLED = 2


def load_state(path):
    seat_map = {
        ".": SeatState.NO_SEAT,
        "#": SeatState.FILLED,
        "L": SeatState.EMPTY,
    }
    result = []
    with open(path, encoding="ascii") as file:
        for line in file.read().split("\n"):
            result.append([seat_map[char] for char in line])
    return result


def count_adjacent_occupied(seats, seat_row, seat_column):
    return count_next_occupied(seats, seat_row, seat_column, True)


def count_next_occupied(seats, seat_row, seat_column, adjacent_only=False):
    number_of_rows = len(seats)
    number_of_columns = len(seats[0])

    def in_bounds(row_index, column_index):
        return 0 <= row_index < number_of_rows and \
               0 <= column_index < number_of_columns

    def is_not_seat(row_index, column_index):
        return seats[row_index][column_index] == SeatState.NO_SEAT

    def is_filled_seat(row_index, column_index):
        return seats[row_index][column_index] == SeatState.FILLED

    seats_to_check = [[-1, -1], [-1, 0], [-1, 1],
                      [0, -1], [0, 1],
                      [1, -1], [1, 0], [1, 1]]

    count = 0
    for [delta_row, delta_column] in seats_to_check:
        row = seat_row + delta_row
        column = seat_column + delta_column
        while not adjacent_only and in_bounds(row, column) and is_not_seat(row, column):
            row += delta_row
            column += delta_column

        if in_bounds(row, column) and is_filled_seat(row, column):
            count += 1

    return count


def stepper(seats, counter, too_busy_threshold):
    def will_be_filled(row_index, column_index):
        return counter(seats, row_index, column_index) == 0

    def will_be_vacated(row_index, column_index):
        return counter(seats, row_index, column_index) >= too_busy_threshold

    updates = 0
    results = copy.deepcopy(seats)
    for row, row_seats in enumerate(seats):
        for column, seat in enumerate(row_seats):
            if seat == SeatState.EMPTY and will_be_filled(row, column):
                results[row][column] = SeatState.FILLED
                updates += 1
            elif seat == SeatState.FILLED and will_be_vacated(row, column):
                results[row][column] = SeatState.EMPTY
                updates += 1

    return results, updates


def single_step(seats):
    return stepper(seats, count_adjacent_occupied, 4)


def single_step_part_2(seats):
    return stepper(seats, count_next_occupied, 5)


def loop_until_stable(seats, step_function=single_step):
    updates = -1
    while updates != 0:
        [seats, updates] = step_function(seats)
    return seats


def loop_until_stable_part_2(seats):
    return loop_until_stable(seats, single_step_part_2)


def number_seated(seats):
    count = 0
    for row in seats:
        count += sum(seat == SeatState.FILLED for seat in row)
    return count


if __name__ == "__main__":
    def main():
        initial_state = load_state("input/d11.txt")
        final_state = loop_until_stable(initial_state)
        print("Seated: {0}".format(number_seated(final_state)))
        final_state_part_2 = loop_until_stable_part_2(initial_state)
        print("Seated: {0}".format(number_seated(final_state_part_2)))


    main()
