from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Song:
    path: str
    title: str
    artist: str
    album: str
    duration_ms: int = 0

    @property
    def filename(self) -> str:
        return Path(self.path).name

    @property
    def display_title(self) -> str:
        return self.title or Path(self.path).stem

    @property
    def display_artist(self) -> str:
        return self.artist or "Unknown Artist"

    @property
    def display_album(self) -> str:
        return self.album or "Unknown Album"
