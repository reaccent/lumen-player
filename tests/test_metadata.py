from pathlib import Path
import wave

from app.library.scanner import AUDIO_EXTENSIONS
from app.metadata.metadata_reader import read_metadata
from app.models.song import Song


def _write_silence_wav(path: Path) -> None:
    with wave.open(str(path), "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(8000)
        wav.writeframes(b"\x00\x00" * 800)


def test_missing_tags_use_filename(tmp_path: Path):
    path = tmp_path / "Midnight Drive.wav"
    _write_silence_wav(path)
    song = read_metadata(path)
    assert song.title == "Midnight Drive"
    assert song.display_artist == "Unknown Artist"
    assert song.display_album == "Unknown Album"
    assert song.duration_ms >= 0


def test_song_display_helpers():
    song = Song(path="/tmp/a.mp3", title="", artist="", album="")
    assert song.display_title == "a"
    assert song.display_artist == "Unknown Artist"
    assert song.display_album == "Unknown Album"


def test_supported_extensions_cover_common_formats():
    expected = {".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg", ".oga", ".opus", ".aiff", ".wma"}
    assert expected.issubset(AUDIO_EXTENSIONS)
