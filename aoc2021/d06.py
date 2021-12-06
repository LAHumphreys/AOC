from typing import List
from copy import copy
from tools.file_loader import load_int_list

def map_state(ages: List[int]) -> List[int]:
    state = [0]*9
    for age in ages:
        state[age]+=1
    return state

def run_model(state: List[int]) -> List[int]:
    next_iteration = copy(state[1:])
    next_iteration[6] += state[0]
    next_iteration.append(state[0])
    return next_iteration


def part_one(ages: List[int], days: int) -> int:
    state = map_state(ages)
    for _ in range(days):
        state = run_model(state)
    return sum(state)

if __name__ == "__main__":
    def main():
        ages = load_int_list("input/d06.txt")
        print (part_one(ages, 80))
        print(part_one(ages, 256))
    main()
