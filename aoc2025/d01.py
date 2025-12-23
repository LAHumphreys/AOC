def load_sample(file: str) -> list[str]:
    with open(file, "r") as f:
        return f.readlines()

def part1(lines) -> int:
    count = 0
    value = 50
    for line in lines:
        value = apply_rotation(value, line.strip())
        if value == 0:
            count += 1
    return count

def apply_rotation(value: int, rotation: str):
    direction = rotation[0]
    size = int(rotation[1:])
    if direction == 'R':
        return (value + size) % 100
    elif direction == 'L':
        return (value - size) % 100
    else:
        raise ValueError(f"Invalid rotation: {rotation}")


def part2(lines):
    count = 0
    value = 50
    for line in lines:
        line = line.strip()
        rotator = int(line[1:]) # TODO: Fix rotation > 100
        full_rotations = int(rotator / 100)
        count += full_rotations
        direction = line[0]
        rotator = rotator % 100
        if direction == "L" and rotator > value:
            count += 1
            if value == 0:
                count -= 1
        if direction == "R" and rotator > (100-value):
            count += 1
            if value == 0:
                count -= 1
        new_value = apply_rotation(value, line)
        if new_value == 0:
            count += 1
        print(f"{line}: {value} -> {new_value} ({count})")
        value = new_value
    return count


def main():
    with open("input/d01.txt", "r") as f:
        lines = f.readlines()
    print(part1(lines))
    print(part2(lines))


if __name__ == "__main__":
    main()
