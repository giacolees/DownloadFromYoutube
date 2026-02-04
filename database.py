import sqlite3
from pathlib import Path
from datetime import datetime

DB_NAME = "songs.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            artist TEXT,
            duration INTEGER,
            url TEXT NOT NULL,
            filepath TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_song(song_data):
    """
    Adds a song to the database.
    song_data should be a dict with keys: id, title, artist, duration, url, filepath (optional)
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO songs (id, title, artist, duration, url, filepath)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            song_data['id'],
            song_data['title'],
            song_data.get('artist'),
            song_data.get('duration'),
            song_data['url'],
            song_data.get('filepath')
        ))
        conn.commit()
        print(f"✅ Saved to DB: {song_data['title']}")
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    finally:
        conn.close()

def get_all_songs():
    conn = get_db_connection()
    songs = conn.execute('SELECT * FROM songs ORDER BY created_at DESC').fetchall()
    conn.close()
    return songs

def search_songs(query):
    conn = get_db_connection()
    like_query = f"%{query}%"
    songs = conn.execute('''
        SELECT * FROM songs 
        WHERE title LIKE ? OR artist LIKE ?
        ORDER BY created_at DESC
    ''', (like_query, like_query)).fetchall()
    conn.close()
    return songs

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
