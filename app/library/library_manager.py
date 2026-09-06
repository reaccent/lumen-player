from __future__ import annotations

from PySide6.QtCore import QObject, Signal

from app.library.scanner import LibraryScanner
from app.models.song import Song


class LibraryManager(QObject):
    songs_changed = Signal(list)
    scan_progress = Signal(int, str)
    scan_failed = Signal(str)
    scan_started = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._songs: list[Song] = []
        self._folder: str | None = None
        self._scanner = LibraryScanner(self)
        self._scanner.progress.connect(self.scan_progress)
        self._scanner.finished.connect(self._on_scan_finished)
        self._scanner.failed.connect(self.scan_failed)

    @property
    def songs(self) -> list[Song]:
        return list(self._songs)

    @property
    def folder(self) -> str | None:
        return self._folder

    @property
    def busy(self) -> bool:
        return self._scanner.busy

    def load_folder(self, folder: str) -> None:
        self._folder = folder
        self.scan_started.emit(folder)
        self._scanner.scan(folder)

    def song_at(self, index: int) -> Song | None:
        if 0 <= index < len(self._songs):
            return self._songs[index]
        return None

    def index_of_path(self, path: str) -> int:
        for i, song in enumerate(self._songs):
            if song.path == path:
                return i
        return -1

    def _on_scan_finished(self, songs: list) -> None:
        self._songs = list(songs)
        self.songs_changed.emit(self.songs)
