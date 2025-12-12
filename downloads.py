import yt_dlp
import sys
import os
from pathlib import Path

def download_content():
    output_folder = Path.home() / "Downloads"
    
    # Ensure the folder exists
    if not output_folder.exists():
        os.makedirs(output_folder)

    # Get the link
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Paste the YouTube link: ").strip()

    if not url:
        print("Error: No URL provided.")
        return

    # Ask for format
    print(f"\nSaving to: {output_folder}")
    print("1: Audio (MP3)")
    print("2: Video (MP4)")
    choice = input("Enter 1 or 2: ").strip()

    # Configure Options
    save_path_template = str(output_folder / '%(title)s.%(ext)s')

    common_opts = {
        'outtmpl': save_path_template, 
        'quiet': False,
        'no_warnings': True,
        'restrictfilenames': True, 
    }

    if choice == '1':
        ydl_opts = {
            **common_opts,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        print(f"Downloading Audio...")

    else:
        ydl_opts = {
            **common_opts,
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
        }
        print(f"Downloading Video...")

    # Run
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\n✅ Saved to: {output_folder}")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    download_content()