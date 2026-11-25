# EngInventory - main entry point

import logging
import sys

from PySide6.QtWidgets import QApplication

from src.db.db_manager import DatabaseManager
from src.services.app_logger import setup_logging
from src.services.app_paths import ensure_folders, get_db_path
from src.services.image_service import ImageService
from src.services.item_service import ItemService
from src.ui.main_window import MainWindow


def main() -> int:
    """Set everything up, show the window, and clean up when it closes."""
    data_dir = ensure_folders()                 # %LOCALAPPDATA%\EngInventory
    setup_logging(data_dir)
    logger = logging.getLogger("enginventory")
    logger.info("APP_START")

    db = DatabaseManager(get_db_path(data_dir))
    db.initialize()
    images = ImageService(data_dir)
    service = ItemService(db, images)

    app = QApplication(sys.argv)
    window = MainWindow(service)
    window.show()
    exit_code = app.exec()

    db.close()
    logger.info("APP_STOP")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())