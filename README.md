# 🎵 Song Database & Downloader

A Python application to build a personal song database from YouTube and download audio tracks.

## ⚙️ Requirements
1.  **uv** (Python package manager)
2.  **FFmpeg** (Required for MP3 conversion)
    *   *Mac:* `brew install ffmpeg`
    *   *Windows:* `winget install Gyan.FFmpeg`
    *   *Linux:* `sudo apt install ffmpeg`

## 🚀 Installation
Initialize the environment and install dependencies:

```bash
uv sync
```

## ▶️ Usage

Run the main application:

```bash
uv run main.py
```

### Menu Options
1.  **Add Song (via URL):** Paste a YouTube link to save metadata to your library.
2.  **Search YouTube & Add:** Search for a song, view results, and add to library.
3.  **Quick Add (Best Match):** Automatically finds and adds the best match for your query.
4.  **View Library:** See all songs saved in your database (`songs.db`).
5.  **Download Song:** Download MP3s from your library to the local `downloads/` folder.

## 📂 Features
*   **Database:** Persist song metadata using SQLite.
*   **Search:** Integrated YouTube search (playlist-aware).
*   **Smart Download:** Downloads high-quality audio (192kbps MP3) to a local `downloads/` folder.
*   **Bypass Restrictions:** Uses Android client simulation to avoid 403 Forbidden errors.

## 📂 Output
Downloads are saved to the `downloads` directory inside the project folder.