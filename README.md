# Lumen Player

A premium, minimalist desktop music player written in Python. The interface is a glassmorphism layout: frosted cards, a soft animated blue backdrop, and a library that sits directly under the player. There is no album artwork — the current track, timeline, and controls own the main stage.

## Features

- Recursively import a music folder (no per-file adding)
- Metadata for title, artist, and album when tags exist
- Play, pause, previous, next, seek, shuffle, repeat, volume, and mute
- Automatic advancement when a track ends, including repeat-one and repeat-all
- Background scanning so large libraries do not freeze the UI
- Broad format detection: MP3, WAV, FLAC, AAC, M4A, OGG, OGA, OPUS, AIFF, WMA

Playback uses Qt Multimedia. This build ships an FFmpeg backend, so common formats including MP3, WAV, FLAC, AAC, M4A, OGG, and AIFF typically play. Opus and WMA depend on the local codec set. Unsupported or damaged files are skipped without crashing.

## Requirements

- Python 3.9 or newer
- macOS, Windows, or Linux with a working Qt Multimedia backend

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

From the project root:

```bash
python -m app
```

or:

```bash
python app/main.py
```

## Use

1. Click **Select Music Folder**.
2. Choose the root of your library. Nested artist/album folders are scanned automatically.
3. Click (or double-click) a row to play.
4. Drag the timeline to seek. Use shuffle, repeat, and volume as needed.

If tags are missing, Lumen uses the filename as the title and shows **Unknown Artist** / **Unknown Album**.

## Project layout

```text
app/
├── main.py
├── ui/
├── player/
├── library/
├── metadata/
├── models/
└── utils/
```
