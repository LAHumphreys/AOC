import itertools
from operator import add


def load_initial_state(path, dimensions=3):
    with open(path) as file:
        lines = file.read().split("\n")
    states = {}
    prefix = tuple([0])*(dimensions-2)
    for y, line in enumerate(lines):
        for x, state in enumerate(line):
            index = prefix + (y,x)
            if state == "#":
                states[index] = 1
            elif state == ".":
                pass
            else:
                raise Exception

    return states


def get_neighbours(index, dimensions=3):
    origin = tuple([0]*dimensions)
    return [tuple(map(add, index, x)) for x in itertools.product([-1, 0, 1], repeat=dimensions) if x != origin]


def step_forward(states, dimensions=3):
    neighbours = {}
    for point in states:
        for neighbour in get_neighbours(point, dimensions):
            if neighbour in neighbours:
                neighbours[neighbour] += 1
            else:
                neighbours[neighbour] = 1

    next_states = {}
    for point in neighbours:
        active_neighbours = neighbours[point]
        if point in states:
            if 1 < active_neighbours < 4:
                next_states[point] = 1
            else:
                # dies
                pass
        elif active_neighbours == 3:
            next_states[point] = 1

    return next_states


def do_steps(states, num_steps, dimensions=3):
    step = 0
    while step < num_steps:
        states = step_forward(states, dimensions=dimensions)
        step += 1
    return states


if __name__ == "__main__":
    def main():
        initial_state = load_initial_state("input/d17.txt")
        step_six = do_steps(initial_state, 6)
        print ("Active at step 6: {0}", len(step_six))

        initial_state = load_initial_state("input/d17.txt", dimensions=4)
        step_six = do_steps(initial_state, 6, dimensions=4)
        print("Active at step 6 in 4d: {0}", len(step_six))
    main()