# Merge Sort (stable)
# Used in: Sorting report exports (D8)
#
# Complexity table:
# merge_sort -> O(n log n) time in best, average and worst case
#               O(n) extra space
# Stable: equal items keep their original order.

from typing import Any, Callable, List, Optional


def _identity(value: Any) -> Any:
    """Return the value unchanged. Used when no key is given. O(1)"""
    return value


def merge_sort(items: List[Any],
               key: Optional[Callable[[Any], Any]] = None) -> List[Any]:
    """Return a NEW sorted list (smallest first). The original is not changed.
    key (optional) says what to sort by, e.g. the item's name. O(n log n)"""
    if key is None:
        key = _identity

    if len(items) <= 1:                 # 0 or 1 items are already sorted
        return list(items)

    middle = len(items) // 2
    left = merge_sort(items[:middle], key)     # sort the left half
    right = merge_sort(items[middle:], key)    # sort the right half
    return _merge(left, right, key)


def _merge(left: List[Any], right: List[Any],
           key: Callable[[Any], Any]) -> List[Any]:
    """Join two sorted lists into one sorted list. O(n)"""
    result = []
    i = 0    # position in the left list
    j = 0    # position in the right list

    while i < len(left) and j < len(right):
        # "<=" takes from the LEFT when equal, which keeps the sort stable
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    while i < len(left):                # leftovers from the left list
        result.append(left[i])
        i += 1
    while j < len(right):               # leftovers from the right list
        result.append(right[j])
        j += 1

    return result