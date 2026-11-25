# Database manager (SQLite)
# Used in: saving items permanently (write-through, PDF guideline 4)
#
# Complexity table (n = number of items):
# initialize     -> O(1)
# add_item       -> O(log n)   (SQLite keeps an index on serial_no)
# get_item       -> O(log n)   (lookup by primary key)
# get_all_items  -> O(n)
# delete_item    -> O(log n)
# count_items    -> O(1)

import logging
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("enginventory")

SCHEMA_PATH = Path(__file__).parent / "schema.sql"


class DatabaseManager:
    """Talks to the SQLite file. Every change is saved right away."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row        # lets us read columns by name
        self.conn.execute("PRAGMA foreign_keys = ON")

    def initialize(self) -> None:
        """Create the tables if they don't exist yet. Safe to run twice. O(1)"""
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        self.conn.executescript(schema)
        self.conn.commit()

    def add_item(self, item: Dict[str, Any]) -> int:
        """Save a new item and return its new item_id.
        Raises ValueError for a duplicate serial number or bad data. O(log n)"""
        try:
            # "with self.conn" saves (commits) if all is well, or undoes on error
            with self.conn:
                cursor = self.conn.execute(
                    "INSERT INTO items (name, category, manufacturer, model, "
                    "serial_no, quantity, available, item_condition, "
                    "storage_location, date_acquired, image_file) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (item["name"], item["category"], item["manufacturer"],
                     item["model"], item["serial_no"], item["quantity"],
                     item["quantity"],                  # available = quantity at first
                     item["item_condition"], item["storage_location"],
                     item["date_acquired"], item.get("image_file")))
        except sqlite3.IntegrityError as error:
            if "serial_no" in str(error):
                raise ValueError("That serial number already exists")
            raise ValueError("Invalid item data")

        item_id = cursor.lastrowid
        logger.info("ADD_ITEM id=%s name=%s", item_id, item["name"])
        return item_id

    def get_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Return one item as a dictionary, or None if missing. O(log n)"""
        row = self.conn.execute(
            "SELECT * FROM items WHERE item_id = ?", (item_id,)).fetchone()
        if row is None:
            return None
        return dict(row)

    def get_all_items(self) -> List[Dict[str, Any]]:
        """Return every item, oldest first. O(n)"""
        rows = self.conn.execute(
            "SELECT * FROM items ORDER BY item_id").fetchall()
        return [dict(row) for row in rows]

    def update_item_image(self, item_id: int, image_file: Optional[str]) -> None:
        """Save the photo's file name for an item. O(log n)"""
        with self.conn:
            self.conn.execute(
                "UPDATE items SET image_file = ? WHERE item_id = ?",
                (image_file, item_id))
        logger.info("UPDATE_IMAGE id=%s file=%s", item_id, image_file)

    def delete_item(self, item_id: int) -> bool:
        """Delete an item. Returns True if it existed. O(log n)"""
        with self.conn:
            cursor = self.conn.execute(
                "DELETE FROM items WHERE item_id = ?", (item_id,))
        deleted = cursor.rowcount > 0
        if deleted:
            logger.info("DELETE_ITEM id=%s", item_id)
        return deleted

    def count_items(self) -> int:
        """How many items are saved. O(1)"""
        row = self.conn.execute("SELECT COUNT(*) FROM items").fetchone()
        return row[0]

    def close(self) -> None:
        """Close the database file. O(1)"""
        self.conn.close()