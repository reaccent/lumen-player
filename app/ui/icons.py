from __future__ import annotations

from PySide6.QtCore import QByteArray, Qt
from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

_ICON_COLOR = "#F0FDFF"
_ICON_MUTED = "rgba(240, 253, 255, 0.72)"


def _svg_icon(svg: str, size: int = 22) -> QIcon:
    renderer = QSvgRenderer(QByteArray(svg.encode("utf-8")))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    icon = QIcon(pixmap)
    icon.addPixmap(pixmap, QIcon.Mode.Normal)
    icon.addPixmap(pixmap, QIcon.Mode.Active)
    return icon


def play_icon(size: int = 28) -> QIcon:
    return _svg_icon(
        f"""
        <svg viewBox="0 0 24 24" fill="{_ICON_COLOR}">
            <path d="M8 5.2v13.6c0 .8.9 1.3 1.6.9l10.2-6.8c.7-.4.7-1.4 0-1.8L9.6 4.3C8.9 3.9 8 4.4 8 5.2z"/>
        </svg>
        """,
        size,
    )


def pause_icon(size: int = 28) -> QIcon:
    return _svg_icon(
        f"""
        <svg viewBox="0 0 24 24" fill="{_ICON_COLOR}">
            <rect x="6" y="5" width="4.2" height="14" rx="1.4"/>
            <rect x="13.8" y="5" width="4.2" height="14" rx="1.4"/>
        </svg>
        """,
        size,
    )


def prev_icon(size: int = 22) -> QIcon:
    return _svg_icon(
        f"""
        <svg viewBox="0 0 24 24" fill="{_ICON_COLOR}">
            <path d="M7 6h2.2v12H7z"/>
            <path d="M19 6.2v11.6c0 .7-.8 1.1-1.4.7L9.2 12.7c-.6-.4-.6-1.2 0-1.6l8.4-5.8c.6-.4 1.4 0 1.4.9z"/>
        </svg>
        """,
        size,
    )


def next_icon(size: int = 22) -> QIcon:
    return _svg_icon(
        f"""
        <svg viewBox="0 0 24 24" fill="{_ICON_COLOR}">
            <path d="M14.8 11.2L6.4 5.4C5.8 5 5 5.4 5 6.2v11.6c0 .8.8 1.2 1.4.8l8.4-5.8c.6-.4.6-1.2 0-1.6z"/>
            <path d="M17 6h2.2v12H17z"/>
        </svg>
        """,
        size,
    )


def shuffle_icon(size: int = 20) -> QIcon:
    return _svg_icon(
        f"""
        <svg viewBox="0 0 24 24" fill="none" stroke="{_ICON_MUTED}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 7h3.4c.6 0 1.1.3 1.5.8L14 16.2c.4.5.9.8 1.5.8H20"/>
            <path d="M17.5 4.5L20 7l-2.5 2.5"/>
            <path d="M4 17h3.4c.6 0 1.1-.3 1.5-.8L11 13.5"/>
            <path d="M17.5 19.5L20 17l-2.5-2.5"/>
        </svg>
        """,
        size,
    )


def repeat_icon(size: int = 20) -> QIcon:
    return _svg_icon(
        f"""
        <svg viewBox="0 0 24 24" fill="none" stroke="{_ICON_MUTED}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M17 3l3 3-3 3"/>
            <path d="M6 7h11a4 4 0 0 1 4 4v1"/>
            <path d="M7 21l-3-3 3-3"/>
            <path d="M18 17H7a4 4 0 0 1-4-4v-1"/>
        </svg>
        """,
        size,
    )


def repeat_one_icon(size: int = 20) -> QIcon:
    return _svg_icon(
        f"""
        <svg viewBox="0 0 24 24" fill="none" stroke="{_ICON_MUTED}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M17 3l3 3-3 3"/>
            <path d="M6 7h11a4 4 0 0 1 4 4v1"/>
            <path d="M7 21l-3-3 3-3"/>
            <path d="M18 17H7a4 4 0 0 1-4-4v-1"/>
            <path d="M12 10.2v4.6" stroke-width="2"/>
        </svg>
        """,
        size,
    )


def volume_icon(size: int = 20) -> QIcon:
    return _svg_icon(
        f"""
        <svg viewBox="0 0 24 24" fill="{_ICON_COLOR}">
            <path d="M4.5 9.2h3.1L12 5.8v12.4l-4.4-3.4H4.5A1.5 1.5 0 0 1 3 13.3v-2.6A1.5 1.5 0 0 1 4.5 9.2z"/>
            <path d="M16 8.4a5 5 0 0 1 0 7.2" fill="none" stroke="{_ICON_COLOR}" stroke-width="1.7" stroke-linecap="round"/>
            <path d="M18.4 6.2a8 8 0 0 1 0 11.6" fill="none" stroke="{_ICON_COLOR}" stroke-width="1.7" stroke-linecap="round"/>
        </svg>
        """,
        size,
    )


def mute_icon(size: int = 20) -> QIcon:
    return _svg_icon(
        f"""
        <svg viewBox="0 0 24 24" fill="{_ICON_COLOR}">
            <path d="M4.5 9.2h3.1L12 5.8v12.4l-4.4-3.4H4.5A1.5 1.5 0 0 1 3 13.3v-2.6A1.5 1.5 0 0 1 4.5 9.2z"/>
            <path d="M16.2 9.2l5 5M21.2 9.2l-5 5" fill="none" stroke="{_ICON_COLOR}" stroke-width="1.8" stroke-linecap="round"/>
        </svg>
        """,
        size,
    )


def folder_icon(size: int = 18) -> QIcon:
    return _svg_icon(
        f"""
        <svg viewBox="0 0 24 24" fill="none" stroke="{_ICON_COLOR}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3.5 8.5V7.2A2.2 2.2 0 0 1 5.7 5h4.1l2 2.2h6.5A2.2 2.2 0 0 1 20.5 9.4v7.4a2.2 2.2 0 0 1-2.2 2.2H5.7A2.2 2.2 0 0 1 3.5 16.8z"/>
        </svg>
        """,
        size,
    )
