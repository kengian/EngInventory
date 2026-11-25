# Item service (features F1, F3, F4)
# Connects: input validation + SQLite + image files + the DSA structures.
# Every change is saved to SQLite AND to the in-memory structures (write-through).
#
# Complexity table (n = number of items, m = number of results):
# add_item                   -> O(log n)
# get_item / by_serial       -> O(1) average     (Hash Table)
# list_items_by_name         -> O(n)             (AVL in-order)
# list_items_by_category     -> O(n log n)       (Merge Sort)
# search (name prefix)       -> O(log n + m)     (AVL range query)
# suggest_names              -> O(L + m log m)   (Trie)
# delete_item                -> O(log n)
# loading at start-up        -> O(n log n)
#
# NOTE: lists returned from here contain the real stored dictionaries.
# Read them, but do not change them.

import logging
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.db.db_manager import DatabaseManager
from src.dsa.avl_tree import AVLTree
from src.dsa.hash_table import HashTable
from src.dsa.merge_sort import merge_sort
from src.dsa.trie import Trie
from src.services.image_service import ImageService

logger = logging.getLogger("enginventory")

CONDITIONS = ["New", "Good", "Fair", "Poor"]
TEXT_FIELDS = [
    ("name", "Name"),
    ("category", "Category"),
    ("manufacturer", "Manufacturer"),
    ("model", "Model"),
    ("serial_no", "Serial No."),
    ("storage_location", "Storage location"),
]
MAX_TEXT_LENGTH = 100
MAX_QUANTITY = 9999
BIG_ID = 10 ** 12          # bigger than any item id (used in range searches)


def validate_item_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Check the form data. Returns a clean copy, or raises ValueError with
    a clear message for the user. O(1)"""
    clean: Dict[str, Any] = {}

    for field, label in TEXT_FIELDS:
        text = str(data.get(field, "")).strip()
        if text == "":
            raise ValueError(label + " is required")
        if len(text) > MAX_TEXT_LENGTH:
            raise ValueError(label + " must be at most 100 characters")
        clean[field] = text
    clean["serial_no"] = clean["serial_no"].upper()

    try:
        quantity = int(str(data.get("quantity", "")).strip())
    except ValueError:
        raise ValueError("Quantity must be a whole number")
    if quantity < 1 or quantity > MAX_QUANTITY:
        raise ValueError("Quantity must be between 1 and 9999")
    clean["quantity"] = quantity

    condition = str(data.get("item_condition", "")).strip()
    if condition not in CONDITIONS:
        raise ValueError("Condition must be one of: " + ", ".join(CONDITIONS))
    clean["item_condition"] = condition

    date_text = str(data.get("date_acquired", "")).strip()
    try:
        acquired = datetime.strptime(date_text, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Date acquired must look like YYYY-MM-DD (example: 2026-01-15)")
    if acquired > date.today():
        raise ValueError("Date acquired cannot be in the future")
    clean["date_acquired"] = acquired.isoformat()

    return clean


class ItemService:
    """All the item actions the screens need."""

    def __init__(self, db: DatabaseManager, images: ImageService) -> None:
        self.db = db
        self.images = images
        self.by_id = HashTable()          # item_id   -> item
        self.by_serial = HashTable()      # serial_no -> item_id
        self.sorted_items = AVLTree()     # (name in lowercase, item_id) -> item
        self.name_trie = Trie()           # item names, for autocomplete
        self._load_from_database()

    # ---------- changing data ----------

    def add_item(self, data: Dict[str, Any], image_path: Optional[Path] = None,
                 user: str = "admin") -> Dict[str, Any]:
        """Validate, save, and index a new item. Returns the saved item.
        Raises ValueError with a clear message if anything is wrong. O(log n)"""
        clean = validate_item_data(data)

        if self.by_serial.contains(clean["serial_no"]):
            raise ValueError("That serial number already exists")

        if image_path is not None:
            self.images.validate_image(Path(image_path))   # check BEFORE saving

        item_id = self.db.add_item(clean)

        if image_path is not None:
            try:
                file_name = self.images.save_image(item_id, Path(image_path))
                self.db.update_item_image(item_id, file_name)
            except Exception:
                self.db.delete_item(item_id)               # undo, keep things clean
                raise

        item = self.db.get_item(item_id)
        self._index(item)
        logger.info("ADD user=%s item_id=%s serial=%s", user, item_id, item["serial_no"])
        return item

    def delete_item(self, item_id: int, user: str = "admin") -> bool:
        """Delete an item and its picture. Returns False if it does not exist. O(log n)"""
        item = self.get_item(item_id)
        if item is None:
            return False

        self.db.delete_item(item_id)
        self.images.delete_image(item.get("image_file"))
        self._unindex(item)
        logger.info("DELETE user=%s item_id=%s", user, item_id)
        return True

    def replace_item_image(self, item_id: int, new_image_path: Path,
                           user: str = "admin") -> str:
        """Give an item a new picture and delete the old one. Returns the new
        file name. Raises ValueError if the item or picture is bad. O(1)"""
        item = self.get_item(item_id)
        if item is None:
            raise ValueError("Item not found")

        new_file = self.images.replace_image(item_id, item.get("image_file"),
                                             Path(new_image_path))
        self.db.update_item_image(item_id, new_file)
        item["image_file"] = new_file            # same dictionary used everywhere
        logger.info("REPLACE_IMAGE user=%s item_id=%s", user, item_id)
        return new_file

    # ---------- reading data ----------

    def get_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Find an item by its ID, or None. O(1) average (Hash Table)"""
        if self.by_id.contains(item_id):
            return self.by_id.get(item_id)
        return None

    def get_item_by_serial(self, serial_no: str) -> Optional[Dict[str, Any]]:
        """Find an item by serial number, or None. O(1) average (Hash Table)"""
        serial = str(serial_no).strip().upper()
        if self.by_serial.contains(serial):
            return self.get_item(self.by_serial.get(serial))
        return None

    def list_items_by_name(self) -> List[Dict[str, Any]]:
        """All items, A to Z by name. O(n) (AVL in-order walk)"""
        return [pair[1] for pair in self.sorted_items.in_order_traversal()]

    def list_items_by_category(self) -> List[Dict[str, Any]]:
        """All items, grouped by category, then name. O(n log n) (Merge Sort)"""
        return merge_sort(self.list_items_by_name(),
                          key=lambda item: (item["category"].lower(),
                                            item["name"].lower()))

    def search(self, prefix: str = "",
               category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Items whose name starts with prefix (not case sensitive), A to Z.
        category (optional) keeps only that category; "All" means no filter.
        O(log n + m) (AVL range query)"""
        text = prefix.strip().lower()
        if text == "":
            items = self.list_items_by_name()
        else:
            pairs = self.sorted_items.range_query((text, 0), (text + "\uffff", BIG_ID))
            items = [pair[1] for pair in pairs]

        if category and category.lower() != "all":
            filtered = []
            for item in items:
                if item["category"].lower() == category.lower():
                    filtered.append(item)
            items = filtered
        return items

    def suggest_names(self, prefix: str, limit: int = 8) -> List[str]:
        """Autocomplete suggestions for the search box. O(L + m log m) (Trie)"""
        return self.name_trie.search_prefix(prefix)[:limit]

    def list_categories(self) -> List[str]:
        """Every category once, A to Z. O(n log n)"""
        names = [item["category"] for item in self.list_items_by_name()]
        ordered = merge_sort(names, key=lambda c: c.lower())
        result: List[str] = []
        for name in ordered:
            if len(result) == 0 or result[-1].lower() != name.lower():
                result.append(name)
        return result

    def count(self) -> int:
        """How many items exist. O(1)"""
        return self.by_id.size()

    # ---------- keeping the DSA structures up to date ----------

    def _load_from_database(self) -> None:
        """Fill the structures from SQLite when the app starts. O(n log n)"""
        for item in self.db.get_all_items():
            self._index(item)

    def _index(self, item: Dict[str, Any]) -> None:
        """Put one item into every structure. O(log n)"""
        self.by_id.insert(item["item_id"], item)
        self.by_serial.insert(item["serial_no"], item["item_id"])
        self.sorted_items.insert((item["name"].lower(), item["item_id"]), item)
        self.name_trie.insert(item["name"])

    def _unindex(self, item: Dict[str, Any]) -> None:
        """Take one item out of every structure. O(log n)"""
        name_lower = item["name"].lower()
        self.by_id.delete(item["item_id"])
        self.by_serial.delete(item["serial_no"])
        self.sorted_items.delete((name_lower, item["item_id"]))

        # Only forget the name if no other item uses it
        same_name = self.sorted_items.range_query((name_lower, 0), (name_lower, BIG_ID))
        if len(same_name) == 0:
            self.name_trie.remove(item["name"])