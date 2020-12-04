from tools.tree import KeyedNode, KeyedTree
from tools.tree import MultipleParentsNotSupported, TreeHasLoop, NoSuchNode, DuplicateNode, TreeIsSplit
from unittest import TestCase

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
        self.assertIsNone(child.GetParent())


    def test_Parent_CanSet(self):
        parent = KeyedNode("parent")
        child = KeyedNode("child")
        child.SetParent(parent)

        self.assertEqual(child.GetParent(), parent)

    def test_Parent_NoSetSelf(self):
        child = KeyedNode("child")

        self.assertRaises(TreeHasLoop, lambda: child.SetParent(child))

    def test_Parent_NoDoubleSet(self):
        parent = KeyedNode("parent")
        child = KeyedNode("child")
        child.SetParent(parent)

        imposter = KeyedNode("imposter")
        self.assertRaises(MultipleParentsNotSupported, lambda : child.SetParent(imposter))

        self.assertEqual(child.GetParent(), parent)

    def test_Children_DefaultEmpty(self):
        child = KeyedNode("me")
        self.assertListEqual(child.GetChildNodes(), [])

    def test_Children_SingleChild(self):
        grandParent = KeyedNode("grand pa")
        parent = KeyedNode("pa")
        child = KeyedNode("me")
        child.SetParent(parent)
        parent.SetParent(grandParent)

        self.assertListEqual(child.GetChildNodes(), [])
        self.assertListEqual(parent.GetChildNodes(), [child])
        self.assertListEqual(grandParent.GetChildNodes(), [parent])

    def test_Children_MultipleChildren(self):
        grandParent = KeyedNode("grand pa")

        parent = KeyedNode("pa")
        aunt = KeyedNode("aunt")
        uncle = KeyedNode("uncle")

        me = KeyedNode("me")
        brother = KeyedNode("bro")
        sister = KeyedNode("si")

        me.SetParent(parent)
        brother.SetParent(parent)
        sister.SetParent(parent)

        parent.SetParent(grandParent)
        aunt.SetParent(grandParent)
        uncle.SetParent(grandParent)

        self.assertListEqual(me.GetChildNodes(), [])
        self.assertListEqual(parent.GetChildNodes(), [me, brother, sister])
        self.assertListEqual(grandParent.GetChildNodes(), [parent, aunt, uncle])

    def test_RootNode_NoLoops(self):
        grandParent = KeyedNode("grand pa")
        parent = KeyedNode("pa")
        child = KeyedNode("me")
        child.SetParent(parent)
        parent.SetParent(grandParent)

        self.assertEqual(child.GetRootNode(), grandParent)
        self.assertEqual(parent.GetRootNode(), grandParent)
        self.assertEqual(grandParent.GetRootNode(), grandParent)

    def test_RootNode_LoopException(self):
        grandParent = KeyedNode("grand pa")
        parent = KeyedNode("pa")
        child = KeyedNode("me")
        child.SetParent(parent)
        parent.SetParent(grandParent)
        grandParent.SetParent(child)

        self.assertRaises(TreeHasLoop, lambda: child.GetRootNode())
        self.assertRaises(TreeHasLoop, lambda: parent.GetRootNode())
        self.assertRaises(TreeHasLoop, lambda: grandParent.GetRootNode())

    def test_Ancestory_NoLoops(self):
        grandParent = KeyedNode("grand pa")
        parent = KeyedNode("pa")
        child = KeyedNode("me")
        child.SetParent(parent)
        parent.SetParent(grandParent)

        self.assertEqual(child.GetAncestory(), [parent, grandParent])
        self.assertEqual(parent.GetAncestory(), [grandParent])
        self.assertEqual(grandParent.GetAncestory(), [])

    def test_Depth_NoLoops(self):
        grandParent = KeyedNode("grand pa")
        parent = KeyedNode("pa")
        child = KeyedNode("me")
        child.SetParent(parent)
        parent.SetParent(grandParent)

        self.assertEqual(child.GetDepth(), 2)
        self.assertEqual(parent.GetDepth(), 1)
        self.assertEqual(grandParent.GetDepth(), 0)

    def test_Depth_LoopException(self):
        grandParent = KeyedNode("grand pa")
        parent = KeyedNode("pa")
        child = KeyedNode("me")
        child.SetParent(parent)
        parent.SetParent(grandParent)
        grandParent.SetParent(child)

        self.assertRaises(TreeHasLoop, lambda: child.GetDepth())
        self.assertRaises(TreeHasLoop, lambda: parent.GetDepth())
        self.assertRaises(TreeHasLoop, lambda: grandParent.GetDepth())

    def test_Ancestory_LoopException(self):
        grandParent = KeyedNode("grand pa")
        parent = KeyedNode("pa")
        child = KeyedNode("me")
        child.SetParent(parent)
        parent.SetParent(grandParent)
        grandParent.SetParent(child)

        self.assertRaises(TreeHasLoop, lambda: child.GetAncestory())
        self.assertRaises(TreeHasLoop, lambda: parent.GetAncestory())
        self.assertRaises(TreeHasLoop, lambda: grandParent.GetAncestory())

    def test_Children_MultipleChildren(self):
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
        cousin_aunt.SetParent(aunt)
        cousin_uncle = KeyedNode("cousin (uncle)")
        cousin_uncle.SetParent(uncle)

        me.SetParent(parent)
        brother.SetParent(parent)
        sister.SetParent(parent)

        parent.SetParent(grandParent)
        aunt.SetParent(grandParent)
        uncle.SetParent(grandParent)
        expected = {
            1: [parent, aunt, uncle],
            2: [me, brother, sister, cousin_aunt, cousin_uncle]
        }

        grandParent.Traverse(callback)
        self.assertDictEqual(calledBack, expected)

class Test_KeyedTree(TestCase):
    def test_GetMissingNode(self):
        tree = KeyedTree()
        missingNode = lambda: tree.GetNode("No Such Node")
        self.assertRaises(NoSuchNode, missingNode)

        tree.AddPair("parent", "child")
        self.assertRaises(NoSuchNode, missingNode)

    def test_GetAddedNodes(self):
        tree = KeyedTree()
        tree.AddPair("parent", "child")
        self.assertEqual(tree.GetNode("parent"), KeyedNode("parent"))
        self.assertEqual(tree.GetNode("child"), KeyedNode("child"))

        self.assertEqual(tree.GetNode("child").GetParent(), tree.GetNode("parent"))

    def test_ParentIsAlreadyKnown(self):
        tree = KeyedTree()
        tree.AddPair("parent", "child")
        tree.AddPair("parent", "brother")
        self.assertEqual(tree.GetNode("parent"), KeyedNode("parent"))
        self.assertEqual(tree.GetNode("child"), KeyedNode("child"))
        self.assertEqual(tree.GetNode("brother"), KeyedNode("brother"))
        self.assertListEqual(tree.GetNode("parent").GetChildNodes(), [KeyedNode("child"), KeyedNode("brother")])

    def test_ChildIsAlreadyKnown(self):
        tree = KeyedTree()
        tree.AddPair("parent", "child")
        tree.AddPair("grandparent", "parent")
        self.assertEqual(tree.GetNode("parent"), KeyedNode("parent"))
        self.assertEqual(tree.GetNode("grandparent"), KeyedNode("grandparent"))
        self.assertEqual(tree.GetNode("child"), KeyedNode("child"))
        self.assertListEqual(tree.GetNode("parent").GetChildNodes(), [KeyedNode("child")])
        self.assertEqual(tree.GetNode("parent").GetParent(), tree.GetNode("grandparent"))

    def test_ForEach_Empty(self):
        nodes = []
        tree = KeyedTree()
        tree.ForEachNode(lambda n: nodes.append(n))
        self.assertListEqual(nodes, [])

    def test_KeyList_Repeats(self):
        tree = KeyedTree()
        tree.AddPair("parent", "child")
        tree.AddPair("parent", "brother")
        tree.AddPair("parent", "sister")
        tree.AddPair("grandparent", "parent")


        expected = [KeyedNode(n) for n in ["parent", "child", "brother", "sister", "grandparent"]]
        nodes = []
        tree.ForEachNode(lambda n: nodes.append(n))
        self.assertListEqual(nodes, expected)

    def test_GetPath_NoSuchNode(self):
        tree = KeyedTree()
        tree.AddPair("parent", "child")
        self.assertRaises(NoSuchNode, lambda : tree.GetPath("parent", "xxx"))
        self.assertRaises(NoSuchNode, lambda : tree.GetPath("xxx", "child"))

    def test_GetPath_SameNode(self):
        tree = KeyedTree()
        tree.AddPair("parent", "child")
        self.assertRaises(DuplicateNode, lambda : tree.GetPath("parent", "parent"))

    def test_GetPath_ParentChild(self):
        tree = KeyedTree()
        tree.AddPair("parent", "child")
        self.assertListEqual(tree.GetPath("parent", "child"), [])
        self.assertListEqual(tree.GetPath("child", "parent"), [])

    def test_GetPath_Cousin(self):
        tree = KeyedTree()
        tree.AddPair("grandparent", "uncle")
        tree.AddPair("grandparent", "parent")
        tree.AddPair("uncle", "cousin")
        tree.AddPair("parent", "child")
        self.assertListEqual(tree.GetPath("cousin", "child"), [KeyedNode("uncle"), KeyedNode("grandparent"), KeyedNode("parent")])
        self.assertListEqual(tree.GetPath("child", "cousin"), [KeyedNode("parent"), KeyedNode("grandparent"), KeyedNode("uncle")])

    def test_GetPathUnrelated(self):
        tree = KeyedTree()
        tree.AddPair("uncle", "cousin")
        tree.AddPair("parent", "child")
        self.assertRaises(TreeIsSplit, lambda: tree.GetPath("child", "cousin"))
        self.assertRaises(TreeIsSplit, lambda: tree.GetPath("cousin", "child"))

    def test_GetPath_IsolatedNode(self):
        tree = KeyedTree()
        tree.AddPair("uncle", "cousin")
        tree.AddPair("parent", "child")
        self.assertRaises(TreeIsSplit, lambda: tree.GetPath("uncle", "child"))
        self.assertRaises(TreeIsSplit, lambda: tree.GetPath("child", "uncle"))
        self.assertRaises(TreeIsSplit, lambda: tree.GetPath("uncle", "parent"))
