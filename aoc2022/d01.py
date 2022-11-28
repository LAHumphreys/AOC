from tools.file_loader import load_ints


def last(numbers: list[int]) -> int:
    return numbers[-1]


if __name__ == "__main__":
    def main():
        numbers = load_ints("input/d01.txt")
        print(last(numbers))
    main()
