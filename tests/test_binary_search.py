import unittest
from src.dsa.binary_search import binary_search


class TestBinarySearch(unittest.TestCase):

    def test_finds_item_in_the_middle(self):
        items = [10, 20, 30, 40, 50]
        self.assertEqual(binary_search(items, 30), 2)

    def test_finds_first_item(self):
        items = [10, 20, 30, 40, 50]
        self.assertEqual(binary_search(items, 10), 0)

    def test_finds_last_item(self):
        items = [10, 20, 30, 40, 50]
        self.assertEqual(binary_search(items, 50), 4)

    def test_missing_item_returns_minus_one(self):
        items = [10, 20, 30, 40, 50]
        self.assertEqual(binary_search(items, 35), -1)

    def test_target_smaller_than_everything(self):
        items = [10, 20, 30]
        self.assertEqual(binary_search(items, 1), -1)

    def test_target_bigger_than_everything(self):
        items = [10, 20, 30]
        self.assertEqual(binary_search(items, 99), -1)

    def test_empty_list(self):
        self.assertEqual(binary_search([], 5), -1)

    def test_single_item_found(self):
        self.assertEqual(binary_search([7], 7), 0)

    def test_single_item_not_found(self):
        self.assertEqual(binary_search([7], 8), -1)

    def test_works_with_words(self):
        names = ["Ana", "Ben", "Cara", "Dan"]
        self.assertEqual(binary_search(names, "Cara"), 2)

    def test_search_by_key(self):
        records = [("E001", "Caliper"), ("E002", "Multimeter"), ("E003", "Scope")]
        self.assertEqual(binary_search(records, "E002", key=lambda r: r[0]), 1)

    def test_finds_every_item_in_a_big_list(self):
        items = list(range(0, 5000, 2))       # 0, 2, 4, ... 4998
        for i in range(len(items)):
            self.assertEqual(binary_search(items, items[i]), i)
        self.assertEqual(binary_search(items, 4999), -1)   # odd numbers are missing


if __name__ == "__main__":
    unittest.main()