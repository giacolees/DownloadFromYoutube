import database
import os

def test_database():
    # Setup
    if os.path.exists("songs.db"):
        os.remove("songs.db")
    database.init_db()
    
    # Test Add
    song = {
        'id': 'test_id',
        'title': 'Test Song',
        'artist': 'Test Artist',
        'duration': 120,
        'url': 'https://example.com',
        'filepath': None
    }
    database.add_song(song)
    
    # Test Get All
    songs = database.get_all_songs()
    assert len(songs) == 1
    assert songs[0]['title'] == 'Test Song'
    print("✅ Add and Get All passed")
    
    # Test Search
    results = database.search_songs("Test")
    assert len(results) == 1
    results = database.search_songs("NonExistent")
    assert len(results) == 0
    print("✅ Search passed")
    
    # Test Update (simulated by re-adding with filepath)
    song['filepath'] = '/path/to/file.mp3'
    database.add_song(song)
    songs = database.get_all_songs()
    assert songs[0]['filepath'] == '/path/to/file.mp3'
    print("✅ Update passed")

if __name__ == "__main__":
    test_database()
