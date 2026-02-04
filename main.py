import sys
from pathlib import Path
import database
import scraper
import yt_dlp
import os

def print_menu():
    print("\n🎵 Song Database & Downloader 🎵")
    print("1. Add Song (via URL)")
    print("2. Search YouTube & Add")
    print("3. Quick Add (Best Match)")
    print("4. View Library")
    print("5. Download Song from Library")
    print("6. Exit")

def add_song_flow():
    url = input("Enter YouTube URL: ").strip()
    if not url:
        return

    print("🔍 Fetching metadata...")
    metadata = scraper.scrape_metadata(url)
    
    if metadata:
        database.add_song(metadata)
        print(f"✅ Added: {metadata['title']} by {metadata['artist']}")
    else:
        print("❌ Could not fetch metadata.")

def search_and_add_flow():
    query = input("Enter search query: ").strip()
    if not query:
        return

    print(f"🔍 Searching for '{query}'...")
    results = scraper.search_youtube(query)

    if not results:
        print("No results found.")
        return

    print("\nResults:")
    for i, res in enumerate(results):
        print(f"{i+1}. {res['title']} ({res['duration']}s) - {res['artist']}")

    try:
        choice = int(input("\nEnter number to add (0 to cancel): "))
        if 1 <= choice <= len(results):
            selected = results[choice-1]
            
            # Ensure full URL if needed (scraper now returns full URL, but safety check)
            if 'url' in selected and not selected['url'].startswith('http'):
                 selected['url'] = f"https://www.youtube.com{selected['url']}"
            
            # For robustness, we could do full scrape, but metadata from search is often good enough
            database.add_song(selected)
            print(f"✅ Added: {selected['title']}")

    except ValueError:
        pass

def quick_add_flow():
    query = input("Enter song name/query: ").strip()
    if not query:
        return

    print(f"🔍 Finding best match for '{query}'...")
    best = scraper.find_best_match(query)
    
    if best:
        print(f"Found: {best['title']} by {best['artist']}")
        confirm = input("Add this song? (y/n): ").strip().lower()
        if confirm == 'y':
            database.add_song(best)
            print(f"✅ Added: {best['title']}")
    else:
        print("❌ No match found.")

def view_library_flow():
    songs = database.get_all_songs()
    if not songs:
        print("Library is empty.")
        return

    print(f"\n📚 Library ({len(songs)} songs):")
    print(f"{'ID':<15} | {'Title':<40} | {'Artist':<20} | {'Downloaded'}")
    print("-" * 90)
    for song in songs:
        downloaded = "✅" if (song['filepath'] and os.path.exists(song['filepath'])) else "❌"
        # Truncate title for display
        title = (song['title'][:37] + '...') if len(song['title']) > 37 else song['title']
        artist = (song['artist'][:17] + '...') if song['artist'] and len(song['artist']) > 17 else (song['artist'] or "Unknown")
        print(f"{song['id']:<15} | {title:<40} | {artist:<20} | {downloaded}")

def download_song_flow():
    query = input("Search in library (Title/Artist): ").strip()
    results = database.search_songs(query)
    
    if not results:
        print("No songs found in library.")
        return

    print("\nSelect song to download:")
    for i, res in enumerate(results):
        print(f"{i+1}. {res['title']} - {res['artist']}")

    try:
        choice = int(input("\nEnter number (0 to cancel): "))
        if 1 <= choice <= len(results):
            song = results[choice-1]
            if song['filepath'] and os.path.exists(song['filepath']):
                print(f"This song is already downloaded at: {song['filepath']}")
                return

            print(f"⬇️  Downloading {song['title']}...")
            
            # Use basic yt-dlp download
            output_folder = Path("downloads")
            output_folder.mkdir(parents=True, exist_ok=True)
            
            save_path_template = str(output_folder / '%(title)s.%(ext)s')
            
            print("Select Format:")
            print("1. MP3 (Compressed)")
            print("2. FLAC (Lossless)")
            fmt_choice = input("Enter number (default 1): ").strip()
            
            codec = 'mp3'
            ext = 'mp3'
            if fmt_choice == '2':
                codec = 'flac'
                ext = 'flac'
            
            ydl_opts = {
                'outtmpl': save_path_template,
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': codec,
                    'preferredquality': '192' if codec == 'mp3' else None,
                }],
                'quiet': False,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web'],
                    }
                },
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(song['url'], download=True)
                    filename = ydl.prepare_filename(info)
                    # filename might have wrong extension if postprocessed
                    final_filename = str(Path(filename).with_suffix(f'.{ext}'))
                    
                    # Update DB
                    conn = database.get_db_connection()
                    conn.execute("UPDATE songs SET filepath = ? WHERE id = ?", (final_filename, song['id']))
                    conn.commit()
                    conn.close()
                    
                    print(f"✅ Downloaded to: {final_filename}")
            except Exception as e:
                print(f"❌ Download failed: {e}")

    except ValueError:
        pass

def main():
    database.init_db()
    
    while True:
        print_menu()
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            add_song_flow()
        elif choice == '2':
            search_and_add_flow()
        elif choice == '3':
            quick_add_flow()
        elif choice == '4':
            view_library_flow()
        elif choice == '5':
            download_song_flow()
        elif choice == '6':
            print("Goodbye! 👋")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
