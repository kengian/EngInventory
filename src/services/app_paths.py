# App folder locations (PDF section 7.3)
#
# Everything the app saves goes under %LOCALAPPDATA%\EngInventory:
#   inventory.db, images\, thumbnails\, backups\, logs\app.log
#
# Complexity: every function here is O(1).

import os
from pathlib import Path
from typing import Optional

APP_FOLDER_NAME = "EngInventory"


def get_data_dir() -> Path:
    """Return the main data folder. Tests can override it with the
    ENGINVENTORY_DATA_DIR environment variable. O(1)"""
    override = os.environ.get("ENGINVENTORY_DATA_DIR")
    if override:
        return Path(override)
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / APP_FOLDER_NAME
    return Path.home() / ("." + APP_FOLDER_NAME)      # fallback, not Windows


def _base(data_dir: Optional[Path]) -> Path:
    """Use the given folder, or the normal data folder. O(1)"""
    if data_dir is None:
        return get_data_dir()
    return Path(data_dir)


def get_db_path(data_dir: Optional[Path] = None) -> Path:
    """Path of inventory.db. O(1)"""
    return _base(data_dir) / "inventory.db"


def get_images_dir(data_dir: Optional[Path] = None) -> Path:
    """Folder for the full-size photos. O(1)"""
    return _base(data_dir) / "images"


def get_thumbnails_dir(data_dir: Optional[Path] = None) -> Path:
    """Folder for the small thumbnails. O(1)"""
    return _base(data_dir) / "thumbnails"


def get_backups_dir(data_dir: Optional[Path] = None) -> Path:
    """Folder for backup zip files. O(1)"""
    return _base(data_dir) / "backups"


def get_logs_dir(data_dir: Optional[Path] = None) -> Path:
    """Folder for the log file. O(1)"""
    return _base(data_dir) / "logs"


def get_log_file(data_dir: Optional[Path] = None) -> Path:
    """Path of app.log. O(1)"""
    return get_logs_dir(data_dir) / "app.log"


def ensure_folders(data_dir: Optional[Path] = None) -> Path:
    """Create the data folder and its sub-folders if they are missing.
    Returns the data folder. O(1)"""
    base = _base(data_dir)
    for folder in [base, get_images_dir(base), get_thumbnails_dir(base),
                   get_backups_dir(base), get_logs_dir(base)]:
        folder.mkdir(parents=True, exist_ok=True)
    return base