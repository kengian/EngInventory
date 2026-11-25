# Main window: the list of all items (feature F4, first version)

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QDialog, QHBoxLayout, QLabel, QListWidget,
                               QListWidgetItem, QMainWindow, QPushButton,
                               QVBoxLayout, QWidget)

from src.services.item_service import ItemService
from src.ui.add_item_dialog import AddItemDialog


class MainWindow(QMainWindow):
    """Shows every item with its thumbnail, sorted A to Z."""

    def __init__(self, service: ItemService) -> None:
        super().__init__()
        self.service = service
        self.setWindowTitle("EngInventory - Equipment & Tools Dispensing")
        self.resize(900, 600)

        self.add_button = QPushButton("Add Item")
        self.add_button.clicked.connect(self.on_add_item)
        self.count_label = QLabel("")

        self.item_list = QListWidget()
        self.item_list.setIconSize(QSize(64, 64))
        self.item_list.setSpacing(4)

        top_row = QHBoxLayout()
        top_row.addWidget(self.add_button)
        top_row.addStretch()
        top_row.addWidget(self.count_label)

        layout = QVBoxLayout()
        layout.addLayout(top_row)
        layout.addWidget(self.item_list)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.refresh_list()

    def refresh_list(self) -> None:
        """Redraw the list from the service. O(n)"""
        self.item_list.clear()
        for item in self.service.list_items_by_name():
            text = (item["name"] + "\n"
                    + "Available: " + str(item["available"])
                    + " of " + str(item["quantity"])
                    + "   |   Condition: " + item["item_condition"]
                    + "   |   Location: " + item["storage_location"])
            row = QListWidgetItem(text)
            if item["image_file"]:
                thumbnail = self.service.images.get_thumbnail_path(item["image_file"])
                row.setIcon(QIcon(str(thumbnail)))
            self.item_list.addItem(row)
        self.count_label.setText(str(self.service.count()) + " item(s)")

    def on_add_item(self) -> None:
        """Open the Add Item form. If an item was saved, redraw the list."""
        dialog = AddItemDialog(self.service, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_list()