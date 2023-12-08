from dataclasses import dataclass
from tools.file_loader import load_string_groups
from math import lcm


@dataclass
class Node:
    left: str
    right: str


@dataclass
class Map:
    nodes: dict[str, Node]
    directions: str


def load_map(file_name:str) -> Map:
    directions, nodes = load_string_groups(file_name)
    node_map = {}
    for node_str in nodes:
        node_id, neighbour_str = node_str.split(" = ")
        left, right = neighbour_str.replace("(", "").replace(")", "").split(",")
        left, right = left.strip(), right.strip()
        node_map[node_id] = Node(left=left, right=right)
    return Map(nodes=node_map, directions=directions[0])


def part_one(map: Map, start_node: str="AAA") -> int:
    steps = 0
    node_id = start_node
    num_directions = len(map.directions)
    while node_id != "ZZZ":
        if map.directions[steps%num_directions] == "L":
            node_id = map.nodes[node_id].left
        else:
            node_id = map.nodes[node_id].right
        steps += 1
    return steps


def part_two(map: Map) -> int:
    current_nodes = [node_id for node_id in map.nodes.keys() if node_id[-1] == "A"]
    num_directions = len(map.directions)
    part_one_steps = []
    for node_id in current_nodes:
        steps = 0
        while node_id[-1] != "Z":
            if map.directions[steps % num_directions] == "L":
                node_id = map.nodes[node_id].left
            else:
                node_id = map.nodes[node_id].right
            steps += 1
        part_one_steps.append(steps)
    return lcm(*part_one_steps)


def main():
    map = load_map("input/d08.txt")
    print(part_one(map))
    print(part_two(map))
    pass


if __name__ == "__main__":
    main()
