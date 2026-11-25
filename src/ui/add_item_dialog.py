# Add Item form (features F1 and F2)
# The form only collects what the admin typed. ItemService does the checking
# and saving, and gives a clear error message if something is wrong.

from pathlib import Path
from typing import Any, Dict, Optional

from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QComboBox, QDateEdit, QDialog, QDialogButtonBox,
                               QFileDialog, QFormLayout, QLabel, QLineEdit,
                               QMessageBox, QPushButton, QSpinBox, QVBoxLayout,
                               QWidget)

from src.services.item_service import CONDITIONS, ItemService


class AddItemDialog(QDialog):
    """A popup form for adding one item."""

    def __init__(self, service: ItemService, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.service = service
        self.image_path: Optional[Path] = None      # the photo the admin chose
        self.saved_item: Optional[Dict[str, Any]] = None

        self.setWindowTitle("Add Item")
        self.setMinimumWidth(480)

        # ----- the input boxes -----
        self.name_edit = QLineEdit()
        self.category_box = QComboBox()
        self.category_box.setEditable(True)               # pick one OR type a new one
        self.category_box.addItems(self.service.list_categories())
        self.category_box.setCurrentText("")
        self.manufacturer_edit = QLineEdit()
        self.model_edit = QLineEdit()
        self.serial_edit = QLineEdit()
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, 9999)
        self.condition_box = QComboBox()
        self.condition_box.addItems(CONDITIONS)
        self.location_edit = QLineEdit()
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_edit.setMaximumDate(QDate.currentDate())   # not in the future

        # ----- the photo part -----
        self.photo_button = QPushButton("Choose Photo...")
        self.photo_button.clicked.connect(self.on_choose_photo)
        self.photo_label = QLabel("No photo selected")
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.photo_label.setMinimumHeight(160)
        self.photo_label.setStyleSheet("border: 1px solid gray;")

        # ----- put the boxes in a form layout -----
        form = QFormLayout()
        form.addRow("Name *", self.name_edit)
        form.addRow("Category *", self.category_box)
        form.addRow("Manufacturer *", self.manufacturer_edit)
        form.addRow("Model *", self.model_edit)
        form.addRow("Serial No. *", self.serial_edit)
        form.addRow("Quantity *", self.quantity_spin)
        form.addRow("Condition *", self.condition_box)
        form.addRow("Storage Location *", self.location_edit)
        form.addRow("Date Acquired *", self.date_edit)
        form.addRow("Photo (JPG/PNG, max 2 MB)", self.photo_button)

        # ----- Save and Cancel buttons -----
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save |
                                   QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.on_save)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.photo_label)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def on_choose_photo(self) -> None:
        """Let the admin pick a photo and show a preview."""
        path, _ = QFileDialog.getOpenFileName(
            self, "Choose a photo", "", "Images (*.jpg *.jpeg *.png)")
        if path == "":                                    # the admin pressed Cancel
            return

        try:
            self.service.images.validate_image(Path(path))
        except ValueError as error:
            QMessageBox.warning(self, "Cannot use this photo", str(error))
            return

        self.image_path = Path(path)
        preview = QPixmap(path).scaled(
            150, 150, Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation)
        self.photo_label.setPixmap(preview)

    def on_save(self) -> None:
        """Send the form data to the service. Show its message if it fails."""
        data = {
            "name": self.name_edit.text(),
            "category": self.category_box.currentText(),
            "manufacturer": self.manufacturer_edit.text(),
            "model": self.model_edit.text(),
            "serial_no": self.serial_edit.text(),
            "quantity": str(self.quantity_spin.value()),
            "item_condition": self.condition_box.currentText(),
            "storage_location": self.location_edit.text(),
            "date_acquired": self.date_edit.date().toString("yyyy-MM-dd"),
        }

        try:
            self.saved_item = self.service.add_item(data, self.image_path, user="admin")
        except ValueError as error:
            QMessageBox.warning(self, "Cannot save item", str(error))
            return                                        # stay open so they can fix it

        self.accept()                                     # close the form