import unittest
from src.dsa.linked_list import LinkedList


class TestLinkedList(unittest.TestCase):

    def test_new_list_is_empty(self):
        ll = LinkedList()
        self.assertTrue(ll.is_empty())
        self.assertEqual(ll.size(), 0)

    def test_insert_puts_newest_first(self):
        ll = LinkedList()
        ll.insert("A")
        ll.insert("B")
        ll.insert("C")
        self.assertEqual(ll.traverse(), ["C", "B", "A"])

    def test_contains_finds_value(self):
        ll = LinkedList()
        ll.insert("A")
        self.assertTrue(ll.contains("A"))
        self.assertFalse(ll.contains("Z"))

    def test_remove_first_item(self):
        ll = LinkedList()
        ll.insert("A")
        ll.insert("B")                 # list is B -> A
        self.assertTrue(ll.remove("B"))
        self.assertEqual(ll.traverse(), ["A"])

    def test_remove_middle_item(self):
        ll = LinkedList()
        ll.insert("A")
        ll.insert("B")
        ll.insert("C")                 # list is C -> B -> A
        self.assertTrue(ll.remove("B"))
        self.assertEqual(ll.traverse(), ["C", "A"])

    def test_remove_last_item(self):
        ll = LinkedList()
        ll.insert("A")
        ll.insert("B")                 # list is B -> A
        self.assertTrue(ll.remove("A"))
        self.assertEqual(ll.traverse(), ["B"])

    def test_remove_missing_returns_false(self):
        ll = LinkedList()
        ll.insert("A")
        self.assertFalse(ll.remove("Z"))
        self.assertEqual(ll.size(), 1)

    def test_remove_from_empty_returns_false(self):
        ll = LinkedList()
        self.assertFalse(ll.remove("A"))

    def test_size_changes(self):
        ll = LinkedList()
        ll.insert(1)
        ll.insert(2)
        self.assertEqual(ll.size(), 2)
        ll.remove(1)
        self.assertEqual(ll.size(), 1)

    def test_traverse_empty_list(self):
        ll = LinkedList()
        self.assertEqual(ll.traverse(), [])


if __name__ == "__main__":
    unittest.main()