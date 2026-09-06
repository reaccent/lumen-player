from __future__ import annotations

from PySide6.QtCore import Property, QEasingCurve, QPropertyAnimation, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath
from PySide6.QtWidgets import QPushButton, QWidget


class IconButton(QPushButton):
    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        diameter: int = 44,
        primary: bool = False,
        checkable: bool = False,
    ) -> None:
        super().__init__(parent)
        self._primary = primary
        self._hover = 0.0
        self._press = 0.0
        self._diameter = diameter
        self.setCheckable(checkable)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(diameter, diameter)
        self.setFlat(True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._hover_anim = QPropertyAnimation(self, b"hover", self)
        self._hover_anim.setDuration(140)
        self._hover_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._press_anim = QPropertyAnimation(self, b"press", self)
        self._press_anim.setDuration(90)

    def get_hover(self) -> float:
        return self._hover

    def set_hover(self, value: float) -> None:
        self._hover = value
        self.update()

    hover = Property(float, get_hover, set_hover)

    def get_press(self) -> float:
        return self._press

    def set_press(self, value: float) -> None:
        self._press = value
        self.update()

    press = Property(float, get_press, set_press)

    def enterEvent(self, event) -> None:
        self._animate_hover(1.0)
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self._animate_hover(0.0)
        super().leaveEvent(event)

    def mousePressEvent(self, event) -> None:
        self._animate_press(1.0)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        self._animate_press(0.0)
        super().mouseReleaseEvent(event)

    def _animate_hover(self, value: float) -> None:
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover)
        self._hover_anim.setEndValue(value)
        self._hover_anim.start()

    def _animate_press(self, value: float) -> None:
        self._press_anim.stop()
        self._press_anim.setStartValue(self._press)
        self._press_anim.setEndValue(value)
        self._press_anim.start()

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect().adjusted(1, 1, -1, -1)
        path = QPainterPath()
        path.addEllipse(rect)

        if self._primary:
            fill = QColor(56, 189, 248, int(160 + 40 * self._hover - 30 * self._press))
            if self.isChecked():
                fill = QColor(34, 211, 238, 190)
            painter.fillPath(path, fill)
            glow = QColor(125, 211, 252, int(50 + 70 * self._hover))
            painter.setPen(glow)
            painter.drawEllipse(rect.adjusted(-1, -1, 1, 1))
        else:
            alpha = 28 + int(36 * self._hover) + (50 if self.isChecked() else 0)
            fill = QColor(255, 255, 255, alpha)
            if self._press:
                fill = QColor(125, 211, 252, 50)
            painter.fillPath(path, fill)
            border = QColor(186, 230, 253, 40 + int(50 * self._hover) + (70 if self.isChecked() else 0))
            painter.setPen(border)
            painter.drawEllipse(rect)

        icon = self.icon()
        if not icon.isNull():
            size = int(self._diameter * (0.46 if self._primary else 0.42))
            pixmap = icon.pixmap(size, size)
            x = (self.width() - pixmap.width()) // 2
            y = (self.height() - pixmap.height()) // 2 + int(self._press)
            painter.drawPixmap(x, y, pixmap)
        painter.end()
