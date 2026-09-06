from __future__ import annotations

from enum import Enum
from pathlib import Path

from PySide6.QtCore import QObject, QUrl, Signal, Slot
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer


class PlaybackState(str, Enum):
    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"


class AudioPlayer(QObject):
    position_changed = Signal(int)
    duration_changed = Signal(int)
    state_changed = Signal(str)
    media_finished = Signal()
    playback_failed = Signal()
    error_occurred = Signal(str)
    volume_changed = Signal(float, bool)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._output = QAudioOutput(self)
        self._player = QMediaPlayer(self)
        self._player.setAudioOutput(self._output)
        self._path: str | None = None
        self._muted_volume = 0.8
        self._output.setVolume(0.8)

        self._player.positionChanged.connect(self._on_position)
        self._player.durationChanged.connect(self._on_duration)
        self._player.playbackStateChanged.connect(self._on_state)
        self._player.mediaStatusChanged.connect(self._on_status)
        self._player.errorOccurred.connect(self._on_error)

    @property
    def path(self) -> str | None:
        return self._path

    @property
    def position(self) -> int:
        return int(self._player.position())

    @property
    def duration(self) -> int:
        return int(self._player.duration())

    @property
    def volume(self) -> float:
        return float(self._output.volume())

    @property
    def muted(self) -> bool:
        return bool(self._output.isMuted())

    @property
    def is_playing(self) -> bool:
        return self._player.playbackState() == QMediaPlayer.PlaybackState.PlayingState

    @property
    def is_paused(self) -> bool:
        return self._player.playbackState() == QMediaPlayer.PlaybackState.PausedState

    def load(self, path: str) -> bool:
        file_path = Path(path)
        if not file_path.exists() or not file_path.is_file():
            self.error_occurred.emit("This file is no longer available.")
            return False
        self._path = str(file_path)
        self._player.setSource(QUrl.fromLocalFile(str(file_path)))
        return True

    def play(self) -> None:
        self._player.play()

    def pause(self) -> None:
        self._player.pause()

    def stop(self) -> None:
        self._player.stop()

    def toggle(self) -> None:
        if self.is_playing:
            self.pause()
        else:
            self.play()

    def seek(self, position_ms: int) -> None:
        duration = self.duration
        if duration > 0:
            position_ms = max(0, min(position_ms, duration))
        self._player.setPosition(int(position_ms))

    def set_volume(self, volume: float) -> None:
        volume = max(0.0, min(1.0, float(volume)))
        self._output.setVolume(volume)
        if volume > 0 and self._output.isMuted():
            self._output.setMuted(False)
        self.volume_changed.emit(self.volume, self.muted)

    def set_muted(self, muted: bool) -> None:
        if muted and not self._output.isMuted():
            current = self._output.volume()
            if current > 0:
                self._muted_volume = current
        self._output.setMuted(muted)
        if not muted and self._output.volume() == 0:
            self._output.setVolume(self._muted_volume or 0.8)
        self.volume_changed.emit(self.volume, self.muted)

    def toggle_mute(self) -> None:
        self.set_muted(not self.muted)

    @Slot(int)
    def _on_position(self, position: int) -> None:
        self.position_changed.emit(int(position))

    @Slot(int)
    def _on_duration(self, duration: int) -> None:
        self.duration_changed.emit(int(duration))

    @Slot(QMediaPlayer.PlaybackState)
    def _on_state(self, state: QMediaPlayer.PlaybackState) -> None:
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.state_changed.emit(PlaybackState.PLAYING.value)
        elif state == QMediaPlayer.PlaybackState.PausedState:
            self.state_changed.emit(PlaybackState.PAUSED.value)
        else:
            self.state_changed.emit(PlaybackState.STOPPED.value)

    @Slot(QMediaPlayer.MediaStatus)
    def _on_status(self, status: QMediaPlayer.MediaStatus) -> None:
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.media_finished.emit()
        elif status == QMediaPlayer.MediaStatus.InvalidMedia:
            self.error_occurred.emit("This file is unsupported or corrupted.")
            self.playback_failed.emit()

    @Slot(QMediaPlayer.Error, str)
    def _on_error(self, _error: QMediaPlayer.Error, error_string: str) -> None:
        message = error_string.strip() or "Playback failed for this file."
        self.error_occurred.emit(message)
