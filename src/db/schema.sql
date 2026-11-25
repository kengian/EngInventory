-- Items table (feature F1 and F2)
-- item_id is created automatically (AUTOINCREMENT).
-- serial_no is UNIQUE, so the same serial number cannot be added twice.
-- available starts equal to quantity and goes down when items are borrowed.
-- image_file stores ONLY the file name, never the picture itself (PDF 7.3).

CREATE TABLE IF NOT EXISTS items (
    item_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name             TEXT    NOT NULL,
    category         TEXT    NOT NULL,
    manufacturer     TEXT    NOT NULL,
    model            TEXT    NOT NULL,
    serial_no        TEXT    NOT NULL UNIQUE,
    quantity         INTEGER NOT NULL CHECK (quantity >= 0),
    available        INTEGER NOT NULL CHECK (available >= 0),
    item_condition   TEXT    NOT NULL,
    storage_location TEXT    NOT NULL,
    date_acquired    TEXT    NOT NULL,
    image_file       TEXT
);