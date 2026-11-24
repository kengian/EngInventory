import unittest
from src.dsa.my_queue import Queue


class TestQueue(unittest.TestCase):

    def test_new_queue_is_empty(self):
        q = Queue()
        self.assertTrue(q.is_empty())

    def test_enqueue_makes_it_not_empty(self):
        q = Queue()
        q.enqueue("Ana")
        self.assertFalse(q.is_empty())

    def test_first_in_first_out(self):
        q = Queue()
        q.enqueue("Ana")
        q.enqueue("Ben")
        q.enqueue("Cara")
        self.assertEqual(q.dequeue(), "Ana")
        self.assertEqual(q.dequeue(), "Ben")
        self.assertEqual(q.dequeue(), "Cara")

    def test_front_does_not_remove(self):
        q = Queue()
        q.enqueue("Ana")
        self.assertEqual(q.front(), "Ana")
        self.assertEqual(q.size(), 1)

    def test_size_goes_up_and_down(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        self.assertEqual(q.size(), 2)
        q.dequeue()
        self.assertEqual(q.size(), 1)

    def test_dequeue_empty_raises_error(self):
        q = Queue()
        with self.assertRaises(IndexError):
            q.dequeue()

    def test_front_empty_raises_error(self):
        q = Queue()
        with self.assertRaises(IndexError):
            q.front()

    def test_can_reuse_after_emptying(self):
        q = Queue()
        q.enqueue("Ana")
        q.dequeue()
        q.enqueue("Ben")           # the line works again after being empty
        self.assertEqual(q.front(), "Ben")


if __name__ == "__main__":
    unittest.main()