import unittest
from src.dsa.merge_sort import merge_sort


class TestMergeSort(unittest.TestCase):

    def test_sorts_numbers(self):
        self.assertEqual(merge_sort([5, 2, 9, 1]), [1, 2, 5, 9])

    def test_empty_list(self):
        self.assertEqual(merge_sort([]), [])

    def test_single_item(self):
        self.assertEqual(merge_sort([7]), [7])

    def test_already_sorted(self):
        self.assertEqual(merge_sort([1, 2, 3, 4]), [1, 2, 3, 4])

    def test_reverse_order(self):
        self.assertEqual(merge_sort([4, 3, 2, 1]), [1, 2, 3, 4])

    def test_duplicates(self):
        self.assertEqual(merge_sort([3, 1, 3, 2, 1]), [1, 1, 2, 3, 3])

    def test_sorts_words(self):
        self.assertEqual(merge_sort(["Cara", "Ana", "Ben"]), ["Ana", "Ben", "Cara"])

    def test_original_list_is_not_changed(self):
        original = [3, 1, 2]
        merge_sort(original)
        self.assertEqual(original, [3, 1, 2])

    def test_sort_by_key(self):
        items = [("Oscilloscope", 3), ("Multimeter", 10), ("Caliper", 5)]
        result = merge_sort(items, key=lambda item: item[0])     # sort by name
        self.assertEqual(result[0][0], "Caliper")
        self.assertEqual(result[2][0], "Oscilloscope")

    def test_is_stable(self):
        records = [("B", 2), ("A", 2), ("C", 1), ("D", 2)]
        result = merge_sort(records, key=lambda r: r[1])         # sort by number only
        # B, A, D all have 2, so they must stay in their ORIGINAL order
        self.assertEqual(result, [("C", 1), ("B", 2), ("A", 2), ("D", 2)])

    def test_big_list_matches_python_sorted(self):
        numbers = []
        for i in range(5000):
            numbers.append((i * 7919) % 5003)     # a scrambled-looking list
        self.assertEqual(merge_sort(numbers), sorted(numbers))


if __name__ == "__main__":
    unittest.main()