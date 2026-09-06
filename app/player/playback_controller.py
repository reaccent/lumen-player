from __future__ import annotations

from enum import Enum
from random import Random

from PySide6.QtCore import QObject, Signal

from app.models.song import Song
from app.player.audio_player import AudioPlayer


class RepeatMode(str, Enum):
    OFF = "off"
    ALL = "all"
    ONE = "one"


class PlaybackController(QObject):
    song_changed = Signal(object)
    shuffle_changed = Signal(bool)
    repeat_changed = Signal(str)
    queue_index_changed = Signal(int)

    def __init__(self, player: AudioPlayer, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.player = player
        self._songs: list[Song] = []
        self._order: list[int] = []
        self._cursor = -1
        self._shuffle = False
        self._repeat = RepeatMode.OFF
        self._rng = Random()
        self._restart_threshold_ms = 3000
        self._skip_attempts = 0
        self.player.media_finished.connect(self._on_finished)
        self.player.playback_failed.connect(self._skip_failed)

    @property
    def songs(self) -> list[Song]:
        return self._songs

    @property
    def current_index(self) -> int:
        if 0 <= self._cursor < len(self._order):
            return self._order[self._cursor]
        return -1

    @property
    def current_song(self) -> Song | None:
        index = self.current_index
        if 0 <= index < len(self._songs):
            return self._songs[index]
        return None

    @property
    def shuffle(self) -> bool:
        return self._shuffle

    @property
    def repeat(self) -> RepeatMode:
        return self._repeat

    def set_library(self, songs: list[Song], keep_current: bool = True) -> None:
        current_path = self.current_song.path if self.current_song else None
        self._songs = list(songs)
        self._rebuild_order()
        if keep_current and current_path:
            index = next((i for i, song in enumerate(self._songs) if song.path == current_path), -1)
            if index >= 0:
                self._cursor = self._order.index(index)
                self.queue_index_changed.emit(index)
                return
        self._cursor = -1
        self.song_changed.emit(None)
        self.queue_index_changed.emit(-1)

    def play_index(self, index: int) -> bool:
        if not 0 <= index < len(self._songs):
            return False
        if index not in self._order:
            self._rebuild_order()
        self._cursor = self._order.index(index)
        return self._play_current()

    def play_pause(self) -> None:
        if self.current_song is None:
            if self._songs:
                self._cursor = 0
                self._play_current()
            return
        if self.player.is_playing:
            self.player.pause()
        else:
            if self.player.path != self.current_song.path:
                self._play_current()
            else:
                self.player.play()

    def next(self, user_initiated: bool = True) -> None:
        if not self._songs:
            return
        if self._repeat == RepeatMode.ONE and not user_initiated:
            self._replay_current()
            return
        if not self._order:
            return
        if self._cursor < 0:
            self._cursor = 0
            self._play_current()
            return
        if self._cursor >= len(self._order) - 1:
            if self._repeat == RepeatMode.ALL or user_initiated:
                self._cursor = 0
                self._play_current()
            else:
                self.player.stop()
            return
        self._cursor += 1
        self._play_current()

    def previous(self) -> None:
        if not self._songs:
            return
        if self.player.position > self._restart_threshold_ms:
            self.player.seek(0)
            return
        if self._cursor <= 0:
            if self._repeat == RepeatMode.ALL:
                self._cursor = len(self._order) - 1
                self._play_current()
            else:
                self.player.seek(0)
            return
        self._cursor -= 1
        self._play_current()

    def toggle_shuffle(self) -> None:
        self.set_shuffle(not self._shuffle)

    def set_shuffle(self, enabled: bool) -> None:
        current = self.current_index
        self._shuffle = bool(enabled)
        self._rebuild_order(current if current >= 0 else None)
        self.shuffle_changed.emit(self._shuffle)

    def cycle_repeat(self) -> None:
        if self._repeat == RepeatMode.OFF:
            self._repeat = RepeatMode.ALL
        elif self._repeat == RepeatMode.ALL:
            self._repeat = RepeatMode.ONE
        else:
            self._repeat = RepeatMode.OFF
        self.repeat_changed.emit(self._repeat.value)

    def _rebuild_order(self, preferred: int | None = None) -> None:
        self._order = list(range(len(self._songs)))
        if self._shuffle and self._order:
            self._rng.shuffle(self._order)
            if preferred is not None and preferred in self._order:
                self._order.remove(preferred)
                self._order.insert(0, preferred)
                self._cursor = 0
                return
        if preferred is not None and preferred in self._order:
            self._cursor = self._order.index(preferred)
        elif self._order:
            self._cursor = min(max(self._cursor, 0), len(self._order) - 1)
        else:
            self._cursor = -1

    def _play_current(self) -> bool:
        song = self.current_song
        if song is None:
            return False
        if not self.player.load(song.path):
            self._skip_failed()
            return False
        self._skip_attempts = 0
        self.player.play()
        self.song_changed.emit(song)
        self.queue_index_changed.emit(self.current_index)
        return True

    def _skip_failed(self) -> None:
        self._skip_attempts += 1
        if self._skip_attempts >= max(1, len(self._songs)):
            self._skip_attempts = 0
            self.player.stop()
            return
        self.next(user_initiated=True)

    def _replay_current(self) -> None:
        self.player.seek(0)
        self.player.play()

    def _on_finished(self) -> None:
        self.next(user_initiated=False)
