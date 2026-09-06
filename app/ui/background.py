from __future__ import annotations

import math

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPainterPath, QRadialGradient
from PySide6.QtWidgets import QWidget


class AnimatedBackground(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._tick = 0.0
        self._timer = QTimer(self)
        self._timer.setInterval(40)
        self._timer.timeout.connect(self._advance)
        self._timer.start()
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

    def _advance(self) -> None:
        self._tick += 0.012
        self.update()

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        width = max(1, self.width())
        height = max(1, self.height())

        sky = QLinearGradient(0, 0, width, height)
        sky.setColorAt(0.0, QColor(6, 18, 42))
        sky.setColorAt(0.45, QColor(10, 42, 78))
        sky.setColorAt(1.0, QColor(8, 24, 58))
        painter.fillRect(self.rect(), sky)

        blobs = [
            (0.22, 0.28, 0.42, QColor(56, 189, 248, 90), 0.7, 0.9),
            (0.78, 0.22, 0.36, QColor(34, 211, 238, 70), 1.1, 0.6),
            (0.62, 0.72, 0.48, QColor(99, 102, 241, 80), 0.8, 1.3),
            (0.18, 0.78, 0.32, QColor(14, 165, 233, 70), 1.4, 0.8),
            (0.50, 0.48, 0.28, QColor(125, 211, 252, 40), 0.5, 1.1),
        ]
        for cx, cy, radius, color, speed, phase in blobs:
            ox = math.sin(self._tick * speed + phase) * 28
            oy = math.cos(self._tick * (speed * 0.8) + phase) * 22
            center = QPointF(width * cx + ox, height * cy + oy)
            span = min(width, height) * radius
            gradient = QRadialGradient(center, span)
            gradient.setColorAt(0.0, color)
            gradient.setColorAt(0.55, QColor(color.red(), color.green(), color.blue(), color.alpha() // 3))
            gradient.setColorAt(1.0, QColor(color.red(), color.green(), color.blue(), 0))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(gradient)
            painter.drawEllipse(center, span, span * 0.86)

        veil = QLinearGradient(0, 0, 0, height)
        veil.setColorAt(0.0, QColor(255, 255, 255, 18))
        veil.setColorAt(0.35, QColor(255, 255, 255, 0))
        veil.setColorAt(1.0, QColor(2, 8, 24, 40))
        painter.fillRect(self.rect(), veil)

        glow = QPainterPath()
        glow.addRoundedRect(QRectF(self.rect()).adjusted(18, 18, -18, -18), 36, 36)
        painter.setPen(QColor(186, 230, 253, 18))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(glow)
        painter.end()
