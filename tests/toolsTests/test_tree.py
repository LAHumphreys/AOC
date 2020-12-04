from unittest import TestCase

from tools.tree import KeyedNode, KeyedTree
from tools.tree import MultipleParentsNotSupported, TreeHasLoop, NoSuchNode, DuplicateNode, TreeIsSplit


class Test_KeyedNode(TestCase):
    def test_EQ(self):
        self.assertEqual(KeyedNode("A"), KeyedNode("A"))
        self.assertNotEqual(KeyedNode("A"), KeyedNode("B"))
        self.assertNotEqual(KeyedNode("A"), KeyedNode("a"))

    def test_LT(self):
        self.assertLess(KeyedNode("A"), KeyedNode("B"))
        self.assertLess(KeyedNode("ABBA"), KeyedNode("BAN"))
        self.assertLess(KeyedNode("ABBA"), KeyedNode("ABBC"))

        self.assertFalse(KeyedNode("ABBC") < KeyedNode("ABBA"))

    def test_Str(self):
        self.assertEqual(str(KeyedNode("APPLE")), "<KeyedNode: APPLE>")

    def test_Parent_DefaultNone(self):
        child = KeyedNode("child")
        self.assertIsNone(child.get_parent())

    def test_Parent_CanSet(self):
        parent = KeyedNode("parent")
        child = KeyedNode("child")
        child.set_parent(parent)

        self.assertEqual(child.get_parent(), parent)

    def test_Parent_NoSetSelf(self):
        child = KeyedNode("child")

        self.assertRaises(TreeHasLoop, lambda: child.set_parent(child))

    def test_Parent_NoDoubleSet(self):
        parent = KeyedNode("parent")
        child = KeyedNode("child")
        child.set_parent(parent)

        imposter = KeyedNode("imposter")
        self.assertRaises(
            MultipleParentsNotSupported,
            lambda: child.set_parent(imposter))

        self.assertEqual(child.get_parent(), parent)

    def test_Children_DefaultEmpty(self):
        child = KeyedNode("me")
        self.assertListEqual(child.get_child_nodes(), [])

    def test_Children_SingleChild(self):
        grandParent = KeyedNode("grand pa")
        parent = KeyedNode("pa")
        child = KeyedNode("me")
        child.set_parent(parent)
        parent.set_parent(grandParent)

        self.assertListEqual(child.get_child_nodes(), [])
        self.assertListEqual(parent.get_child_nodes(), [child])
        self.assertListEqual(grandParent.get_child_nodes(), [parent])

    def test_Children_MultipleChildren(self):
        grandParent = KeyedNode("grand pa")

        parent = KeyedNode("pa")
        aunt = KeyedNode("aunt")
        uncle = KeyedNode("uncle")

        me = KeyedNode("me")
        brother = KeyedNode("bro")
        sister = KeyedNode("si")

        me.set_parent(parent)
        brother.set_parent(parent)
        sister.set_parent(parent)

        parent.set_parent(grandParent)
        aunt.set_parent(grandParent)
        uncle.set_parent(grandParent)

        self.assertListEqual(me.get_child_nodes(), [])
        self.assertListEqual(parent.get_child_nodes(), [me, brother, sister])
        self.assertListEqual(
            grandParent.get_child_nodes(), [
                parent, aunt, uncle])

    def test_RootNode_NoLoops(self):
        grandParent = KeyedNode("grand pa")
        parent = KeyedNode("pa")
        child = KeyedNode("me")
        child.set_parent(parent)
        parent.set_parent(grandParent)

        self.assertEqual(child.get_root_node(), grandParent)
        self.assertEqual(parent.get_root_node(), grandParent)
        self.assertEqual(grandParent.get_root_node(), grandParent)

    def test_RootNode_LoopException(self):
        grandParent = KeyedNode("grand pa")
        parent = KeyedNode("pa")
        child = KeyedNode("me")
        child.set_parent(parent)
        parent.set_parent(grandParent)
        grandParent.set_parent(child)

        self.assertRaises(TreeHasLoop, lambda: child.get_root_node())
        self.assertRaises(TreeHasLoop, lambda: parent.get_root_node())
        self.assertRaises(TreeHasLoop, lambda: grandParent.get_root_node())

    def test_Ancestory_NoLoops(self):
        grandParent = KeyedNode("grand pa")
        parent = KeyedNode("pa")
        child = KeyedNode("me")
        child.set_parent(parent)
        parent.set_parent(grandParent)

        self.assertEqual(child.get_ancestry(), [parent, grandParent])
        self.assertEqual(parent.get_ancestry(), [grandParent])
        self.assertEqual(grandParent.get_ancestry(), [])

    def test_Depth_NoLoops(self):
        grandParent = KeyedNode("grand pa")
        parent = KeyedNode("pa")
        child = KeyedNode("me")
        child.set_parent(parent)
        parent.set_parent(grandParent)

        self.assertEqual(child.get_depth(), 2)
        self.assertEqual(parent.get_depth(), 1)
        self.assertEqual(grandParent.get_depth(), 0)

    def test_Depth_LoopException(self):
        grandParent = KeyedNode("grand pa")
        parent = KeyedNode("pa")
        child = KeyedNode("me")
        child.set_parent(parent)
        parent.set_parent(grandParent)
        grandParent.set_parent(child)

        self.assertRaises(TreeHasLoop, lambda: child.get_depth())
        self.assertRaises(TreeHasLoop, lambda: parent.get_depth())
        self.assertRaises(TreeHasLoop, lambda: grandParent.get_depth())

    def test_Ancestory_LoopException(self):
        grandParent = KeyedNode("grand pa")
        parent = KeyedNode("pa")
        child = KeyedNode("me")
        child.set_parent(parent)
        parent.set_parent(grandParent)
        grandParent.set_parent(child)

        self.assertRaises(TreeHasLoop, lambda: child.get_ancestry())
        self.assertRaises(TreeHasLoop, lambda: parent.get_ancestry())
        self.assertRaises(TreeHasLoop, lambda: grandParent.get_ancestry())

    def test_Traverse_MultipleChildren(self):
        calledBack = {}

        def callback(depth, node):
            if depth not in calledBack:
                calledBack[depth] = []
            calledBack[depth].append(node)

        grandParent = KeyedNode("grand pa")

        parent = KeyedNode("pa")
        aunt = KeyedNode("aunt")
        uncle = KeyedNode("uncle")

        me = KeyedNode("me")
        brother = KeyedNode("bro")
        sister = KeyedNode("si")

        cousin_aunt = KeyedNode("cousin (aunt)")
        cousin_aunt.set_parent(aunt)
        cousin_uncle = KeyedNode("cousin (uncle)")
        cousin_uncle.set_parent(uncle)

        me.set_parent(parent)
        brother.set_parent(parent)
        sister.set_parent(parent)

        parent.set_parent(grandParent)
        aunt.set_parent(grandParent)
        uncle.set_parent(grandParent)
        expected = {
            1: [parent, aunt, uncle],
            2: [me, brother, sister, cousin_aunt, cousin_uncle]
        }

        grandParent.traverse(callback)
        self.assertDictEqual(calledBack, expected)


class Test_KeyedTree(TestCase):
    def test_GetMissingNode(self):
        tree = KeyedTree()

        def missingNode(): return tree.get_node("No Such Node")
        self.assertRaises(NoSuchNode, missingNode)

        tree.add_pair("parent", "child")
        self.assertRaises(NoSuchNode, missingNode)

    def test_GetAddedNodes(self):
        tree = KeyedTree()
        tree.add_pair("parent", "child")
        self.assertEqual(tree.get_node("parent"), KeyedNode("parent"))
        self.assertEqual(tree.get_node("child"), KeyedNode("child"))

        self.assertEqual(
            tree.get_node("child").get_parent(),
            tree.get_node("parent"))

    def test_ParentIsAlreadyKnown(self):
        tree = KeyedTree()
        tree.add_pair("parent", "child")
        tree.add_pair("parent", "brother")
        self.assertEqual(tree.get_node("parent"), KeyedNode("parent"))
        self.assertEqual(tree.get_node("child"), KeyedNode("child"))
        self.assertEqual(tree.get_node("brother"), KeyedNode("brother"))
        self.assertListEqual(
            tree.get_node("parent").get_child_nodes(), [
                KeyedNode("child"), KeyedNode("brother")])

    def test_ChildIsAlreadyKnown(self):
        tree = KeyedTree()
        tree.add_pair("parent", "child")
        tree.add_pair("grandparent", "parent")
        self.assertEqual(tree.get_node("parent"), KeyedNode("parent"))
        self.assertEqual(tree.get_node("grandparent"), KeyedNode("grandparent"))
        self.assertEqual(tree.get_node("child"), KeyedNode("child"))
        self.assertListEqual(
            tree.get_node("parent").get_child_nodes(), [
                KeyedNode("child")])
        self.assertEqual(
            tree.get_node("parent").get_parent(),
            tree.get_node("grandparent"))

    def test_ForEach_Empty(self):
        nodes = []
        tree = KeyedTree()
        tree.for_each_node(lambda n: nodes.append(n))
        self.assertListEqual(nodes, [])

    def test_KeyList_Repeats(self):
        tree = KeyedTree()
        tree.add_pair("parent", "child")
        tree.add_pair("parent", "brother")
        tree.add_pair("parent", "sister")
        tree.add_pair("grandparent", "parent")

        expected = [
            KeyedNode(n) for n in [
                "parent",
                "child",
                "brother",
                "sister",
                "grandparent"]]
        nodes = []
        tree.for_each_node(lambda n: nodes.append(n))
        self.assertListEqual(nodes, expected)

    def test_GetPath_NoSuchNode(self):
        tree = KeyedTree()
        tree.add_pair("parent", "child")
        self.assertRaises(NoSuchNode, lambda: tree.get_path("parent", "xxx"))
        self.assertRaises(NoSuchNode, lambda: tree.get_path("xxx", "child"))

    def test_GetPath_SameNode(self):
        tree = KeyedTree()
        tree.add_pair("parent", "child")
        self.assertRaises(
            DuplicateNode,
            lambda: tree.get_path(
                "parent",
                "parent"))

    def test_GetPath_ParentChild(self):
        tree = KeyedTree()
        tree.add_pair("parent", "child")
        self.assertListEqual(tree.get_path("parent", "child"), [])
        self.assertListEqual(tree.get_path("child", "parent"), [])

    def test_GetPath_Cousin(self):
        tree = KeyedTree()
        tree.add_pair("grandparent", "uncle")
        tree.add_pair("grandparent", "parent")
        tree.add_pair("uncle", "cousin")
        tree.add_pair("parent", "child")
        self.assertListEqual(tree.get_path("cousin", "child"), [KeyedNode(
            "uncle"), KeyedNode("grandparent"), KeyedNode("parent")])
        self.assertListEqual(tree.get_path("child", "cousin"), [KeyedNode(
            "parent"), KeyedNode("grandparent"), KeyedNode("uncle")])

    def test_GetPathUnrelated(self):
        tree = KeyedTree()
        tree.add_pair("uncle", "cousin")
        tree.add_pair("parent", "child")
        self.assertRaises(TreeIsSplit, lambda: tree.get_path("child", "cousin"))
        self.assertRaises(TreeIsSplit, lambda: tree.get_path("cousin", "child"))

    def test_GetPath_IsolatedNode(self):
        tree = KeyedTree()
        tree.add_pair("uncle", "cousin")
        tree.add_pair("parent", "child")
        self.assertRaises(TreeIsSplit, lambda: tree.get_path("uncle", "child"))
        self.assertRaises(TreeIsSplit, lambda: tree.get_path("child", "uncle"))
        self.assertRaises(TreeIsSplit, lambda: tree.get_path("uncle", "parent"))
