# AVL Tree (self-balancing binary search tree)
# Used in: Sorted browse listing and range queries (D2)
#
# Complexity table (n = number of items, m = number of results):
# insert             -> O(log n)
# delete             -> O(log n)
# get / contains     -> O(log n)
# in_order_traversal -> O(n)
# range_query        -> O(log n + m)
# rotations          -> O(1)
#
# AVL rule: for every node, |height(left) - height(right)| <= 1.
# After insert/delete we fix any broken node with rotations.

from typing import Any, List, Optional, Tuple


class AVLNode:
    """One box in the tree."""

    def __init__(self, key: Any, value: Any = None) -> None:
        self.key = key
        self.value = value
        self.left: Optional["AVLNode"] = None
        self.right: Optional["AVLNode"] = None
        self.height = 1            # a single box has height 1


class AVLTree:
    """A balanced tree that keeps keys sorted."""

    def __init__(self) -> None:
        self.root: Optional[AVLNode] = None
        self.count = 0

    # ---------- public operations ----------

    def insert(self, key: Any, value: Any = None) -> bool:
        """Add a key. If it already exists, replace its value.
        Returns True if a new key was added. O(log n)"""
        if self.contains(key):
            node = self._find(key)
            node.value = value
            return False
        self.root = self._insert(self.root, key, value)
        self.count += 1
        return True

    def delete(self, key: Any) -> None:
        """Remove a key. Raises KeyError if it is missing. O(log n)"""
        if not self.contains(key):
            raise KeyError(key)
        self.root = self._delete(self.root, key)
        self.count -= 1

    def get(self, key: Any) -> Any:
        """Return the value for a key. Raises KeyError if missing. O(log n)"""
        node = self._find(key)
        if node is None:
            raise KeyError(key)
        return node.value

    def contains(self, key: Any) -> bool:
        """Return True if the key is in the tree. O(log n)"""
        return self._find(key) is not None

    def in_order_traversal(self) -> List[Tuple[Any, Any]]:
        """Return all (key, value) pairs sorted by key. O(n)"""
        result: List[Tuple[Any, Any]] = []
        self._in_order(self.root, result)
        return result

    def range_query(self, low: Any, high: Any) -> List[Tuple[Any, Any]]:
        """Return (key, value) pairs with low <= key <= high, sorted. O(log n + m)"""
        result: List[Tuple[Any, Any]] = []
        self._range(self.root, low, high, result)
        return result

    def size(self) -> int:
        """How many keys are stored. O(1)"""
        return self.count

    def height(self) -> int:
        """Height of the whole tree (0 if empty). O(1)"""
        return self._height(self.root)

    def is_balanced(self) -> bool:
        """Check that every box follows the AVL rule. O(n)"""
        return self._check_balanced(self.root)

    # ---------- height and balance helpers ----------

    def _height(self, node: Optional[AVLNode]) -> int:
        """Height of a box (0 for nothing). O(1)"""
        if node is None:
            return 0
        return node.height

    def _update_height(self, node: AVLNode) -> None:
        """Recalculate a box's height from its children. O(1)"""
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node: Optional[AVLNode]) -> int:
        """Left height minus right height. O(1)"""
        if node is None:
            return 0
        return self._height(node.left) - self._height(node.right)

    # ---------- rotations ----------

    def _rotate_right(self, y: AVLNode) -> AVLNode:
        """Fix a left-heavy box. Returns the new top box. O(1)

              y                x
             / \\              / \\
            x   C    -->     A   y
           / \\                  / \\
          A   B                B   C
        """
        x = y.left
        y.left = x.right
        x.right = y
        self._update_height(y)      # y is lower now, so update it first
        self._update_height(x)
        return x

    def _rotate_left(self, x: AVLNode) -> AVLNode:
        """Fix a right-heavy box. Returns the new top box. O(1)

            x                    y
           / \\                  / \\
          A   y      -->       x   C
             / \\              / \\
            B   C            A   B
        """
        y = x.right
        x.right = y.left
        y.left = x
        self._update_height(x)
        self._update_height(y)
        return y

    def _rebalance(self, node: AVLNode) -> AVLNode:
        """Update the height, and rotate if the box is out of balance. O(1)"""
        self._update_height(node)
        balance = self._balance_factor(node)

        if balance > 1:                                   # too heavy on the left
            if self._balance_factor(node.left) < 0:       # Left-Right case
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)               # Left-Left case

        if balance < -1:                                  # too heavy on the right
            if self._balance_factor(node.right) > 0:      # Right-Left case
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)                # Right-Right case

        return node                                       # already fine

    # ---------- inner recursive helpers ----------

    def _insert(self, node: Optional[AVLNode], key: Any, value: Any) -> AVLNode:
        """Insert below this box and rebalance on the way back up. O(log n)"""
        if node is None:
            return AVLNode(key, value)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        else:
            node.right = self._insert(node.right, key, value)
        return self._rebalance(node)

    def _delete(self, node: Optional[AVLNode], key: Any) -> Optional[AVLNode]:
        """Delete below this box and rebalance on the way back up. O(log n)"""
        if node is None:
            return None

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Found the box to delete
            if node.left is None:          # zero children, or only a right child
                return node.right
            if node.right is None:         # only a left child
                return node.left

            # Two children: copy the next bigger key here, then delete that one
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.key = successor.key
            node.value = successor.value
            node.right = self._delete(node.right, successor.key)

        return self._rebalance(node)

    def _find(self, key: Any) -> Optional[AVLNode]:
        """Walk down the tree looking for a key. O(log n)"""
        node = self.root
        while node is not None:
            if key == node.key:
                return node
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    def _in_order(self, node: Optional[AVLNode], result: List[Tuple[Any, Any]]) -> None:
        """Left, then this box, then right. O(n)"""
        if node is None:
            return
        self._in_order(node.left, result)
        result.append((node.key, node.value))
        self._in_order(node.right, result)

    def _range(self, node: Optional[AVLNode], low: Any, high: Any,
               result: List[Tuple[Any, Any]]) -> None:
        """Collect keys between low and high, skipping parts that can't match."""
        if node is None:
            return
        if low < node.key:                 # smaller keys might still be in range
            self._range(node.left, low, high, result)
        if low <= node.key <= high:
            result.append((node.key, node.value))
        if node.key < high:                # bigger keys might still be in range
            self._range(node.right, low, high, result)

    def _check_balanced(self, node: Optional[AVLNode]) -> bool:
        """True if this box and everything below it follows the AVL rule."""
        if node is None:
            return True
        if abs(self._balance_factor(node)) > 1:
            return False
        return self._check_balanced(node.left) and self._check_balanced(node.right)