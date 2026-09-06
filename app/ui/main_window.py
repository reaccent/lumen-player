from __future__ import annotations

from PySide6.QtCore import QSettings, Qt, QTimer
from PySide6.QtWidgets import (
    QFileDialog,
    QGraphicsOpacityEffect,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from app.library.library_manager import LibraryManager
from app.player.audio_player import AudioPlayer
from app.player.playback_controller import PlaybackController
from app.ui.background import AnimatedBackground
from app.ui.library_widget import LibraryWidget
from app.ui.player_widget import PlayerWidget
from app.ui.styles import APP_STYLESHEET


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Lumen Player")
        self.setMinimumSize(780, 720)
        self.resize(980, 860)
        self.setStyleSheet(APP_STYLESHEET)

        self._settings = QSettings("Lumen", "LumenPlayer")
        self.library = LibraryManager(self)
        self.audio = AudioPlayer(self)
        self.controller = PlaybackController(self.audio, self)

        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)

        self.background = AnimatedBackground(root)
        self.player_widget = PlayerWidget(root)
        self.library_widget = LibraryWidget(root)

        self._toast = QLabel(root)
        self._toast.setObjectName("statusLabel")
        self._toast.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._toast.setStyleSheet(
            "background: rgba(8, 24, 48, 180); border: 1px solid rgba(186,230,253,0.28);"
            "border-radius: 14px; padding: 10px 16px; color: #F8FBFF;"
        )
        self._toast_effect = QGraphicsOpacityEffect(self._toast)
        self._toast.setGraphicsEffect(self._toast_effect)
        self._toast.hide()
        self._toast_timer = QTimer(self)
        self._toast_timer.setSingleShot(True)
        self._toast_timer.timeout.connect(self._toast.hide)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(28, 28, 28, 24)
        layout.setSpacing(18)
        layout.addWidget(self.player_widget, 0)
        layout.addWidget(self.library_widget, 1)

        self._connect_signals()
        last_folder = self._settings.value("library/folder", "", type=str)
        if last_folder:
            QTimer.singleShot(250, lambda: self.library.load_folder(last_folder))

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.background.setGeometry(self.centralWidget().rect())
        self.background.lower()
        self._position_toast()

    def _connect_signals(self) -> None:
        self.player_widget.play_pause_requested.connect(self.controller.play_pause)
        self.player_widget.previous_requested.connect(self.controller.previous)
        self.player_widget.next_requested.connect(self.controller.next)
        self.player_widget.shuffle_toggled.connect(self.controller.toggle_shuffle)
        self.player_widget.repeat_cycled.connect(self.controller.cycle_repeat)
        self.player_widget.seek_requested.connect(self.audio.seek)
        self.player_widget.volume_changed.connect(self.audio.set_volume)
        self.player_widget.mute_toggled.connect(self.audio.toggle_mute)

        self.library_widget.folder_requested.connect(self._choose_folder)
        self.library_widget.song_activated.connect(self.controller.play_index)

        self.library.scan_started.connect(self._on_scan_started)
        self.library.scan_progress.connect(self.library_widget.set_scanning)
        self.library.scan_failed.connect(self._on_scan_failed)
        self.library.songs_changed.connect(self._on_songs_changed)

        self.controller.song_changed.connect(self._on_song_changed)
        self.controller.shuffle_changed.connect(self.player_widget.set_shuffle)
        self.controller.repeat_changed.connect(self.player_widget.set_repeat)
        self.controller.queue_index_changed.connect(self._on_queue_index)

        self.audio.position_changed.connect(self.player_widget.set_position)
        self.audio.duration_changed.connect(self.player_widget.set_duration)
        self.audio.state_changed.connect(self._on_state_changed)
        self.audio.error_occurred.connect(self._show_toast)
        self.audio.volume_changed.connect(self.player_widget.set_volume)

    def _choose_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select Music Folder", self.library.folder or "")
        if folder:
            self._settings.setValue("library/folder", folder)
            self.library.load_folder(folder)

    def _on_scan_started(self, folder: str) -> None:
        self.library_widget.status.setText(f"Scanning {folder}…")

    def _on_scan_failed(self, message: str) -> None:
        self._show_toast(message)
        self.library_widget.status.setText(message)

    def _on_songs_changed(self, songs) -> None:
        self.library_widget.set_songs(songs)
        self.controller.set_library(songs, keep_current=True)
        if not songs:
            self.player_widget.show_idle()

    def _on_song_changed(self, song) -> None:
        self.player_widget.set_song(song)
        self.library_widget.set_active_path(song.path if song else None)

    def _on_queue_index(self, index: int) -> None:
        if index >= 0:
            model_index = self.library_widget.model.index(index)
            self.library_widget.view.setCurrentIndex(model_index)
            self.library_widget.view.scrollTo(model_index)

    def _on_state_changed(self, state: str) -> None:
        self.player_widget.set_playing(state == "playing")

    def _show_toast(self, message: str) -> None:
        if not message:
            return
        self._toast.setText(message)
        self._toast.adjustSize()
        self._position_toast()
        self._toast_effect.setOpacity(0.96)
        self._toast.show()
        self._toast.raise_()
        self._toast_timer.start(3200)

    def _position_toast(self) -> None:
        if not self.centralWidget():
            return
        width = min(520, self.centralWidget().width() - 80)
        self._toast.setFixedWidth(max(240, width))
        self._toast.adjustSize()
        x = (self.centralWidget().width() - self._toast.width()) // 2
        y = self.centralWidget().height() - self._toast.height() - 28
        self._toast.move(max(20, x), max(20, y))
