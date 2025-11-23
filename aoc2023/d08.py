from dataclasses import dataclass
from math import lcm

from tools.file_loader import load_string_groups


@dataclass
class Node:
    left: str
    right: str


@dataclass
class Map:
    nodes: dict[str, Node]
    directions: str


def load_map(file_name:str) -> Map:
    # pylint: disable=unbalanced-tuple-unpacking
    directions, nodes = load_string_groups(file_name)
    # pylint: enable=unbalanced-tuple-unpacking
    node_map = {}
    for node_str in nodes:
        node_id, neighbour_str = node_str.split(" = ")
        left, right = neighbour_str.replace("(", "").replace(")", "").split(",")
        left, right = left.strip(), right.strip()
        node_map[node_id] = Node(left=left, right=right)
    return Map(nodes=node_map, directions=directions[0])


def part_one(node_map: Map, start_node: str="AAA") -> int:
    steps = 0
    node_id = start_node
    num_directions = len(node_map.directions)
    while node_id != "ZZZ":
        if node_map.directions[steps%num_directions] == "L":
            node_id = node_map.nodes[node_id].left
        else:
            node_id = node_map.nodes[node_id].right
        steps += 1
    return steps


def part_two(node_map: Map) -> int:
    current_nodes = [node_id for node_id in node_map.nodes.keys() if node_id[-1] == "A"]
    num_directions = len(node_map.directions)
    part_one_steps = []
    for node_id in current_nodes:
        steps = 0
        while node_id[-1] != "Z":
            if node_map.directions[steps % num_directions] == "L":
                node_id = node_map.nodes[node_id].left
            else:
                node_id = node_map.nodes[node_id].right
            steps += 1
        part_one_steps.append(steps)
    return lcm(*part_one_steps)


def main():
    node_map = load_map("input/d08.txt")
    print(part_one(node_map))
    print(part_two(node_map))


if __name__ == "__main__":
    main()
