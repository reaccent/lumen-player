from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, QThread, Signal

from app.metadata.metadata_reader import read_metadata
from app.models.song import Song

AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".wave",
    ".flac",
    ".aac",
    ".m4a",
    ".m4b",
    ".ogg",
    ".oga",
    ".opus",
    ".aiff",
    ".aif",
    ".wma",
}


class _ScanWorker(QObject):
    progress = Signal(int, str)
    finished = Signal(list)
    failed = Signal(str)

    def __init__(self, folder: str) -> None:
        super().__init__()
        self._folder = folder
        self._cancelled = False

    def cancel(self) -> None:
        self._cancelled = True

    def run(self) -> None:
        root = Path(self._folder)
        if not root.exists() or not root.is_dir():
            self.failed.emit("That folder could not be opened. Choose a valid music directory.")
            return

        songs: list[Song] = []
        scanned = 0
        try:
            for path in root.rglob("*"):
                if self._cancelled:
                    return
                if not path.is_file():
                    continue
                if path.suffix.lower() not in AUDIO_EXTENSIONS:
                    continue
                scanned += 1
                try:
                    song = read_metadata(path)
                    songs.append(song)
                except OSError:
                    continue
                except Exception:
                    continue
                if scanned % 8 == 0:
                    self.progress.emit(scanned, path.name)
            songs.sort(key=lambda item: (item.display_artist.lower(), item.display_album.lower(), item.display_title.lower()))
            self.finished.emit(songs)
        except PermissionError:
            self.failed.emit("Permission was denied while reading that folder.")
        except OSError as exc:
            self.failed.emit(f"The folder could not be scanned: {exc}")


class LibraryScanner(QObject):
    progress = Signal(int, str)
    finished = Signal(list)
    failed = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._thread: QThread | None = None
        self._worker: _ScanWorker | None = None

    @property
    def busy(self) -> bool:
        return self._thread is not None and self._thread.isRunning()

    def scan(self, folder: str) -> None:
        self.cancel()
        thread = QThread(self)
        worker = _ScanWorker(folder)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.progress.connect(self.progress)
        worker.finished.connect(self._on_finished)
        worker.failed.connect(self._on_failed)
        worker.finished.connect(thread.quit)
        worker.failed.connect(thread.quit)
        thread.finished.connect(worker.deleteLater)
        thread.finished.connect(self._clear_thread)
        self._thread = thread
        self._worker = worker
        thread.start()

    def cancel(self) -> None:
        if self._worker is not None:
            self._worker.cancel()
        if self._thread is not None:
            self._thread.quit()
            self._thread.wait(400)

    def _on_finished(self, songs: list) -> None:
        self.finished.emit(songs)

    def _on_failed(self, message: str) -> None:
        self.failed.emit(message)

    def _clear_thread(self) -> None:
        self._thread = None
        self._worker = None
