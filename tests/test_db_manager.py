import tempfile
import unittest
from pathlib import Path

from src.db.db_manager import DatabaseManager


def make_item(serial: str = "SN-001") -> dict:
    """A sample item for testing."""
    return {
        "name": "Digital Multimeter",
        "category": "Electronics",
        "manufacturer": "Fluke",
        "model": "117",
        "serial_no": serial,
        "quantity": 5,
        "item_condition": "Good",
        "storage_location": "Shelf A1",
        "date_acquired": "2026-01-15",
    }


class TestDatabaseManager(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp.name) / "test.db"
        self.db = DatabaseManager(self.db_path)
        self.db.initialize()

    def tearDown(self):
        self.db.close()            # Windows cannot delete a file that is still open
        self.tmp.cleanup()

    def test_new_database_is_empty(self):
        self.assertEqual(self.db.count_items(), 0)

    def test_add_and_get_item(self):
        item_id = self.db.add_item(make_item())
        saved = self.db.get_item(item_id)
        self.assertEqual(saved["name"], "Digital Multimeter")
        self.assertEqual(saved["serial_no"], "SN-001")

    def test_item_ids_are_automatic(self):
        first = self.db.add_item(make_item("SN-001"))
        second = self.db.add_item(make_item("SN-002"))
        self.assertEqual(second, first + 1)

    def test_available_starts_equal_to_quantity(self):
        item_id = self.db.add_item(make_item())
        self.assertEqual(self.db.get_item(item_id)["available"], 5)

    def test_duplicate_serial_is_rejected(self):
        self.db.add_item(make_item("SN-001"))
        with self.assertRaises(ValueError):
            self.db.add_item(make_item("SN-001"))
        self.assertEqual(self.db.count_items(), 1)

    def test_negative_quantity_is_rejected(self):
        bad = make_item()
        bad["quantity"] = -1
        with self.assertRaises(ValueError):
            self.db.add_item(bad)

    def test_get_missing_item_returns_none(self):
        self.assertIsNone(self.db.get_item(999))

    def test_get_all_items(self):
        self.db.add_item(make_item("SN-001"))
        self.db.add_item(make_item("SN-002"))
        self.assertEqual(len(self.db.get_all_items()), 2)

    def test_update_item_image(self):
        item_id = self.db.add_item(make_item())
        self.db.update_item_image(item_id, "1_ab12cd34.jpg")
        self.assertEqual(self.db.get_item(item_id)["image_file"], "1_ab12cd34.jpg")

    def test_delete_item(self):
        item_id = self.db.add_item(make_item())
        self.assertTrue(self.db.delete_item(item_id))
        self.assertIsNone(self.db.get_item(item_id))

    def test_delete_missing_item_returns_false(self):
        self.assertFalse(self.db.delete_item(999))

    def test_data_survives_closing_and_reopening(self):
        item_id = self.db.add_item(make_item())
        self.db.close()
        self.db = DatabaseManager(self.db_path)       # open the same file again
        self.assertEqual(self.db.get_item(item_id)["name"], "Digital Multimeter")

    def test_initialize_twice_is_safe(self):
        self.db.add_item(make_item())
        self.db.initialize()                          # must not erase anything
        self.assertEqual(self.db.count_items(), 1)


if __name__ == "__main__":
    unittest.main()