# Main window: the list of all items (feature F4, first version)
# Now with a Delete button that asks for confirmation (PDF section 4.2).

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QDialog, QHBoxLayout, QLabel, QListWidget,
                               QListWidgetItem, QMainWindow, QMessageBox,
                               QPushButton, QVBoxLayout, QWidget)

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

        self.delete_button = QPushButton("Delete Item")
        self.delete_button.setEnabled(False)            # off until something is selected
        self.delete_button.clicked.connect(self.on_delete_item)

        self.count_label = QLabel("")

        self.item_list = QListWidget()
        self.item_list.setIconSize(QSize(64, 64))
        self.item_list.setSpacing(4)
        self.item_list.itemSelectionChanged.connect(self.on_selection_changed)

        top_row = QHBoxLayout()
        top_row.addWidget(self.add_button)
        top_row.addWidget(self.delete_button)
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
            row.setData(Qt.ItemDataRole.UserRole, item["item_id"])   # remember which item
            if item["image_file"]:
                thumbnail = self.service.images.get_thumbnail_path(item["image_file"])
                row.setIcon(QIcon(str(thumbnail)))
            self.item_list.addItem(row)
        self.count_label.setText(str(self.service.count()) + " item(s)")

    def on_selection_changed(self) -> None:
        """Turn the Delete button on only when a row is selected."""
        self.delete_button.setEnabled(self.item_list.currentItem() is not None)

    def on_add_item(self) -> None:
        """Open the Add Item form. If an item was saved, redraw the list."""
        dialog = AddItemDialog(self.service, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_list()

    def on_delete_item(self) -> None:
        """Ask for confirmation, then delete the selected item."""
        row = self.item_list.currentItem()
        if row is None:
            return

        item_id = row.data(Qt.ItemDataRole.UserRole)
        item = self.service.get_item(item_id)
        if item is None:
            return

        answer = QMessageBox.question(
            self, "Delete item",
            'Delete "' + item["name"] + '" permanently?\n\n'
            "Its photo will be deleted too. This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No)                # "No" is the safe default

        if answer == QMessageBox.StandardButton.Yes:
            self.service.delete_item(item_id, user="admin")
            self.refresh_list()