
def calc_depth(lines):
    x_loc: int = 0
    y_loc: int = 0

    tokens = ((c, int(v)) for c, v in (ln.split() for ln in lines))
    for cmd, value in tokens:
        if cmd == "forward":
            x_loc += value
        elif cmd == "up":
            y_loc -= value
        elif cmd == "down":
            y_loc += value

    return x_loc, y_loc


def calc_aim(lines):
    x_loc: int = 0
    y_loc: int = 0
    aim: int = 0

    tokens = ((c, int(v)) for c, v in (ln.split() for ln in lines))
    for cmd, value in tokens:
        if cmd == "forward":
            x_loc += value
            y_loc += aim * value
        elif cmd == "up":
            aim -= value
        elif cmd == "down":
            aim += value

    return x_loc, y_loc


if __name__ == "__main__":
    def main():
        with open("input/d02.txt", encoding="ascii") as file:
            lines = file.readlines()
        depth = calc_depth(lines)
        aim = calc_aim(lines)
        print(depth)
        print (depth[0] * depth[1])
        print(aim)
        print(aim[0] * aim[1])
    main()
