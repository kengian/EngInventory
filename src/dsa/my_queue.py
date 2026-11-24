# Queue (FIFO - First In, First Out)
# Used in: Waitlist per item (F6)
#
# Complexity table:
# enqueue  -> O(1)
# dequeue  -> O(1)
# front    -> O(1)
# is_empty -> O(1)


class Node:
    """One box in the line. Holds a value and points to the next box."""

    def __init__(self, value):
        self.value = value
        self.next = None


class Queue:
    """A queue made from linked nodes."""

    def __init__(self):
        self.head = None   # the front of the line
        self.tail = None   # the back of the line
        self.count = 0

    def enqueue(self, value):
        """Add a person at the back of the line. O(1)"""
        new_node = Node(value)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.count += 1

    def dequeue(self):
        """Remove and return the person at the front. O(1)"""
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue")
        value = self.head.value
        self.head = self.head.next
        if self.head is None:      # the line is now empty
            self.tail = None
        self.count -= 1
        return value

    def front(self):
        """Look at the first person without removing them. O(1)"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.head.value

    def is_empty(self):
        """Return True if nobody is in line. O(1)"""
        return self.head is None

    def size(self):
        """How many people are in line. O(1)"""
        return self.count