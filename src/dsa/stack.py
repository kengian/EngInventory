# Stack (LIFO - Last In, First Out)
# Used in: Undo last return (F9)
#
# Complexity table:
# push     -> O(1)
# pop      -> O(1)
# peek     -> O(1)
# is_empty -> O(1)


class Stack:
    """A simple stack built on top of a Python list."""

    def __init__(self):
        self.items = []  # the list is just the storage box

    def push(self, item):
        """Put an item on top. O(1)"""
        self.items.append(item)

    def pop(self):
        """Remove and return the top item. O(1)"""
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack")
        return self.items.pop()

    def peek(self):
        """Look at the top item without removing it. O(1)"""
        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack")
        return self.items[-1]

    def is_empty(self):
        """Return True if the stack has nothing. O(1)"""
        return len(self.items) == 0

    def size(self):
        """How many items are in the stack. O(1)"""
        return len(self.items)