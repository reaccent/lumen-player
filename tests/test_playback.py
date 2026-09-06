from __future__ import annotations

from app.models.song import Song
from app.player.playback_controller import PlaybackController, RepeatMode


class DummyPlayer:
    def __init__(self) -> None:
        self.path = None
        self.position = 0
        self._playing = False
        self.media_finished = _Signal()
        self.playback_failed = _Signal()
        self.loaded = []

    def load(self, path: str) -> bool:
        self.path = path
        self.loaded.append(path)
        return True

    def play(self) -> None:
        self._playing = True

    def pause(self) -> None:
        self._playing = False

    def stop(self) -> None:
        self._playing = False

    def seek(self, position_ms: int) -> None:
        self.position = position_ms

    @property
    def is_playing(self) -> bool:
        return self._playing


class _Signal:
    def connect(self, _callback) -> None:
        return None


def _songs() -> list[Song]:
    return [
        Song("/tmp/one.mp3", "One", "A", "X"),
        Song("/tmp/two.mp3", "Two", "A", "X"),
        Song("/tmp/three.mp3", "Three", "B", "Y"),
    ]


def test_play_index_and_next():
    player = DummyPlayer()
    controller = PlaybackController(player)
    controller.set_library(_songs())
    assert controller.play_index(0) is True
    assert controller.current_song.title == "One"
    controller.next()
    assert controller.current_song.title == "Two"


def test_repeat_one_replays_on_natural_finish():
    player = DummyPlayer()
    controller = PlaybackController(player)
    controller.set_library(_songs())
    controller.play_index(1)
    controller.cycle_repeat()
    controller.cycle_repeat()
    assert controller.repeat == RepeatMode.ONE
    player.loaded.clear()
    controller._on_finished()
    assert player.loaded == []
    assert controller.current_song.title == "Two"
    assert player.position == 0
