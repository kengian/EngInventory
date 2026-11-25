# Hash Table (separate chaining)
# Used in: Item lookup by Item ID / serial number (D1)
#
# Complexity table:
# insert   -> O(1) average, O(n) worst case
# get      -> O(1) average, O(n) worst case
# delete   -> O(1) average, O(n) worst case
# contains -> O(1) average, O(n) worst case
# resize   -> O(n), but rare
#
# Note: the worst case happens only if every key lands in the same box.


class HashTable:
    """A hash table. Each box (bucket) holds a small list of [key, value] pairs."""

    def __init__(self, capacity=16):
        self.capacity = capacity
        self.count = 0
        self.buckets = self._make_buckets(capacity)

    def _make_buckets(self, capacity):
        """Make a list of empty boxes. O(capacity)"""
        buckets = []
        for _ in range(capacity):
            buckets.append([])
        return buckets

    def _index_for(self, key):
        """Turn a key into a box number. O(length of key)"""
        text = str(key)
        total = 0
        for letter in text:
            total = (total * 31 + ord(letter)) % 1000000007
        return total % self.capacity

    def insert(self, key, value):
        """Add a key and value. If the key exists, replace its value. O(1) average"""
        box = self.buckets[self._index_for(key)]

        # If the key is already there, just update it
        for pair in box:
            if pair[0] == key:
                pair[1] = value
                return

        # Otherwise add a new pair to this box
        box.append([key, value])
        self.count += 1

        # If the table is too crowded, make more boxes
        if self.count / self.capacity > 0.75:
            self._resize()

    def get(self, key):
        """Return the value for a key. Raises KeyError if missing. O(1) average"""
        box = self.buckets[self._index_for(key)]
        for pair in box:
            if pair[0] == key:
                return pair[1]
        raise KeyError(key)

    def delete(self, key):
        """Remove a key. Raises KeyError if missing. O(1) average"""
        box = self.buckets[self._index_for(key)]
        for i in range(len(box)):
            if box[i][0] == key:
                box.pop(i)
                self.count -= 1
                return
        raise KeyError(key)

    def contains(self, key):
        """Return True if the key is in the table. O(1) average"""
        box = self.buckets[self._index_for(key)]
        for pair in box:
            if pair[0] == key:
                return True
        return False

    def size(self):
        """How many keys are stored. O(1)"""
        return self.count

    def _resize(self):
        """Double the number of boxes and move every pair to its new box. O(n)"""
        old_buckets = self.buckets
        self.capacity = self.capacity * 2
        self.buckets = self._make_buckets(self.capacity)
        self.count = 0
        for box in old_buckets:
            for pair in box:
                self.insert(pair[0], pair[1])