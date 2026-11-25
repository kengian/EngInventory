# Min-Heap (smallest value is always on top)
# Used in: Overdue dashboard, earliest due date first (D6)
#
# Complexity table:
# insert      -> O(log n)
# extract_min -> O(log n)
# peek_min    -> O(1)
# heapify     -> O(n)
# is_empty    -> O(1)
#
# The heap is a tree stored in a list:
#   parent of i      = (i - 1) // 2
#   left child of i  = 2 * i + 1
#   right child of i = 2 * i + 2


class MinHeap:
    """A min-heap stored in a Python list."""

    def __init__(self):
        self.items = []

    def insert(self, value):
        """Add a value, then move it up to its correct place. O(log n)"""
        self.items.append(value)
        self._bubble_up(len(self.items) - 1)

    def extract_min(self):
        """Remove and return the smallest value. O(log n)"""
        if self.is_empty():
            raise IndexError("Cannot extract from an empty heap")
        smallest = self.items[0]
        last = self.items.pop()          # take the last value out
        if self.items:                   # if anything is left...
            self.items[0] = last         # ...put the last value on top
            self._bubble_down(0)         # ...and move it down
        return smallest

    def peek_min(self):
        """Look at the smallest value without removing it. O(1)"""
        if self.is_empty():
            raise IndexError("Heap is empty")
        return self.items[0]

    def heapify(self, values):
        """Turn a messy list into a valid heap. O(n)"""
        self.items = list(values)
        last_parent = len(self.items) // 2 - 1
        for i in range(last_parent, -1, -1):   # go backwards from the last parent
            self._bubble_down(i)

    def is_empty(self):
        """Return True if the heap has nothing. O(1)"""
        return len(self.items) == 0

    def size(self):
        """How many values are in the heap. O(1)"""
        return len(self.items)

    def _bubble_up(self, index):
        """Swap a value up while it is smaller than its parent. O(log n)"""
        while index > 0:
            parent = (index - 1) // 2
            if self.items[index] < self.items[parent]:
                self.items[index], self.items[parent] = self.items[parent], self.items[index]
                index = parent
            else:
                break

    def _bubble_down(self, index):
        """Swap a value down while a child is smaller. O(log n)"""
        n = len(self.items)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if left < n and self.items[left] < self.items[smallest]:
                smallest = left
            if right < n and self.items[right] < self.items[smallest]:
                smallest = right

            if smallest == index:        # already in the right place
                break

            self.items[index], self.items[smallest] = self.items[smallest], self.items[index]
            index = smallest