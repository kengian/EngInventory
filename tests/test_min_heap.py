import unittest
from src.dsa.min_heap import MinHeap


class TestMinHeap(unittest.TestCase):

    def test_new_heap_is_empty(self):
        h = MinHeap()
        self.assertTrue(h.is_empty())
        self.assertEqual(h.size(), 0)

    def test_extract_gives_smallest_first(self):
        h = MinHeap()
        h.insert(5)
        h.insert(2)
        h.insert(9)
        h.insert(1)
        self.assertEqual(h.extract_min(), 1)
        self.assertEqual(h.extract_min(), 2)
        self.assertEqual(h.extract_min(), 5)
        self.assertEqual(h.extract_min(), 9)

    def test_peek_does_not_remove(self):
        h = MinHeap()
        h.insert(7)
        h.insert(3)
        self.assertEqual(h.peek_min(), 3)
        self.assertEqual(h.size(), 2)

    def test_extract_empty_raises_error(self):
        h = MinHeap()
        with self.assertRaises(IndexError):
            h.extract_min()

    def test_peek_empty_raises_error(self):
        h = MinHeap()
        with self.assertRaises(IndexError):
            h.peek_min()

    def test_heapify_builds_valid_heap(self):
        h = MinHeap()
        h.heapify([5, 3, 8, 1, 9, 2])
        result = []
        while not h.is_empty():
            result.append(h.extract_min())
        self.assertEqual(result, [1, 2, 3, 5, 8, 9])

    def test_works_with_due_dates(self):
        h = MinHeap()
        h.insert(("2026-11-20", "Loan C"))
        h.insert(("2026-11-10", "Loan A"))
        h.insert(("2026-11-15", "Loan B"))
        self.assertEqual(h.extract_min(), ("2026-11-10", "Loan A"))   # most overdue first
        self.assertEqual(h.extract_min(), ("2026-11-15", "Loan B"))

    def test_duplicates_are_kept(self):
        h = MinHeap()
        h.insert(4)
        h.insert(4)
        self.assertEqual(h.size(), 2)
        self.assertEqual(h.extract_min(), 4)
        self.assertEqual(h.extract_min(), 4)

    def test_many_numbers_come_out_sorted(self):
        numbers = [50, 3, 77, 21, 8, 99, 1, 35, 62, 14, 44, 6]
        h = MinHeap()
        for n in numbers:
            h.insert(n)
        result = []
        while not h.is_empty():
            result.append(h.extract_min())
        self.assertEqual(result, sorted(numbers))


if __name__ == "__main__":
    unittest.main()