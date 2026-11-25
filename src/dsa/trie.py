# Trie (prefix tree)
# Used in: Prefix autocomplete in the search box (D3)
#
# Complexity table (L = length of the word, m = number of matches):
# insert        -> O(L)
# contains      -> O(L)
# search_prefix -> O(L + m log m)   (the m log m is sorting the matches)
# remove        -> O(L)
#
# Children of a node are kept in a small list (no dict, as the project requires).
# Search is not case sensitive: "CAL" finds "Caliper".

from typing import List, Optional

from src.dsa.merge_sort import merge_sort


class TrieNode:
    """One letter in the tree."""

    def __init__(self, char: str = "") -> None:
        self.char = char
        self.children: List["TrieNode"] = []
        self.word: Optional[str] = None    # the full word, if a word ends here

    def find_child(self, char: str) -> Optional["TrieNode"]:
        """Return the child with this letter, or None. O(alphabet size)"""
        for child in self.children:
            if child.char == char:
                return child
        return None


class Trie:
    """A prefix tree for words like item names."""

    def __init__(self) -> None:
        self.root = TrieNode()
        self.count = 0

    def insert(self, word: str) -> bool:
        """Add a word. Returns True if new, False if it was already there. O(L)"""
        if not isinstance(word, str) or word.strip() == "":
            raise ValueError("Word cannot be empty")

        word = word.strip()
        node = self.root
        for letter in word.lower():
            child = node.find_child(letter)
            if child is None:
                child = TrieNode(letter)
                node.children.append(child)
            node = child

        if node.word is not None:      # already stored
            return False
        node.word = word
        self.count += 1
        return True

    def contains(self, word: str) -> bool:
        """Return True if this exact word is stored. O(L)"""
        node = self._find_node(word.strip().lower())
        return node is not None and node.word is not None

    def search_prefix(self, prefix: str) -> List[str]:
        """Return all words starting with prefix, sorted A to Z. O(L + m log m)"""
        node = self._find_node(prefix.strip().lower())
        if node is None:
            return []
        results: List[str] = []
        self._collect(node, results)
        return merge_sort(results, key=lambda w: w.lower())

    def remove(self, word: str) -> bool:
        """Remove a word. Returns True if removed, False if not found. O(L)"""
        text = word.strip().lower()

        # Walk down and remember every node on the way
        path = [self.root]
        node = self.root
        for letter in text:
            child = node.find_child(letter)
            if child is None:
                return False
            path.append(child)
            node = child

        if node.word is None:          # the path exists, but it is not a word
            return False

        node.word = None
        self.count -= 1

        # Walk back up and delete nodes that are no longer needed
        for i in range(len(text), 0, -1):
            current = path[i]
            if current.word is not None or len(current.children) > 0:
                break                  # still needed by another word
            path[i - 1].children.remove(current)
        return True

    def size(self) -> int:
        """How many words are stored. O(1)"""
        return self.count

    def _find_node(self, text: str) -> Optional[TrieNode]:
        """Walk down the letters. Returns the last node, or None. O(L)"""
        node = self.root
        for letter in text:
            child = node.find_child(letter)
            if child is None:
                return None
            node = child
        return node

    def _collect(self, node: TrieNode, results: List[str]) -> None:
        """Gather every word at or below this node. O(nodes below)"""
        if node.word is not None:
            results.append(node.word)
        for child in node.children:
            self._collect(child, results)