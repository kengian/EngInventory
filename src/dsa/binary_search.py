# Binary Search
# Used in: Fast lookup inside any sorted array (D9)
#
# Complexity table:
# binary_search -> O(log n) time, O(1) extra space
#
# IMPORTANT: the list must already be sorted (smallest to largest).

from typing import Any, Callable, List, Optional


def _identity(value: Any) -> Any:
    """Return the value unchanged. Used when no key is given. O(1)"""
    return value


def binary_search(items: List[Any], target: Any,
                  key: Optional[Callable[[Any], Any]] = None) -> int:
    """Find target in a sorted list.
    key (optional) says what part of each item to compare, e.g. its ID.
    Returns the index if found, or -1 if not found. O(log n)"""
    if key is None:
        key = _identity

    low = 0
    high = len(items) - 1

    while low <= high:
        middle = (low + high) // 2
        middle_value = key(items[middle])

        if middle_value == target:
            return middle
        elif middle_value < target:
            low = middle + 1
        else:
            high = middle - 1

    return -1