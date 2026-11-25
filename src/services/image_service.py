# Image service (features F1 and F2, PDF section 7.3)
#
# Complexity: every operation works on ONE file, so the time depends on the
# picture size, not on how many items exist. In terms of the number of items
# the cost is O(1).
#
# Rules:
#   - only .jpg / .jpeg / .png, at most 2 MB, and it must really be an image
#   - the file is COPIED into the app's images folder
#   - it is renamed to {ItemID}_{random8}.{ext}
#   - a small thumbnail is saved in the thumbnails folder

import logging
import secrets
import shutil
from pathlib import Path
from typing import Optional

from PIL import Image

from src.services.app_paths import (ensure_folders, get_images_dir,
                                    get_thumbnails_dir)

logger = logging.getLogger("enginventory")

ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png"]
MAX_SIZE_BYTES = 2 * 1024 * 1024          # 2 MB
THUMBNAIL_SIZE = (128, 128)


class ImageService:
    """Copies item photos into the app folder and makes thumbnails."""

    def __init__(self, data_dir: Optional[Path] = None) -> None:
        base = ensure_folders(data_dir)
        self.images_dir = get_images_dir(base)
        self.thumbnails_dir = get_thumbnails_dir(base)

    def validate_image(self, source_path: Path) -> None:
        """Check the picture. Raises ValueError with a clear message if bad. O(1)"""
        source = Path(source_path)

        if not source.is_file():
            raise ValueError("The image file was not found")

        if source.suffix.lower() not in ALLOWED_EXTENSIONS:
            raise ValueError("Only JPG and PNG images are allowed")

        if source.stat().st_size > MAX_SIZE_BYTES:
            raise ValueError("The image is bigger than 2 MB")

        try:
            with Image.open(source) as picture:
                picture.verify()              # is it really a picture?
        except Exception:
            raise ValueError("The file is not a valid image")

    def save_image(self, item_id: int, source_path: Path) -> str:
        """Copy the picture in, make a thumbnail, and return the new file name.
        Store ONLY this file name in the database. O(1)"""
        self.validate_image(source_path)

        source = Path(source_path)
        extension = source.suffix.lower()
        if extension == ".jpeg":
            extension = ".jpg"

        random_part = secrets.token_hex(4)               # 8 random characters
        file_name = str(item_id) + "_" + random_part + extension

        shutil.copy2(source, self.images_dir / file_name)
        self._make_thumbnail(file_name)

        logger.info("IMAGE_SAVED item=%s file=%s", item_id, file_name)
        return file_name

    def replace_image(self, item_id: int, old_file_name: Optional[str],
                      new_source_path: Path) -> str:
        """Save the new picture first, then delete the old one.
        (If the new one is bad, the old one is kept.) O(1)"""
        new_file_name = self.save_image(item_id, new_source_path)
        if old_file_name:
            self.delete_image(old_file_name)
        return new_file_name

    def delete_image(self, file_name: Optional[str]) -> None:
        """Delete the picture and its thumbnail, if they exist. O(1)"""
        if not file_name:
            return
        for folder in [self.images_dir, self.thumbnails_dir]:
            path = folder / file_name
            if path.exists():
                path.unlink()
        logger.info("IMAGE_DELETED file=%s", file_name)

    def get_image_path(self, file_name: str) -> Path:
        """Full path of the picture. O(1)"""
        return self.images_dir / file_name

    def get_thumbnail_path(self, file_name: str) -> Path:
        """Full path of the thumbnail. O(1)"""
        return self.thumbnails_dir / file_name

    def _make_thumbnail(self, file_name: str) -> None:
        """Make a small copy of the picture. O(1)"""
        source = self.images_dir / file_name
        destination = self.thumbnails_dir / file_name

        with Image.open(source) as picture:
            picture.thumbnail(THUMBNAIL_SIZE)             # keeps the proportions
            if destination.suffix == ".jpg" and picture.mode != "RGB":
                picture = picture.convert("RGB")
            picture.save(destination)