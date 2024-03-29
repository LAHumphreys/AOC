def get_all_seats():
    return list(range(128)), list(range(8))


class UnknownChop(Exception):
    pass


class UnEvenChop(Exception):
    pass


class BadCode(Exception):
    pass


def chop(seats, code):
    rows = len(seats[0])
    cols = len(seats[1])

    if rows % 2 != 0 and code in ["F", "B"]:
        raise UnEvenChop
    if cols % 2 != 0 and code in ["L", "R"]:
        raise UnEvenChop

    if code == "F":
        result = (seats[0][0:rows // 2], seats[1])
    elif code == "B":
        result = (seats[0][rows // 2:], seats[1])
    elif code == "L":
        result = (seats[0], seats[1][0:cols // 2])
    elif code == "R":
        result = (seats[0], seats[1][cols // 2:])
    else:
        raise UnknownChop

    return result


def get_seat(code):
    seats = get_all_seats()
    for seat in code:
        seats = chop(seats, seat)

    if len(seats[0]) != 1:
        raise BadCode
    if len(seats[1]) != 1:
        raise BadCode

    (row, col) = (seats[0][0], seats[1][0])
    seat_id = row * 8 + col

    return row, col, seat_id


if __name__ == "__main__":
    def main():
        with open("input/d05.txt", encoding="ascii") as file_handle:
            max_seat = (0, 0, 0)
            all_seats = {}
            for i in range(128):
                all_seats[i] = []
            for code in file_handle.readlines():
                if code[-1] == "\n":
                    code = code[0:-1]
                this_seat = get_seat(code)
                if this_seat[2] > max_seat[2]:
                    max_seat = this_seat
                row_seats = all_seats[this_seat[0]]
                row_seats.append(this_seat[1])
            print(max_seat)

            for row in all_seats.items():
                cols = row[1]
                if len(cols) != 8:
                    cols.sort()
                    print("incomplete row {0}: {1}".format(row[0], row[1]))


    main()
