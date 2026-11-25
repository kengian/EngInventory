import unittest
from src.dsa.avl_tree import AVLTree


class TestAVLTree(unittest.TestCase):

    def test_insert_and_get(self):
        t = AVLTree()
        t.insert(5, "five")
        self.assertEqual(t.get(5), "five")
        self.assertTrue(t.contains(5))
        self.assertFalse(t.contains(6))

    def test_in_order_is_sorted(self):
        t = AVLTree()
        for k in [50, 20, 70, 10, 30, 60, 80]:
            t.insert(k)
        keys = [pair[0] for pair in t.in_order_traversal()]
        self.assertEqual(keys, [10, 20, 30, 50, 60, 70, 80])

    def test_duplicate_key_updates_value(self):
        t = AVLTree()
        self.assertTrue(t.insert(1, "old"))
        self.assertFalse(t.insert(1, "new"))
        self.assertEqual(t.get(1), "new")
        self.assertEqual(t.size(), 1)

    def test_get_missing_raises_error(self):
        t = AVLTree()
        with self.assertRaises(KeyError):
            t.get(99)

    def test_delete_missing_raises_error(self):
        t = AVLTree()
        with self.assertRaises(KeyError):
            t.delete(99)

    # ----- the four rotation cases: each ends with 20 on top -----

    def test_left_left_rotation(self):
        t = AVLTree()
        for k in [30, 20, 10]:
            t.insert(k)
        self.assertEqual(t.root.key, 20)
        self.assertEqual(t.root.left.key, 10)
        self.assertEqual(t.root.right.key, 30)

    def test_right_right_rotation(self):
        t = AVLTree()
        for k in [10, 20, 30]:
            t.insert(k)
        self.assertEqual(t.root.key, 20)
        self.assertEqual(t.root.left.key, 10)
        self.assertEqual(t.root.right.key, 30)

    def test_left_right_rotation(self):
        t = AVLTree()
        for k in [30, 10, 20]:
            t.insert(k)
        self.assertEqual(t.root.key, 20)
        self.assertEqual(t.root.left.key, 10)
        self.assertEqual(t.root.right.key, 30)

    def test_right_left_rotation(self):
        t = AVLTree()
        for k in [10, 30, 20]:
            t.insert(k)
        self.assertEqual(t.root.key, 20)
        self.assertEqual(t.root.left.key, 10)
        self.assertEqual(t.root.right.key, 30)

    # ----- delete cases -----

    def test_delete_leaf(self):
        t = AVLTree()
        for k in [20, 10, 30]:
            t.insert(k)
        t.delete(10)
        self.assertFalse(t.contains(10))
        self.assertEqual(t.size(), 2)

    def test_delete_node_with_one_child(self):
        t = AVLTree()
        for k in [20, 10, 30, 5]:
            t.insert(k)
        t.delete(10)                         # 10 has only the child 5
        keys = [pair[0] for pair in t.in_order_traversal()]
        self.assertEqual(keys, [5, 20, 30])
        self.assertTrue(t.is_balanced())

    def test_delete_node_with_two_children(self):
        t = AVLTree()
        for k in [50, 30, 70, 20, 40, 60, 80]:
            t.insert(k)
        t.delete(50)                         # the root has two children
        keys = [pair[0] for pair in t.in_order_traversal()]
        self.assertEqual(keys, [20, 30, 40, 60, 70, 80])
        self.assertTrue(t.is_balanced())

    def test_delete_causes_rotation(self):
        t = AVLTree()
        for k in [20, 10, 30, 25, 40]:
            t.insert(k)
        t.delete(10)                         # right side becomes too heavy
        self.assertTrue(t.is_balanced())
        keys = [pair[0] for pair in t.in_order_traversal()]
        self.assertEqual(keys, [20, 25, 30, 40])

    # ----- range query -----

    def test_range_query(self):
        t = AVLTree()
        for k in [10, 20, 30, 40, 50, 60]:
            t.insert(k, "item" + str(k))
        result = t.range_query(25, 50)
        self.assertEqual([pair[0] for pair in result], [30, 40, 50])

    def test_range_query_with_no_matches(self):
        t = AVLTree()
        for k in [10, 20, 30]:
            t.insert(k)
        self.assertEqual(t.range_query(100, 200), [])

    def test_empty_tree(self):
        t = AVLTree()
        self.assertEqual(t.in_order_traversal(), [])
        self.assertEqual(t.height(), 0)
        self.assertTrue(t.is_balanced())

    # ----- the big test: sorted input must NOT make a straight line -----

    def test_sorted_input_stays_balanced(self):
        t = AVLTree()
        for k in range(1, 1001):             # 1, 2, 3, ... 1000 in order
            t.insert(k)
        self.assertEqual(t.size(), 1000)
        self.assertTrue(t.is_balanced())
        self.assertTrue(t.height() <= 14)    # a plain BST would have height 1000

    def test_stays_balanced_after_many_deletes(self):
        t = AVLTree()
        for k in range(1, 501):
            t.insert(k)
        for k in range(1, 501, 2):           # delete every odd number
            t.delete(k)
        self.assertEqual(t.size(), 250)
        self.assertTrue(t.is_balanced())
        keys = [pair[0] for pair in t.in_order_traversal()]
        self.assertEqual(keys, list(range(2, 501, 2)))


if __name__ == "__main__":
    unittest.main()