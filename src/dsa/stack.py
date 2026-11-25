# Stack (LIFO - Last In, First Out)
# Used in: Undo last return (F9)
#
# Complexity table:
# push     -> O(1)
# pop      -> O(1)
# peek     -> O(1)
# is_empty -> O(1)

from typing import Any, List


class Stack:
    """A simple stack built on top of a Python list."""

    def __init__(self) -> None:
        self.items: List[Any] = []  # the list is just the storage box

    def push(self, item: Any) -> None:
        """Put an item on top. O(1)"""
        self.items.append(item)

    def pop(self) -> Any:
        """Remove and return the top item. O(1)"""
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack")
        return self.items.pop()

    def peek(self) -> Any:
        """Look at the top item without removing it. O(1)"""
        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack")
        return self.items[-1]

    def is_empty(self) -> bool:
        """Return True if the stack has nothing. O(1)"""
        return len(self.items) == 0

    def size(self) -> int:
        """How many items are in the stack. O(1)"""
        return len(self.items)