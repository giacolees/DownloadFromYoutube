import syncedlyrics
from pathlib import Path

def get_lyrics(query, output_path):
    """
    Downloads lyrics for the query and saves to output_path (.lrc or .txt).
    Returns True if found, False otherwise.
    """
    try:
        # save_path needs to be string
        lrc = syncedlyrics.search(query)
        if lrc:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(lrc)
            return True
        return False
    except Exception as e:
        print(f"Error fetching lyrics: {e}")
        return False
