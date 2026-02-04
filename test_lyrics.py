import yt_dlp
import os
from pathlib import Path

def test_lyrics_download():
    # Nitro - Rotten (Testo) - seemingly has lyrics on screen, maybe captions?
    # Url: https://www.youtube.com/watch?v=NimrNfqT7wk
    # Note: "Testo" means lyrics in Italian, so video is a lyric video.
    # Let's try to get subs.
    
    url = "https://www.youtube.com/watch?v=NimrNfqT7wk"
    output_folder = Path("lyrics_test")
    output_folder.mkdir(parents=True, exist_ok=True)
    
    ydl_opts = {
        'skip_download': True, # We only want info/subs
        'writesubtitles': True,
        'writeautomaticsub': True, # Fallback to auto-subs
        'subtitleslangs': ['it', 'en', 'all'], # Try Italian, English, or all
        'outtmpl': str(output_folder / '%(title)s'),
        'quiet': False,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
            }
        },
    }
    
    print(f"Attempting to download lyrics/subs for {url}...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            print("\nKeys:", info.keys())
            if 'subtitles' in info:
                print("\nManual Subtitles:", info['subtitles'].keys())
            if 'automatic_captions' in info:
                print("\nAuto Captions:", info['automatic_captions'].keys())
                
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_lyrics_download()
