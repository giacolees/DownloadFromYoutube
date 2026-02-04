import yt_dlp

def scrape_metadata(url):
    """
    Extracts metadata from a YouTube URL without downloading the video.
    Returns a dictionary with song info or None if failed.
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True, # Fast extraction for single URLs usually works
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # If it's a playlist, simple extraction might return entries
            if 'entries' in info:
                if len(info['entries']) > 0:
                    info = info['entries'][0]
            
            return {
                'id': info.get('id'),
                'title': info.get('title'),
                'artist': info.get('uploader') or info.get('artist'), 
                'duration': info.get('duration'),
                'url': info.get('webpage_url') or info.get('url') or url
            }
            
    except Exception as e:
        print(f"❌ Error scraping metadata: {e}")
        return None

def search_youtube(query, max_results=5):
    """
    Searches YouTube and returns a list of results with metadata.
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': 'in_playlist', # Fix: True breaks search, 'in_playlist' works
        'default_search': f'ytsearch{max_results}', # Search for N results
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            
            results = []
            if 'entries' in info:
                for entry in info['entries']:
                    results.append({
                        'id': entry.get('id'),
                        'title': entry.get('title'),
                        'artist': entry.get('uploader'),
                        'duration': entry.get('duration'),
                        'url': entry.get('url') # extract_flat: 'in_playlist' returns full URL usually
                    })
            return results
            
    except Exception as e:
        print(f"❌ Error searching YouTube: {e}")
        return []

def find_best_match(query):
    """
    Finds the single best match for a query.
    Returns metadata dict or None.
    """
    results = search_youtube(query, max_results=1)
    return results[0] if results else None

if __name__ == "__main__":
    # Test scraping
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    print(f"Testing scrape for {test_url}...")
    data = scrape_metadata(test_url)
    print(data)

    # Test search
    print("\nTesting search for 'Rick Astley'...")
    results = search_youtube("Rick Astley", max_results=3)
    for r in results:
        print(r)
        
    # Test best match
    print("\nTesting best match for 'Bohemian Rhapsody'...")
    best = find_best_match("Bohemian Rhapsody")
    print(best)
