from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from app.models.song import Song
from app.player.playback_controller import RepeatMode
from app.ui.glass import GlassCard
from app.ui.icon_button import IconButton
from app.ui.icons import (
    mute_icon,
    next_icon,
    pause_icon,
    play_icon,
    prev_icon,
    repeat_icon,
    repeat_one_icon,
    shuffle_icon,
    volume_icon,
)
from app.ui.seek_slider import SeekSlider
from app.utils.timefmt import format_clock, format_remaining


class PlayerWidget(GlassCard):
    play_pause_requested = Signal()
    previous_requested = Signal()
    next_requested = Signal()
    shuffle_toggled = Signal()
    repeat_cycled = Signal()
    seek_requested = Signal(int)
    volume_changed = Signal(float)
    mute_toggled = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent, radius=32)
        self.setMinimumHeight(248)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)

        self._title = QLabel("Select a folder to begin")
        self._title.setObjectName("heroTitle")
        self._title.setWordWrap(True)
        self._artist = QLabel("Your library will appear below")
        self._artist.setObjectName("heroArtist")
        self._album = QLabel("")
        self._album.setObjectName("heroAlbum")
        self._album.setVisible(False)

        self._elapsed = QLabel("0:00")
        self._elapsed.setObjectName("timeLabel")
        self._remaining = QLabel("0:00")
        self._remaining.setObjectName("timeLabel")
        self._remaining.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.seek = SeekSlider()
        self.seek.seek_requested.connect(self.seek_requested)

        self.shuffle_button = IconButton(diameter=42, checkable=True)
        self.shuffle_button.setIcon(shuffle_icon())
        self.shuffle_button.setToolTip("Shuffle")
        self.shuffle_button.clicked.connect(self.shuffle_toggled)

        self.prev_button = IconButton(diameter=46)
        self.prev_button.setIcon(prev_icon(24))
        self.prev_button.setToolTip("Previous")
        self.prev_button.clicked.connect(self.previous_requested)

        self.play_button = IconButton(diameter=64, primary=True)
        self.play_button.setIcon(play_icon(30))
        self.play_button.setToolTip("Play")
        self.play_button.clicked.connect(self.play_pause_requested)

        self.next_button = IconButton(diameter=46)
        self.next_button.setIcon(next_icon(24))
        self.next_button.setToolTip("Next")
        self.next_button.clicked.connect(self.next_requested)

        self.repeat_button = IconButton(diameter=42, checkable=True)
        self.repeat_button.setIcon(repeat_icon())
        self.repeat_button.setToolTip("Repeat")
        self.repeat_button.clicked.connect(self.repeat_cycled)

        self.mute_button = IconButton(diameter=38)
        self.mute_button.setIcon(volume_icon())
        self.mute_button.setToolTip("Mute")
        self.mute_button.clicked.connect(self.mute_toggled)

        self.volume = QSlider(Qt.Orientation.Horizontal)
        self.volume.setObjectName("volumeSlider")
        self.volume.setRange(0, 100)
        self.volume.setValue(80)
        self.volume.setFixedWidth(120)
        self.volume.valueChanged.connect(lambda value: self.volume_changed.emit(value / 100.0))

        meta = QVBoxLayout()
        meta.setSpacing(4)
        meta.addWidget(self._title)
        meta.addWidget(self._artist)
        meta.addWidget(self._album)

        timeline = QHBoxLayout()
        timeline.setSpacing(12)
        timeline.addWidget(self._elapsed)
        timeline.addWidget(self.seek, 1)
        timeline.addWidget(self._remaining)

        transport = QHBoxLayout()
        transport.setSpacing(12)
        transport.addStretch(1)
        transport.addWidget(self.shuffle_button, 0, Qt.AlignmentFlag.AlignVCenter)
        transport.addWidget(self.prev_button, 0, Qt.AlignmentFlag.AlignVCenter)
        transport.addWidget(self.play_button, 0, Qt.AlignmentFlag.AlignVCenter)
        transport.addWidget(self.next_button, 0, Qt.AlignmentFlag.AlignVCenter)
        transport.addWidget(self.repeat_button, 0, Qt.AlignmentFlag.AlignVCenter)
        transport.addStretch(1)
        transport.addWidget(self.mute_button, 0, Qt.AlignmentFlag.AlignVCenter)
        transport.addWidget(self.volume, 0, Qt.AlignmentFlag.AlignVCenter)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 24)
        layout.setSpacing(18)
        layout.addLayout(meta)
        layout.addLayout(timeline)
        layout.addLayout(transport)

    def show_idle(self) -> None:
        self._title.setText("Select a folder to begin")
        self._artist.setText("Your library will appear below")
        self._album.setVisible(False)
        self.seek.setRange(0, 0)
        self.seek.setValue(0)
        self._elapsed.setText("0:00")
        self._remaining.setText("0:00")
        self.set_playing(False)

    def set_song(self, song: Song | None) -> None:
        if song is None:
            self.show_idle()
            return
        self._title.setText(song.display_title)
        self._artist.setText(song.display_artist)
        album = song.display_album
        self._album.setText(album)
        self._album.setVisible(bool(album))

    def set_playing(self, playing: bool) -> None:
        if playing:
            self.play_button.setIcon(pause_icon(30))
            self.play_button.setToolTip("Pause")
        else:
            self.play_button.setIcon(play_icon(30))
            self.play_button.setToolTip("Play")
        self.play_button.update()

    def set_duration(self, duration_ms: int) -> None:
        self.seek.setRange(0, max(0, duration_ms))
        self._remaining.setText(format_remaining(self.seek.value(), duration_ms))

    def set_position(self, position_ms: int) -> None:
        self.seek.set_position(position_ms)
        self._elapsed.setText(format_clock(position_ms))
        self._remaining.setText(format_remaining(position_ms, self.seek.maximum()))

    def set_shuffle(self, enabled: bool) -> None:
        self.shuffle_button.setChecked(enabled)
        self.shuffle_button.setToolTip("Shuffle on" if enabled else "Shuffle")

    def set_repeat(self, mode: str) -> None:
        if mode == RepeatMode.ONE.value:
            self.repeat_button.setChecked(True)
            self.repeat_button.setIcon(repeat_one_icon())
            self.repeat_button.setToolTip("Repeat one")
        elif mode == RepeatMode.ALL.value:
            self.repeat_button.setChecked(True)
            self.repeat_button.setIcon(repeat_icon())
            self.repeat_button.setToolTip("Repeat all")
        else:
            self.repeat_button.setChecked(False)
            self.repeat_button.setIcon(repeat_icon())
            self.repeat_button.setToolTip("Repeat")
        self.repeat_button.update()

    def set_volume(self, volume: float, muted: bool) -> None:
        self.volume.blockSignals(True)
        self.volume.setValue(0 if muted else int(round(volume * 100)))
        self.volume.blockSignals(False)
        if muted or volume <= 0:
            self.mute_button.setIcon(mute_icon())
            self.mute_button.setToolTip("Unmute")
        else:
            self.mute_button.setIcon(volume_icon())
            self.mute_button.setToolTip("Mute")
        self.mute_button.update()
