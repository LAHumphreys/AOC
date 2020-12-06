from tools.file_loader import load_ints


def calc_fuel(mass):
    return max((int(mass / 3) - 2), 0)


def calc_rocket_fuel(mass):
    total_fuel = 0
    fuel = calc_fuel(mass)
    while fuel != 0:
        total_fuel += fuel
        fuel = calc_fuel(fuel)

    return total_fuel


def calc_total_fuel(masses):
    fuel = 0
    for mass in masses:
        fuel += calc_fuel(mass)

    return fuel


def total_rocket_fuel(masses):
    fuel = 0
    for mass in masses:
        fuel += calc_rocket_fuel(mass)

    return fuel


if __name__ == "__main__":
    print(calc_total_fuel(load_ints("input/d01.txt")))
    print(total_rocket_fuel(load_ints("input/d01.txt")))
