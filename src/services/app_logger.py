# Logging to app.log (PDF section 4.2 and 7.5: no print(), use logging)
#
# Complexity: setup_logging is O(1).

import logging
from pathlib import Path
from typing import Optional

from src.services.app_paths import ensure_folders, get_log_file

LOGGER_NAME = "enginventory"


def setup_logging(data_dir: Optional[Path] = None) -> logging.Logger:
    """Start writing log lines to logs\\app.log. Safe to call twice. O(1)"""
    base = ensure_folders(data_dir)
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)

    if not logger.handlers:                     # don't add the handler twice
        handler = logging.FileHandler(get_log_file(base), encoding="utf-8")
        handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        logger.addHandler(handler)
    return logger


def get_logger() -> logging.Logger:
    """Return the app logger. O(1)"""
    return logging.getLogger(LOGGER_NAME)