import unittest
from src.dsa.stack import Stack


class TestStack(unittest.TestCase):

    def test_new_stack_is_empty(self):
        s = Stack()
        self.assertTrue(s.is_empty())

    def test_push_makes_it_not_empty(self):
        s = Stack()
        s.push(1)
        self.assertFalse(s.is_empty())

    def test_pop_returns_last_item(self):
        s = Stack()
        s.push("a")
        s.push("b")
        self.assertEqual(s.pop(), "b")   # last in, first out
        self.assertEqual(s.pop(), "a")

    def test_peek_does_not_remove(self):
        s = Stack()
        s.push(10)
        self.assertEqual(s.peek(), 10)
        self.assertEqual(s.size(), 1)

    def test_pop_empty_raises_error(self):
        s = Stack()
        with self.assertRaises(IndexError):
            s.pop()

    def test_peek_empty_raises_error(self):
        s = Stack()
        with self.assertRaises(IndexError):
            s.peek()


if __name__ == "__main__":
    unittest.main()