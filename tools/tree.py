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


class KeyedNode:
    def __init__(self, key):
        self.id = key
        self.parent = None
        self.children = []

    def get_parent(self):
        return self.parent

    def get_child_nodes(self):
        return self.children

    def traverse(self, callback, depth=0):
        depth += 1
        for c in self.children:
            callback(depth, c)
            c.traverse(callback, depth)

    def set_parent(self, parent):
        if self.parent is not None:
            raise MultipleParentsNotSupported
        elif parent == self:
            raise TreeHasLoop
        else:
            self.parent = parent
            self.parent.children.append(self)

    def get_root_node(self):
        node = self
        while node.parent is not None:
            if node.parent == self:
                raise TreeHasLoop
            else:
                node = node.parent
        return node

    def get_depth(self):
        depth = 0
        node = self
        while node.parent is not None:
            depth += 1
            if node.parent == self:
                raise TreeHasLoop
            else:
                node = node.parent
        return depth

    def get_ancestry(self):
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

    def get_node(self, key):
        if key in self.nodes:
            return self.nodes[key]
        else:
            raise NoSuchNode

    def get_path(self, source, dest):
        if source == dest:
            raise DuplicateNode
        if source not in self.nodes or dest not in self.nodes:
            raise NoSuchNode

        source_hist = self.nodes[source].get_ancestry()
        dest_hist = self.nodes[dest].get_ancestry()

        if len(source_hist) == 0 and len(dest_hist) == 0:
            raise TreeIsSplit
        elif not source_hist and dest_hist[-1] != self.nodes[source]:
            raise TreeIsSplit
        elif not dest_hist and source_hist[-1] != self.nodes[dest]:
            raise TreeIsSplit
        elif not source_hist or not dest_hist:
            # parent / child
            pass
        elif source_hist[-1] != dest_hist[-1]:
            raise TreeIsSplit

        path = []

        for si in range(len(source_hist)):
            s_ancestor = source_hist[si]
            if s_ancestor in dest_hist:
                for di in range(len(dest_hist)):
                    d_ancestor = dest_hist[di]
                    if d_ancestor == s_ancestor:
                        path = source_hist[0:si]
                        while di >= 0:
                            path.append(dest_hist[di])
                            di -= 1
                        break
                break

        return path

    def add_pair(self, parent, child):
        if parent in self.nodes:
            p_node = self.nodes[parent]
        else:
            p_node = self.nodes[parent] = KeyedNode(parent)

        if child in self.nodes:
            c_node = self.nodes[child]
        else:
            c_node = self.nodes[child] = KeyedNode(child)

        c_node.set_parent(p_node)
        pass

    def for_each_node(self, cb):
        for n in self.nodes:
            cb(self.nodes[n])
