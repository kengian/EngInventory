import tempfile
import unittest
from pathlib import Path

from PIL import Image

from src.db.db_manager import DatabaseManager
from src.services.image_service import ImageService
from src.services.item_service import ItemService


def valid_data(serial="SN-001", name="Digital Multimeter", category="Electronics"):
    """Form data as the screen would send it (numbers arrive as text)."""
    return {
        "name": name,
        "category": category,
        "manufacturer": "Fluke",
        "model": "117",
        "serial_no": serial,
        "quantity": "5",
        "item_condition": "Good",
        "storage_location": "Shelf A1",
        "date_acquired": "2026-01-15",
    }


class TestItemService(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self.tmp.name)
        self.db_path = self.folder / "test.db"
        self.db = DatabaseManager(self.db_path)
        self.db.initialize()
        self.images = ImageService(data_dir=self.folder / "appdata")
        self.service = ItemService(self.db, self.images)

    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def make_picture(self, name="photo.jpg") -> Path:
        path = self.folder / name
        Image.new("RGB", (300, 200), "blue").save(path)
        return path

    def names(self, items):
        return [item["name"] for item in items]

    # ----- adding and validating -----

    def test_add_item_returns_saved_item(self):
        item = self.service.add_item(valid_data())
        self.assertTrue(item["item_id"] >= 1)
        self.assertEqual(item["quantity"], 5)
        self.assertEqual(item["available"], 5)
        self.assertEqual(self.service.count(), 1)

    def test_serial_is_saved_in_capitals(self):
        item = self.service.add_item(valid_data(serial="sn-abc"))
        self.assertEqual(item["serial_no"], "SN-ABC")

    def test_lookup_by_id_and_serial(self):
        item = self.service.add_item(valid_data())
        self.assertEqual(self.service.get_item(item["item_id"])["name"], "Digital Multimeter")
        self.assertEqual(self.service.get_item_by_serial("sn-001")["item_id"], item["item_id"])
        self.assertIsNone(self.service.get_item(999))
        self.assertIsNone(self.service.get_item_by_serial("nope"))

    def test_duplicate_serial_rejected(self):
        self.service.add_item(valid_data(serial="SN-001"))
        with self.assertRaises(ValueError):
            self.service.add_item(valid_data(serial="sn-001"))
        self.assertEqual(self.service.count(), 1)

    def test_missing_name_rejected(self):
        data = valid_data()
        data["name"] = "   "
        with self.assertRaises(ValueError) as context:
            self.service.add_item(data)
        self.assertIn("Name", str(context.exception))

    def test_bad_quantity_rejected(self):
        for bad in ["abc", "0", "-2", "", "10000", "2.5"]:
            with self.subTest(quantity=bad):
                data = valid_data()
                data["quantity"] = bad
                with self.assertRaises(ValueError):
                    self.service.add_item(data)

    def test_bad_condition_rejected(self):
        data = valid_data()
        data["item_condition"] = "Shiny"
        with self.assertRaises(ValueError):
            self.service.add_item(data)

    def test_bad_date_rejected(self):
        for bad in ["15/01/2026", "2026-13-40", "yesterday", ""]:
            with self.subTest(date=bad):
                data = valid_data()
                data["date_acquired"] = bad
                with self.assertRaises(ValueError):
                    self.service.add_item(data)

    def test_future_date_rejected(self):
        data = valid_data()
        data["date_acquired"] = "2999-01-01"
        with self.assertRaises(ValueError):
            self.service.add_item(data)

    # ----- images -----

    def test_add_with_image(self):
        item = self.service.add_item(valid_data(), image_path=self.make_picture())
        self.assertTrue(item["image_file"].startswith(str(item["item_id"]) + "_"))
        self.assertTrue(self.images.get_image_path(item["image_file"]).exists())
        self.assertTrue(self.images.get_thumbnail_path(item["image_file"]).exists())

    def test_bad_image_rejects_whole_item(self):
        fake = self.folder / "fake.jpg"
        fake.write_text("not a picture")
        with self.assertRaises(ValueError):
            self.service.add_item(valid_data(), image_path=fake)
        self.assertEqual(self.service.count(), 0)
        self.assertEqual(self.db.count_items(), 0)

    def test_replace_image(self):
        item = self.service.add_item(valid_data(), image_path=self.make_picture("a.jpg"))
        old_file = item["image_file"]
        new_file = self.service.replace_item_image(item["item_id"], self.make_picture("b.jpg"))
        self.assertNotEqual(old_file, new_file)
        self.assertFalse(self.images.get_image_path(old_file).exists())
        self.assertEqual(self.db.get_item(item["item_id"])["image_file"], new_file)

    # ----- listing and searching -----

    def test_list_items_by_name_is_sorted(self):
        self.service.add_item(valid_data("S1", "Oscilloscope"))
        self.service.add_item(valid_data("S2", "Caliper"))
        self.service.add_item(valid_data("S3", "Multimeter"))
        self.assertEqual(self.names(self.service.list_items_by_name()),
                         ["Caliper", "Multimeter", "Oscilloscope"])

    def test_list_items_by_category(self):
        self.service.add_item(valid_data("S1", "Oscilloscope", "Electronics"))
        self.service.add_item(valid_data("S2", "Caliper", "Measuring"))
        self.service.add_item(valid_data("S3", "Multimeter", "Electronics"))
        self.service.add_item(valid_data("S4", "Anvil", "Hand Tools"))
        self.assertEqual(self.names(self.service.list_items_by_category()),
                         ["Multimeter", "Oscilloscope", "Anvil", "Caliper"])

    def test_search_by_prefix(self):
        self.service.add_item(valid_data("S1", "Caliper"))
        self.service.add_item(valid_data("S2", "Calculator"))
        self.service.add_item(valid_data("S3", "Cable"))
        self.assertEqual(self.names(self.service.search("CAL")), ["Calculator", "Caliper"])

    def test_search_with_category_filter(self):
        self.service.add_item(valid_data("S1", "Caliper", "Measuring"))
        self.service.add_item(valid_data("S2", "Calculator", "Electronics"))
        self.assertEqual(self.names(self.service.search("cal", category="Measuring")), ["Caliper"])
        self.assertEqual(len(self.service.search("cal", category="All")), 2)

    def test_search_with_no_match(self):
        self.service.add_item(valid_data())
        self.assertEqual(self.service.search("zzz"), [])

    def test_suggest_names(self):
        self.service.add_item(valid_data("S1", "Caliper"))
        self.service.add_item(valid_data("S2", "Calculator"))
        self.assertEqual(self.service.suggest_names("ca"), ["Calculator", "Caliper"])

    def test_list_categories(self):
        self.service.add_item(valid_data("S1", "Oscilloscope", "Electronics"))
        self.service.add_item(valid_data("S2", "Caliper", "Measuring"))
        self.service.add_item(valid_data("S3", "Multimeter", "Electronics"))
        self.service.add_item(valid_data("S4", "Anvil", "Hand Tools"))
        self.assertEqual(self.service.list_categories(),
                         ["Electronics", "Hand Tools", "Measuring"])

    # ----- deleting -----

    def test_delete_item_removes_everything(self):
        item = self.service.add_item(valid_data(), image_path=self.make_picture())
        file_name = item["image_file"]
        self.assertTrue(self.service.delete_item(item["item_id"]))
        self.assertIsNone(self.service.get_item(item["item_id"]))
        self.assertIsNone(self.service.get_item_by_serial("SN-001"))
        self.assertIsNone(self.db.get_item(item["item_id"]))
        self.assertFalse(self.images.get_image_path(file_name).exists())
        self.assertEqual(self.service.suggest_names("dig"), [])

    def test_delete_missing_item_returns_false(self):
        self.assertFalse(self.service.delete_item(999))

    def test_delete_keeps_name_if_another_item_uses_it(self):
        first = self.service.add_item(valid_data("S1", "Caliper"))
        second = self.service.add_item(valid_data("S2", "Caliper"))
        self.service.delete_item(first["item_id"])
        self.assertEqual(self.service.suggest_names("cal"), ["Caliper"])
        self.service.delete_item(second["item_id"])
        self.assertEqual(self.service.suggest_names("cal"), [])

    # ----- persistence -----

    def test_items_are_reloaded_after_restart(self):
        self.service.add_item(valid_data("S1", "Oscilloscope"))
        self.service.add_item(valid_data("S2", "Caliper"))

        second_db = DatabaseManager(self.db_path)       # "start the app again"
        try:
            second_service = ItemService(second_db, self.images)
            self.assertEqual(self.names(second_service.list_items_by_name()),
                             ["Caliper", "Oscilloscope"])
            self.assertIsNotNone(second_service.get_item_by_serial("S1"))
            self.assertEqual(second_service.suggest_names("os"), ["Oscilloscope"])
        finally:
            second_db.close()


if __name__ == "__main__":
    unittest.main()