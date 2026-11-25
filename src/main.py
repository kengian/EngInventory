# EngInventory - main entry point
# (This is a tiny practice window. We will replace it with the real app later.)

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow,
                               QPushButton, QVBoxLayout, QWidget)


class MainWindow(QMainWindow):
    """The main window of the app."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("EngInventory")
        self.resize(500, 300)
        self.clicks = 0

        # 1. Make the widgets
        self.label = QLabel("Hello! Click the button.")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button = QPushButton("Click me")

        # 2. Connect the signal (click) to the slot (our function)
        self.button.clicked.connect(self.on_button_clicked)

        # 3. Put them in a layout (top to bottom)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_button_clicked(self) -> None:
        """Runs every time the button is clicked."""
        self.clicks += 1
        self.label.setText("You clicked " + str(self.clicks) + " time(s)!")


def main() -> int:
    """Start the app and keep the window open until it is closed."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())