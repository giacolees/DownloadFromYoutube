# 📺 Simple YouTube Downloader

A lightweight Python script to download **Video (MP4)** or **Audio (MP3)** from YouTube.

## ⚙️ Requirements
1.  **uv** (Python package manager)
2.  **FFmpeg** (Required for MP3 conversion and high-quality video)
    *   *Mac:* `brew install ffmpeg`
    *   *Windows:* `winget install Gyan.FFmpeg`
    *   *Linux:* `sudo apt install ffmpeg`

## 🚀 Installation
Initialize the environment and install dependencies:

```bash
uv init
```

```bash
uv sync
```

## ▶️ Usage

**Option 1: Interactive Mode** (Script asks for the link)
```bash
uv run main.py
```

**Option 2: Fast Mode** (Paste link directly)
```bash
uv run main.py "https://www.youtube.com/watch?v=example"
```

## 📂 Features
*   Saves files directly to your **Downloads** folder.
*   **Auto-renaming:** Replaces spaces and bad characters with `_` (e.g., `My Video.mp4` → `My_Video.mp4`).
*   Automatically merges best video and audio streams.