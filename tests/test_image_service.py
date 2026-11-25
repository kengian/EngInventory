import re
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from src.services.image_service import ImageService


class TestImageService(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self.tmp.name)
        self.service = ImageService(data_dir=self.folder / "appdata")

    def tearDown(self):
        self.tmp.cleanup()

    def make_picture(self, name: str, size=(400, 300)) -> Path:
        """Create a real picture file for testing."""
        path = self.folder / name
        Image.new("RGB", size, "red").save(path)
        return path

    def test_save_jpg_gives_correct_file_name(self):
        source = self.make_picture("photo.jpg")
        file_name = self.service.save_image(1, source)
        self.assertTrue(re.match(r"^1_[0-9a-f]{8}\.jpg$", file_name))

    def test_picture_is_copied_to_images_folder(self):
        source = self.make_picture("photo.jpg")
        file_name = self.service.save_image(1, source)
        self.assertTrue(self.service.get_image_path(file_name).exists())
        self.assertTrue(source.exists())              # the original is untouched

    def test_thumbnail_is_created_and_small(self):
        source = self.make_picture("photo.png", size=(800, 600))
        file_name = self.service.save_image(2, source)
        thumb_path = self.service.get_thumbnail_path(file_name)
        self.assertTrue(thumb_path.exists())
        with Image.open(thumb_path) as thumb:
            self.assertTrue(thumb.width <= 128)
            self.assertTrue(thumb.height <= 128)

    def test_two_saves_give_different_names(self):
        source = self.make_picture("photo.jpg")
        first = self.service.save_image(1, source)
        second = self.service.save_image(1, source)
        self.assertNotEqual(first, second)

    def test_jpeg_extension_becomes_jpg(self):
        source = self.make_picture("photo.jpeg")
        file_name = self.service.save_image(3, source)
        self.assertTrue(file_name.endswith(".jpg"))

    def test_rejects_wrong_file_type(self):
        path = self.folder / "picture.gif"
        path.write_bytes(b"GIF89a")
        with self.assertRaises(ValueError):
            self.service.save_image(1, path)

    def test_rejects_fake_image(self):
        path = self.folder / "fake.jpg"
        path.write_text("this is just text, not a picture")
        with self.assertRaises(ValueError):
            self.service.save_image(1, path)

    def test_rejects_missing_file(self):
        with self.assertRaises(ValueError):
            self.service.save_image(1, self.folder / "nothing.jpg")

    def test_rejects_file_bigger_than_2mb(self):
        path = self.folder / "huge.jpg"
        path.write_bytes(b"0" * (2 * 1024 * 1024 + 1))
        with self.assertRaises(ValueError):
            self.service.save_image(1, path)

    def test_delete_removes_picture_and_thumbnail(self):
        source = self.make_picture("photo.jpg")
        file_name = self.service.save_image(1, source)
        self.service.delete_image(file_name)
        self.assertFalse(self.service.get_image_path(file_name).exists())
        self.assertFalse(self.service.get_thumbnail_path(file_name).exists())

    def test_delete_missing_file_does_not_crash(self):
        self.service.delete_image("not_there.jpg")
        self.service.delete_image(None)

    def test_replace_deletes_the_old_picture(self):
        first = self.service.save_image(1, self.make_picture("a.jpg"))
        second = self.service.replace_image(1, first, self.make_picture("b.jpg"))
        self.assertFalse(self.service.get_image_path(first).exists())
        self.assertTrue(self.service.get_image_path(second).exists())

    def test_replace_with_bad_file_keeps_the_old_picture(self):
        first = self.service.save_image(1, self.make_picture("a.jpg"))
        bad = self.folder / "bad.jpg"
        bad.write_text("not a picture")
        with self.assertRaises(ValueError):
            self.service.replace_image(1, first, bad)
        self.assertTrue(self.service.get_image_path(first).exists())


if __name__ == "__main__":
    unittest.main()