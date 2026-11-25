import unittest
from src.dsa.trie import Trie


class TestTrie(unittest.TestCase):

    def test_insert_and_contains(self):
        t = Trie()
        t.insert("Multimeter")
        self.assertTrue(t.contains("Multimeter"))
        self.assertFalse(t.contains("Multi"))      # a prefix is not a word

    def test_prefix_finds_all_matches_sorted(self):
        t = Trie()
        t.insert("Caliper")
        t.insert("Calculator")
        t.insert("Cable")
        t.insert("Oscilloscope")
        self.assertEqual(t.search_prefix("ca"), ["Cable", "Calculator", "Caliper"])

    def test_prefix_with_no_match(self):
        t = Trie()
        t.insert("Caliper")
        self.assertEqual(t.search_prefix("xyz"), [])

    def test_search_is_not_case_sensitive(self):
        t = Trie()
        t.insert("Multimeter")
        self.assertEqual(t.search_prefix("MULTI"), ["Multimeter"])
        self.assertTrue(t.contains("multimeter"))

    def test_duplicate_insert_returns_false(self):
        t = Trie()
        self.assertTrue(t.insert("Caliper"))
        self.assertFalse(t.insert("Caliper"))
        self.assertEqual(t.size(), 1)

    def test_empty_word_raises_error(self):
        t = Trie()
        with self.assertRaises(ValueError):
            t.insert("")
        with self.assertRaises(ValueError):
            t.insert("   ")

    def test_empty_prefix_returns_everything(self):
        t = Trie()
        t.insert("Caliper")
        t.insert("Anvil")
        self.assertEqual(t.search_prefix(""), ["Anvil", "Caliper"])

    def test_remove_word(self):
        t = Trie()
        t.insert("Caliper")
        self.assertTrue(t.remove("Caliper"))
        self.assertFalse(t.contains("Caliper"))
        self.assertEqual(t.size(), 0)

    def test_remove_keeps_longer_word(self):
        t = Trie()
        t.insert("car")
        t.insert("card")
        t.remove("car")
        self.assertFalse(t.contains("car"))
        self.assertTrue(t.contains("card"))
        self.assertEqual(t.search_prefix("car"), ["card"])

    def test_remove_keeps_shorter_word(self):
        t = Trie()
        t.insert("car")
        t.insert("card")
        t.remove("card")
        self.assertTrue(t.contains("car"))

    def test_remove_missing_returns_false(self):
        t = Trie()
        t.insert("Caliper")
        self.assertFalse(t.remove("Cal"))          # a prefix, not a word
        self.assertFalse(t.remove("Zebra"))

    def test_remove_cleans_up_unused_nodes(self):
        t = Trie()
        t.insert("abc")
        t.remove("abc")
        self.assertEqual(t.root.children, [])      # nothing left behind


if __name__ == "__main__":
    unittest.main()