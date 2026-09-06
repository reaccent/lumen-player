from __future__ import annotations

from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QFrame, QWidget


class GlassCard(QFrame):
    def __init__(self, parent: QWidget | None = None, radius: int = 28) -> None:
        super().__init__(parent)
        self._radius = radius
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRect(0, 0, self.width(), self.height()).adjusted(1, 1, -1, -1)
        path = QPainterPath()
        path.addRoundedRect(rect, self._radius, self._radius)

        fill = QLinearGradient(rect.topLeft(), rect.bottomRight())
        fill.setColorAt(0.0, QColor(255, 255, 255, 38))
        fill.setColorAt(0.45, QColor(148, 210, 243, 22))
        fill.setColorAt(1.0, QColor(15, 50, 88, 46))
        painter.fillPath(path, fill)

        highlight = QLinearGradient(rect.topLeft(), rect.bottomLeft())
        highlight.setColorAt(0.0, QColor(255, 255, 255, 42))
        highlight.setColorAt(0.18, QColor(255, 255, 255, 0))
        painter.fillPath(path, highlight)

        painter.setPen(QPen(QColor(224, 242, 254, 48), 1.2))
        painter.drawPath(path)
        inner = QRect(rect).adjusted(1, 1, -1, -1)
        inner_path = QPainterPath()
        inner_path.addRoundedRect(inner, self._radius - 1, self._radius - 1)
        painter.setPen(QPen(QColor(255, 255, 255, 18), 1))
        painter.drawPath(inner_path)
        painter.end()
