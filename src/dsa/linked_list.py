# Linked List (singly linked)
# Used in: Active loans record store (D7)
#
# Complexity table:
# insert (at front) -> O(1)
# remove            -> O(n)
# contains          -> O(n)
# traverse          -> O(n)
# is_empty / size   -> O(1)


class Node:
    """One box in the chain. Holds a value and points to the next box."""

    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    """A chain of nodes. We only keep track of the first one (the head)."""

    def __init__(self):
        self.head = None
        self.count = 0

    def insert(self, value):
        """Add a value at the front of the chain. O(1)"""
        new_node = Node(value)
        new_node.next = self.head   # new box points to the old first box
        self.head = new_node        # new box becomes the first box
        self.count += 1

    def remove(self, value):
        """Remove the first node holding this value.
        Returns True if removed, False if not found. O(n)"""
        if self.head is None:
            return False

        # Case 1: the value is in the first box
        if self.head.value == value:
            self.head = self.head.next
            self.count -= 1
            return True

        # Case 2: walk down the chain and look one box ahead
        current = self.head
        while current.next is not None:
            if current.next.value == value:
                current.next = current.next.next   # skip over that box
                self.count -= 1
                return True
            current = current.next
        return False

    def contains(self, value):
        """Return True if the value is in the chain. O(n)"""
        current = self.head
        while current is not None:
            if current.value == value:
                return True
            current = current.next
        return False

    def traverse(self):
        """Visit every box and return all values as a Python list. O(n)"""
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result

    def is_empty(self):
        """Return True if the chain has no boxes. O(1)"""
        return self.head is None

    def size(self):
        """How many boxes are in the chain. O(1)"""
        return self.count