from tools.tree import KeyedTree
import re
from tools.fileLoader import LoadPatterns

parentChildRegex = re.compile("^([A-Z0-9]+)\\)([A-Z0-9]+)")

class OrbitCounter:
    def __init__(self):
        self.tree = KeyedTree()

    def Add(self, orbitee, orbiter):
        self.tree.AddPair(orbitee, orbiter)

    def GetOrbits(self):
        count = 0
        def counter(node):
            nonlocal count
            count += node.GetDepth()

        self.tree.ForEachNode(counter)

        return count

    def GetHops(self, me, santa):
        return len(self.tree.GetPath(me, santa))-1

if __name__ == "__main__":
    pairs = LoadPatterns(parentChildRegex, "input/d06.txt")
    counter = OrbitCounter()
    for pair in pairs:
        counter.Add(pair[0], pair[1])
    print ("Orbits: {0}".format(counter.GetOrbits()))
    print ("Transfers: {0}".format(counter.GetHops("YOU", "SAN")))
