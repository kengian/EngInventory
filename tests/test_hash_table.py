import unittest
from src.dsa.hash_table import HashTable


class TestHashTable(unittest.TestCase):

    def test_insert_and_get(self):
        h = HashTable()
        h.insert("E001", "Multimeter")
        self.assertEqual(h.get("E001"), "Multimeter")

    def test_contains(self):
        h = HashTable()
        h.insert("E001", "Multimeter")
        self.assertTrue(h.contains("E001"))
        self.assertFalse(h.contains("E999"))

    def test_insert_same_key_updates_value(self):
        h = HashTable()
        h.insert("E001", "Old")
        h.insert("E001", "New")
        self.assertEqual(h.get("E001"), "New")
        self.assertEqual(h.size(), 1)

    def test_delete_removes_key(self):
        h = HashTable()
        h.insert("E001", "Multimeter")
        h.delete("E001")
        self.assertFalse(h.contains("E001"))
        self.assertEqual(h.size(), 0)

    def test_get_missing_raises_error(self):
        h = HashTable()
        with self.assertRaises(KeyError):
            h.get("nope")

    def test_delete_missing_raises_error(self):
        h = HashTable()
        with self.assertRaises(KeyError):
            h.delete("nope")

    def test_many_keys_with_collisions_and_resize(self):
        h = HashTable(capacity=4)          # small on purpose, so collisions happen
        for i in range(200):
            h.insert("ID" + str(i), i)
        self.assertEqual(h.size(), 200)
        for i in range(200):               # every key can still be found
            self.assertEqual(h.get("ID" + str(i)), i)
        self.assertTrue(h.capacity > 4)    # the table grew

    def test_works_with_number_keys(self):
        h = HashTable()
        h.insert(42, "answer")
        self.assertEqual(h.get(42), "answer")

    def test_delete_one_keeps_others(self):
        h = HashTable(capacity=1)          # everything shares one box at first
        h.insert("A", 1)
        h.delete("A")
        h.insert("B", 2)
        self.assertEqual(h.get("B"), 2)
        self.assertFalse(h.contains("A"))


if __name__ == "__main__":
    unittest.main()