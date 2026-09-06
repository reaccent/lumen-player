from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QSlider, QWidget


class SeekSlider(QSlider):
    seek_requested = Signal(int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(Qt.Orientation.Horizontal, parent)
        self.setObjectName("seekSlider")
        self.setRange(0, 0)
        self.setPageStep(5000)
        self.setSingleStep(1000)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._scrubbing = False
        self.sliderPressed.connect(self._on_pressed)
        self.sliderReleased.connect(self._on_released)

    @property
    def scrubbing(self) -> bool:
        return self._scrubbing

    def set_position(self, value: int) -> None:
        if not self._scrubbing:
            self.setValue(value)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._scrubbing = True
            self._seek_from_event(event)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self._scrubbing:
            self._seek_from_event(event)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._seek_from_event(event)
            self._scrubbing = False
            self.seek_requested.emit(self.value())
        super().mouseReleaseEvent(event)

    def _on_pressed(self) -> None:
        self._scrubbing = True

    def _on_released(self) -> None:
        self._scrubbing = False
        self.seek_requested.emit(self.value())

    def _seek_from_event(self, event) -> None:
        if self.maximum() <= 0:
            return
        ratio = max(0.0, min(1.0, event.position().x() / max(1, self.width())))
        self.setValue(int(self.minimum() + ratio * (self.maximum() - self.minimum())))
