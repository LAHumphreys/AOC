from dataclasses import dataclass
from typing import Optional, Callable, List
from math import floor, ceil
from copy import deepcopy
import ast


@dataclass
class SnailFishNode:
    value: Optional[int] = None
    left: Optional['SnailFishNode'] = None
    right: Optional['SnailFishNode'] = None
    left_depth: int = 0
    right_depth: int = 0
    parent: Optional['SnailFishNode'] = None


class Unhandled(Exception):
    pass


def encode_to_nodes(raw_snail_n: list) -> SnailFishNode:
    if len(raw_snail_n) != 2:
        raise Unhandled

    left, right = raw_snail_n

    if isinstance(left, int):
        left = SnailFishNode(value=left)
    else:
        left = encode_to_nodes(left)

    if isinstance(right, int):
        right = SnailFishNode(value=right)
    else:
        right = encode_to_nodes(right)

    return add(left, right)


def decode_to_lists(root_node: SnailFishNode):
    if root_node.value is not None:
        return root_node.value

    return [decode_to_lists(root_node.left), decode_to_lists(root_node.right)]


def add(lhs: SnailFishNode, rhs: SnailFishNode) -> SnailFishNode:
    if lhs.parent or lhs.parent:
        raise Unhandled

    root = SnailFishNode(left=lhs,
                         left_depth=max(lhs.left_depth, lhs.right_depth) + 1,
                         right=rhs,
                         right_depth=max(rhs.left_depth, rhs.right_depth) + 1)
    lhs.parent = root
    rhs.parent = root
    return root


def find_first_at_depth(root: SnailFishNode, depth: int) -> Optional[SnailFishNode]:
    if depth == 1:
        return root

    if root.left_depth >= depth:
        return find_first_at_depth(root.left, depth-1)

    if root.right_depth >= depth:
        return find_first_at_depth(root.right, depth-1)

    return None


def _reduce_depth(child: SnailFishNode):
    if child.parent:
        parent = child.parent
        if parent.left is child:
            parent.left_depth -= 1
            if parent.left_depth >= parent.right_depth:
                _reduce_depth(parent)
        elif parent.right is child:
            parent.right_depth -= 1
            if parent.right_depth >= parent.left_depth:
                _reduce_depth(parent)
        else:
            raise Unhandled


def _increase_depth(child: SnailFishNode):
    if child.parent:
        parent = child.parent
        if parent.left is child:
            parent.left_depth += 1
            if parent.left_depth > parent.right_depth:
                _increase_depth(parent)
        elif parent.right is child:
            parent.right_depth += 1
            if parent.right_depth > parent.left_depth:
                _increase_depth(parent)
        else:
            raise Unhandled


def find_value_to_right(start: SnailFishNode) -> Optional[SnailFishNode]:
    node = None
    if start.parent is not None:
        parent = start.parent
        if parent.right is start:
            node = find_value_to_right(parent)
        else:
            node = parent.right
            while node.value is None:
                node = node.left

    return node


def find_value_to_left(start: SnailFishNode) -> Optional[SnailFishNode]:
    node = None
    if start.parent is not None:
        parent = start.parent
        if parent.left is start:
            node = find_value_to_left(parent)
        else:
            node = parent.left
            while node.value is None:
                node = node.right

    return node


def _explode_node(to_explode: SnailFishNode):
    _reduce_depth(to_explode)
    parent = to_explode.parent
    rhs_value_node = find_value_to_right(to_explode)
    lhs_value_node = find_value_to_left(to_explode)

    if parent.left and parent.left is to_explode:
        parent.left = SnailFishNode(value=0, parent=parent)
    elif parent.right and parent.right is to_explode:
        parent.right = SnailFishNode(value=0, parent=parent)
    else:
        raise Unhandled

    rhs_value = to_explode.right.value
    lhs_value = to_explode.left.value
    if rhs_value_node is not None:
        rhs_value_node.value += rhs_value
    if lhs_value_node is not None:
        lhs_value_node.value += lhs_value


def find_first_value(root: SnailFishNode, pred: Callable[[int], bool]) -> Optional[SnailFishNode]:
    node = None
    if root.value is not None:
        if pred(root.value):
            node = root
    else:
        node = find_first_value(root.left, pred)
        if node is None:
            node = find_first_value(root.right, pred)
    return node


def _split_node(to_split: SnailFishNode):
    _increase_depth(to_split)
    parent = to_split.parent
    left = SnailFishNode(value=floor(to_split.value / 2.0))
    right = SnailFishNode(value=ceil(to_split.value / 2.0))
    split_node = add(left, right)
    split_node.parent = parent
    if parent.left and parent.left is to_split:
        parent.left = split_node
    elif parent.right and parent.right is to_split:
        parent.right = split_node


def load_snail_numbers(path: str) -> List[SnailFishNode]:
    with open(path, encoding="ascii") as file:
        return [encode_to_nodes(ast.literal_eval(raw_sn)) for raw_sn in file.readlines()]


def reduce(root: SnailFishNode):
    reduced = False
    to_explode = find_first_at_depth(root, 5)
    if to_explode is not None:
        _explode_node(to_explode)
        reduced = True
    else:
        to_split = find_first_value(root, lambda value: value >= 10)
        if to_split:
            _split_node(to_split)
            reduced = True
    return reduced


def full_reduce(root: SnailFishNode):
    while reduce(root):
        pass


def sn_sum(numbers: List[SnailFishNode]) -> SnailFishNode:
    total = add(numbers[0], numbers[1])
    full_reduce(total)
    for rhs in numbers[2:]:
        total = add(total, rhs)
        full_reduce(total)
    return total


def magnitude(number: SnailFishNode) -> int:
    if number.value is not None:
        return number.value
    return 3*magnitude(number.left) + 2*magnitude(number.right)


def largest_magnitude(numbers: List[SnailFishNode]) -> int:
    largest = 0
    for lhs in numbers:
        for rhs in numbers:
            if lhs is not rhs:
                mag = magnitude(sn_sum([deepcopy(lhs), deepcopy(rhs)]))
                largest = max(largest, mag)
    return largest


if __name__ == "__main__":
    def main():
        numbers = load_snail_numbers("input/d18.txt")
        total = sn_sum(numbers)
        print(decode_to_lists(total))
        print(magnitude(total))
        numbers = load_snail_numbers("input/d18.txt")
        print(largest_magnitude(numbers))
    main()
