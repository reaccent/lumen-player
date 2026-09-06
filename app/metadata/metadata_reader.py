from __future__ import annotations

from pathlib import Path

from mutagen import File as MutagenFile
from mutagen.flac import FLAC
from mutagen.id3 import ID3NoHeaderError
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.oggopus import OggOpus
from mutagen.oggvorbis import OggVorbis
from mutagen.wave import WAVE

from app.models.song import Song

UNKNOWN_ARTIST = "Unknown Artist"
UNKNOWN_ALBUM = "Unknown Album"


def _first_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        for item in value:
            text = _first_text(item)
            if text:
                return text
        return ""
    text = str(value).strip()
    return text


def _from_tags(tags, keys: tuple[str, ...]) -> str:
    if not tags:
        return ""
    for key in keys:
        if key in tags:
            text = _first_text(tags[key])
            if text:
                return text
    lower_map = {str(k).lower(): k for k in tags.keys()}
    for key in keys:
        actual = lower_map.get(key.lower())
        if actual is not None:
            text = _first_text(tags[actual])
            if text:
                return text
    return ""


def _duration_ms(audio) -> int:
    try:
        info = getattr(audio, "info", None)
        length = getattr(info, "length", None)
        if length:
            return int(float(length) * 1000)
    except Exception:
        return 0
    return 0


def read_metadata(path: str | Path) -> Song:
    file_path = Path(path)
    title = file_path.stem
    artist = UNKNOWN_ARTIST
    album = UNKNOWN_ALBUM
    duration_ms = 0

    try:
        audio = MutagenFile(file_path, easy=True)
        if audio is None:
            audio = MutagenFile(file_path)
        if audio is not None:
            duration_ms = _duration_ms(audio)
            tags = audio.tags
            title_value = _from_tags(tags, ("title", "TIT2", "\xa9nam"))
            artist_value = _from_tags(
                tags,
                ("artist", "albumartist", "TPE1", "TPE2", "\xa9ART", "aART"),
            )
            album_value = _from_tags(tags, ("album", "TALB", "\xa9alb"))
            if title_value:
                title = title_value
            if artist_value:
                artist = artist_value
            if album_value:
                album = album_value
        else:
            duration_ms = _fallback_duration(file_path)
    except (ID3NoHeaderError, OSError, ValueError, Exception):
        duration_ms = _fallback_duration(file_path)

    return Song(
        path=str(file_path),
        title=title,
        artist=artist,
        album=album,
        duration_ms=duration_ms,
    )


def _fallback_duration(path: Path) -> int:
    readers = (MP3, FLAC, MP4, WAVE, OggVorbis, OggOpus)
    for reader in readers:
        try:
            audio = reader(path)
            return _duration_ms(audio)
        except Exception:
            continue
    return 0
