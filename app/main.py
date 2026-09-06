from __future__ import annotations

import sys

from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication

from app.ui.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Lumen Player")
    app.setOrganizationName("Lumen")
    app.setApplicationDisplayName("Lumen Player")

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(6, 18, 42))
    palette.setColor(QPalette.ColorRole.Base, QColor(6, 18, 42))
    palette.setColor(QPalette.ColorRole.Text, QColor(244, 251, 255))
    app.setPalette(palette)

    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
