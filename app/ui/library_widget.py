from __future__ import annotations

from PySide6.QtCore import (
    QAbstractListModel,
    QModelIndex,
    QRect,
    QSize,
    Qt,
    Signal,
)
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListView,
    QPushButton,
    QSizePolicy,
    QStyle,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QVBoxLayout,
    QWidget,
)

from app.models.song import Song
from app.ui.glass import GlassCard
from app.ui.icons import folder_icon

TITLE_ROLE = Qt.ItemDataRole.DisplayRole
ARTIST_ROLE = Qt.ItemDataRole.UserRole + 1
ALBUM_ROLE = Qt.ItemDataRole.UserRole + 2
PATH_ROLE = Qt.ItemDataRole.UserRole + 3
ACTIVE_ROLE = Qt.ItemDataRole.UserRole + 4


class SongListModel(QAbstractListModel):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._songs: list[Song] = []
        self._active_path: str | None = None

    def set_songs(self, songs: list[Song]) -> None:
        self.beginResetModel()
        self._songs = list(songs)
        self.endResetModel()

    def set_active_path(self, path: str | None) -> None:
        self._active_path = path
        if self._songs:
            self.dataChanged.emit(self.index(0), self.index(len(self._songs) - 1), [ACTIVE_ROLE])

    def song_at(self, row: int) -> Song | None:
        if 0 <= row < len(self._songs):
            return self._songs[row]
        return None

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        if parent.isValid():
            return 0
        return len(self._songs)

    def data(self, index: QModelIndex, role: int = TITLE_ROLE):
        if not index.isValid():
            return None
        song = self._songs[index.row()]
        if role == TITLE_ROLE:
            return song.display_title
        if role == ARTIST_ROLE:
            return song.display_artist
        if role == ALBUM_ROLE:
            return song.display_album
        if role == PATH_ROLE:
            return song.path
        if role == ACTIVE_ROLE:
            return song.path == self._active_path
        return None


class SongRowDelegate(QStyledItemDelegate):
    def sizeHint(self, _option: QStyleOptionViewItem, _index: QModelIndex) -> QSize:  # noqa: N802
        return QSize(100, 72)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = option.rect.adjusted(8, 6, -8, -6)
        path = QPainterPath()
        path.addRoundedRect(rect, 16, 16)

        hovered = bool(option.state & QStyle.StateFlag.State_MouseOver)
        active = bool(index.data(ACTIVE_ROLE))
        if active:
            painter.fillPath(path, QColor(56, 189, 248, 42))
            painter.setPen(QPen(QColor(125, 211, 252, 90), 1))
            painter.drawPath(path)
        elif hovered:
            painter.fillPath(path, QColor(255, 255, 255, 22))
        else:
            painter.fillPath(path, QColor(255, 255, 255, 8))

        title = str(index.data(TITLE_ROLE) or "")
        artist = str(index.data(ARTIST_ROLE) or "")
        album = str(index.data(ALBUM_ROLE) or "")

        left = rect.adjusted(18, 12, -18, -12)
        album_width = min(220, int(left.width() * 0.32))
        text_rect = QRect(left.left(), left.top(), left.width() - album_width - 12, left.height())
        album_rect = QRect(left.right() - album_width, left.top(), album_width, left.height())

        if active:
            painter.setPen(QColor(165, 243, 252))
            painter.setBrush(QColor(165, 243, 252))
            painter.drawEllipse(left.left() - 8, left.center().y() - 3, 6, 6)
            text_rect.adjust(8, 0, 0, 0)

        title_font = QFont(option.font)
        title_font.setBold(True)
        title_font.setPointSize(13)
        artist_font = QFont(option.font)
        artist_font.setPointSize(11)
        artist_font.setBold(False)
        album_font = QFont(option.font)
        album_font.setPointSize(12)

        title_color = QColor(255, 255, 255, 245 if active else 230)
        artist_color = QColor(186, 230, 253, 210 if active else 150)
        album_color = QColor(224, 242, 254, 180 if active else 130)

        title_rect = QRect(text_rect.left(), text_rect.top(), text_rect.width(), 22)
        artist_rect = QRect(text_rect.left(), text_rect.top() + 24, text_rect.width(), 20)

        painter.setFont(title_font)
        painter.setPen(title_color)
        painter.drawText(title_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, title)
        painter.setFont(artist_font)
        painter.setPen(artist_color)
        painter.drawText(artist_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, artist)
        painter.setFont(album_font)
        painter.setPen(album_color)
        painter.drawText(album_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, album)

        divider = QColor(255, 255, 255, 18)
        painter.setPen(QPen(divider, 1))
        painter.drawLine(option.rect.left() + 24, option.rect.bottom() - 1, option.rect.right() - 24, option.rect.bottom() - 1)
        painter.restore()


class LibraryWidget(GlassCard):
    folder_requested = Signal()
    song_activated = Signal(int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent, radius=28)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        heading = QLabel("LIBRARY")
        heading.setObjectName("sectionTitle")
        self.status = QLabel("Choose a music folder to scan recursively.")
        self.status.setObjectName("statusLabel")

        self.folder_button = QPushButton("  Select Music Folder")
        self.folder_button.setObjectName("folderButton")
        self.folder_button.setIcon(folder_icon())
        self.folder_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.folder_button.clicked.connect(self.folder_requested)

        header = QHBoxLayout()
        header.setSpacing(12)
        titles = QVBoxLayout()
        titles.setSpacing(2)
        titles.addWidget(heading)
        titles.addWidget(self.status)
        header.addLayout(titles, 1)
        header.addWidget(self.folder_button, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.model = SongListModel(self)
        self.view = QListView()
        self.view.setObjectName("libraryView")
        self.view.setModel(self.model)
        self.view.setItemDelegate(SongRowDelegate(self.view))
        self.view.setUniformItemSizes(True)
        self.view.setMouseTracking(True)
        self.view.setSelectionMode(QListView.SelectionMode.SingleSelection)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollMode(QListView.ScrollMode.ScrollPerPixel)
        self.view.clicked.connect(self._on_clicked)
        self.view.doubleClicked.connect(self._on_clicked)

        empty = QLabel("No songs yet.\nSelect a folder and Lumen will import every supported track it finds.")
        empty.setObjectName("statusLabel")
        empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty.setWordWrap(True)
        self._empty = empty

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 20, 18, 16)
        layout.setSpacing(12)
        layout.addLayout(header)
        layout.addWidget(self.view, 1)
        layout.addWidget(self._empty, 1)
        self._empty.hide()

    def set_songs(self, songs: list[Song]) -> None:
        self.model.set_songs(songs)
        empty = len(songs) == 0
        self.view.setVisible(not empty)
        self._empty.setVisible(empty)
        if empty:
            self.status.setText("No supported audio files were found in that folder.")
        else:
            noun = "song" if len(songs) == 1 else "songs"
            self.status.setText(f"{len(songs)} {noun} in your library")

    def set_scanning(self, count: int, name: str) -> None:
        self.status.setText(f"Scanning… {count} files  ·  {name}")

    def set_active_path(self, path: str | None) -> None:
        self.model.set_active_path(path)

    def _on_clicked(self, index: QModelIndex) -> None:
        if index.isValid():
            self.song_activated.emit(index.row())
