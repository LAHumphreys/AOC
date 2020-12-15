COUNT_TO = 30000000


# COUNT_TO=2020

def part_one(numbers):
    i = 0
    while i < COUNT_TO:
        found = False
        for index, number in enumerate(reversed(numbers[:-1])):
            if number == numbers[-1]:
                found = True
                numbers.append(index + 1)
                break
        if not found:
            numbers.append(0)
        i += 1
    return numbers[COUNT_TO - 1]


def part_two(numbers, target):
    index = [None for i in range(target)]
    for i, number in enumerate(numbers[:-1]):
        if number in numbers:
            index[number] = i

    i = len(numbers)
    last = numbers[-1]
    previous = i -1
    runs = 0
    while i < target:
        if i % 1000000 == 0:
            print(i)
        found = index[last]
        if found is None:
            next = 0
        else:
            next = i - found - 1
        index[last] = i - 1
        last = next
        i += 1
    return last


if __name__ == "__main__":
    def main():
        print(part_two([1, 2, 16, 19, 18, 0], 2020))
        print(part_two([1, 2, 16, 19, 18, 0], 30000000))
        pass


    main()
