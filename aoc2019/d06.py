import re

from tools.fileLoader import load_patterns
from tools.tree import KeyedTree

parentChildRegex = re.compile("^([A-Z0-9]+)\\)([A-Z0-9]+)")


class OrbitCounter:
    def __init__(self):
        self.tree = KeyedTree()

    def add(self, orbiting, orbiter):
        self.tree.add_pair(orbiting, orbiter)

    def get_orbits(self):
        count = 0

        def counter(node):
            nonlocal count
            count += node.get_depth()

        self.tree.for_each_node(counter)

        return count

    def get_hops(self, me, santa):
        return len(self.tree.get_path(me, santa)) - 1


if __name__ == "__main__":
    def main():
        pairs = load_patterns(parentChildRegex, "input/d06.txt")
        counter = OrbitCounter()
        for pair in pairs:
            counter.add(pair[0], pair[1])
        print("Orbits: {0}".format(counter.get_orbits()))
        print("Transfers: {0}".format(counter.get_hops("YOU", "SAN")))

    main()
