from tools.fileLoader import LoadInts
def CalcFuel(mass):
    return max((int(mass/ 3) - 2), 0)

def CalcRocketFuel(mass):
    total_fuel = 0;
    fuel = CalcFuel(mass)
    while (fuel != 0):
        total_fuel += fuel
        fuel = CalcFuel(fuel)

    return total_fuel

def TotalFuel(masses):
    fuel = 0;
    for m in masses:
        fuel += CalcFuel(m)

    return fuel

def TotalRocketFuel(masses):
    fuel = 0;
    for m in masses:
        fuel += CalcRocketFuel(m)

    return fuel


if __name__ == "__main__":
    print(TotalFuel(LoadInts("input/d01.txt")))
    print(TotalRocketFuel(LoadInts("input/d01.txt")))
