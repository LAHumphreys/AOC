

class MultipleParentsNotSupported(Exception):
    pass

class TreeHasLoop(Exception):
    pass

class TreeIsSplit(Exception):
    pass

class NoSuchNode(Exception):
    pass

class DuplicateNode(Exception):
    pass

class KeyedNode():
    def __init__(self, id):
        self.id = id
        self.parent = None
        self.children = []

    def GetParent(self):
        return self.parent

    def GetChildNodes(self):
        return self.children

    def Traverse(self, callback, depth=0):
        depth += 1
        for c in self.children:
            callback(depth, c)
            c.Traverse(callback, depth)

    def SetParent(self, parent):
        if self.parent is not None:
            raise MultipleParentsNotSupported
        elif parent == self:
            raise TreeHasLoop
        else:
            self.parent = parent
            self.parent.children.append(self)

    def GetRootNode(self):
        node = self
        while node.parent is not None:
            if node.parent == self:
                raise TreeHasLoop
            else:
                node = node.parent
        return node

    def GetDepth(self):
        depth = 0
        node = self
        while node.parent is not None:
            depth += 1
            if node.parent == self:
                raise TreeHasLoop
            else:
                node = node.parent
        return depth

    def GetAncestory(self):
        result = []
        node = self
        while node.parent is not None:
            if node.parent == self:
                raise TreeHasLoop
            else:
                result.append(node.parent)
            node = node.parent

        return result


    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.id < other.id

    def __repr__(self):
        return "<KeyedNode: {0}>".format(self.id)

    def __str__(self):
        return self.__repr__()


class KeyedTree:
    def __init__(self):
        self.nodes = {}
        pass

    def GetNode(self, id):
        if id in self.nodes:
            return self.nodes[id]
        else:
            raise NoSuchNode

    def GetPath(self, source, dest):
        if source == dest:
            raise DuplicateNode
        if source not in self.nodes or dest not in self.nodes:
            raise NoSuchNode

        sourceHist = self.nodes[source].GetAncestory()
        destHist = self.nodes[dest].GetAncestory()

        if len(sourceHist) == 0 and len(destHist) == 0:
            raise TreeIsSplit
        elif not sourceHist and destHist[-1] != self.nodes[source]:
            raise TreeIsSplit
        elif not destHist and sourceHist[-1] != self.nodes[dest]:
            raise TreeIsSplit
        elif not sourceHist or not destHist:
            # parent / child
            pass
        elif sourceHist[-1] != destHist[-1]:
            raise TreeIsSplit

        path = []

        for si in range(len(sourceHist)):
            sAncestor = sourceHist[si]
            if sAncestor in destHist:
                for di in range(len(destHist)):
                    dAncestor = destHist[di]
                    if dAncestor == sAncestor:
                        path = sourceHist[0:si]
                        while di >= 0:
                            path.append(destHist[di])
                            di -= 1
                        break
                break




        return path


    def AddPair(self, parent, child):
        if parent in self.nodes:
            pnode = self.nodes[parent]
        else:
            pnode = self.nodes[parent] = KeyedNode(parent)

        if child in self.nodes:
            cnode = self.nodes[child]
        else:
            cnode = self.nodes[child] = KeyedNode(child)

        cnode.SetParent(pnode)
        pass

    def ForEachNode(self, cb):
        for n in self.nodes:
            cb(self.nodes[n])