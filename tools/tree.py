"""
Tools for manipulating graphs and trees
"""


class MultipleParentsNotSupported(Exception):
    """
    Raise in single parent trees when attempting to assign a second parent to
    a node
    """


class TreeHasLoop(Exception):
    """
    Raised when a loop is detected within a tree
    """


class TreeIsSplit(Exception):
    """
    Raised if a set of nodes is split into multiple trees, and an operation
    requires them to be in a single tree
    """


class NoSuchNode(Exception):
    """
    Raised when attempting to retrieve a node with a key which is unknown to
    the set
    """


class DuplicateNode(Exception):
    """
    Raised in a key tree, when attempting to create a second node with the
    same key
    """


class KeyedNode:
    """
    A node in a tree with:
      - An associated identifier (provided a construction time)
      - 0 or 1 parent nodes
      - 0, 1 or many child nodes

    The identifier must implement the __eq__ method and be findable
    via `x in <list>`
    """

    def __init__(self, key):
        self.key = key
        self.parent = None
        self.children = []

    def get_parent(self):
        """
        Return the parent node
        :return: The node, or None if there is no parent
        """
        return self.parent

    def get_child_nodes(self):
        """
        Return the list of child nodes. Sort order is undefined.
        """
        return self.children

    def get_root_node(self):
        """
        Get the top of the tree
        :return: The node object at the top of the tree. If this node is the top of the tree,
                 (it has no parent), then it will be returned.
        """
        node = self
        while node.parent is not None:
            if node.parent == self:
                raise TreeHasLoop
            node = node.parent
        return node

    def get_depth(self):
        """
        Compute the depth of this node in the tree, by traversing up to the parent

        :return: The number of nodes above this node in the tree
        """
        depth = 0
        node = self
        while node.parent is not None:
            depth += 1
            if node.parent == self:
                raise TreeHasLoop
            node = node.parent
        return depth

    def get_ancestry(self):
        """
        Return the list of all nodes in a direct path to the root node. If we have no parent,
        an empty list is returned.

        A loop results in TreeHasLoop being thrown

        :return: The list of nodes: [parent, grand_parent, great_grand_parent, ..., root_node]
        """
        result = []
        node = self
        while node.parent is not None:
            if node.parent == self:
                raise TreeHasLoop
            result.append(node.parent)
            node = node.parent

        return result

    def set_parent(self, parent):
        """
        Add this node to the list of children of node parent.

        This function does the necessary updates to both this node and the new parent node.

        If we already have a parent node, MultipleParentsNotSupported is thrown

        :param parent: The node to add ourselves to
        """
        if self.parent is not None:
            raise MultipleParentsNotSupported

        if parent == self:
            raise TreeHasLoop

        self.parent = parent
        self.parent.children.append(self)

    def traverse(self, callback, starting_depth=0):
        """
        Trigger a callback for each node below this node in the tree

        callback signature:
           def callback(depth: int, node: KeyedNode)
               depth: The depth of this node, with this node considered to
                      be at starting_starting_depth
               node:  The child node

        Callback order is undefined. Only child nodes are returned, not
        this node. A loop will result in TreeHasLoop being thrown,
        but only after it is detected by returning to this node.

        :param callback: The method to callback on
        :param starting_depth: Added to depth before triggering the callback
        """
        starting_depth += 1
        for child in self.children:
            callback(starting_depth, child)
            child.traverse(callback, starting_depth)

    def __eq__(self, other):
        return self.key == other.key

    def __lt__(self, other):
        return self.key < other.key

    def __repr__(self):
        return "<KeyedNode: {0}>".format(self.key)

    def __str__(self):
        return self.__repr__()


class KeyedTree:
    """
    Container of Keyed nodes, responsible for guaranteeing uniqueness.

    When using KeyedNodes as part of a KeyedTree, all updates to the
    tree should be made via the KeyedTree (and not via the KeyedNodes
    directly).
    """

    def __init__(self):
        self.nodes = {}

    def get_node(self, key):
        """
        Retrieve the node identified by key

        A node will always be returned. If it does not exist, NoSuchNode is
        thrown

        :param key: The key (or something equal to it) when creating the node
        :return: The node identified by key
        """
        if key not in self.nodes:
            raise NoSuchNode

        return self.nodes[key]

    def for_each_node(self, callback):
        """
        Trigger callback for each node in the tree. Callback order is undefined

        :param callback: The function to callback on:
            def callback(node: KeyedNode):
                pass
        """
        for node in self.nodes:
            callback(self.nodes[node])

    def add_pair(self, parent, child):
        """
        Create a parent/child relationship between the two specified nodes.

        If either node do not exist in the tree, new KeyedNodes are created
        to represent them. Since nodes may not have multiple parents, if child
        already exists in the tree, and already has a parent
        MultipleParentsNotSupported will be thrown.

        :param parent: A key object for a new or existing parent node
        :param child: A key object for a new or existing child node
        """
        if parent in self.nodes:
            p_node = self.nodes[parent]
        else:
            p_node = self.nodes[parent] = KeyedNode(parent)

        if child in self.nodes:
            c_node = self.nodes[child]
        else:
            c_node = self.nodes[child] = KeyedNode(child)

        c_node.set_parent(p_node)

    def get_path(self, source, dest):
        """
        Return the path of nodes that must be traversed to move from
        the source node to the destination node. It is assumed you
        can move in either direction (up to parents or down to
        children)

        The result will NOT include either source or dest.

        For example, given the following tree:
                     | - d <- h <- i
            a <- b <-| - c <- f
                     | - e <- g
        then get_path(g,i) => [e, b, d, h]

        If there is no path between source and dest, the tree is split
        and TreeIsSplit is thrown.

        :param source: The starting node
        :param dest:   The final node

        :return: A list of nodes that must be traversed
        """
        if source == dest:
            raise DuplicateNode
        if source not in self.nodes or dest not in self.nodes:
            raise NoSuchNode

        source_hist = self.nodes[source].get_ancestry()
        dest_hist = self.nodes[dest].get_ancestry()

        if len(source_hist) == 0 and len(dest_hist) == 0:
            raise TreeIsSplit

        if not source_hist and dest_hist[-1] != self.nodes[source]:
            raise TreeIsSplit

        if not dest_hist and source_hist[-1] != self.nodes[dest]:
            raise TreeIsSplit

        if not source_hist or not dest_hist:
            # parent / child
            pass
        elif source_hist[-1] != dest_hist[-1]:
            raise TreeIsSplit

        path = []

        found = False
        s_ancestor = None
        source_index = -1
        destination_index = -1

        while not found and source_index < (len(source_hist) - 1):
            source_index += 1
            s_ancestor = source_hist[source_index]
            found = (s_ancestor in dest_hist)

        if found:
            found = False
            while not found and destination_index < (len(dest_hist) - 1):
                destination_index += 1
                d_ancestor = dest_hist[destination_index]
                found = (d_ancestor == s_ancestor)

            path = source_hist[0:source_index]
            while destination_index >= 0:
                path.append(dest_hist[destination_index])
                destination_index -= 1

        return path
