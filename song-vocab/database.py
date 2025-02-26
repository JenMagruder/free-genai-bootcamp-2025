import sqlite3
from contextlib import contextmanager
from datetime import datetime

@contextmanager
def get_db_connection():
    conn = sqlite3.connect('song_vocab.db')
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db_connection() as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS vocabulary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            definition TEXT NOT NULL,
            example TEXT NOT NULL,
            song_title TEXT,
            artist TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()

def save_vocabulary(word: str, definition: str, example: str, song_title: str = None, artist: str = None):
    with get_db_connection() as conn:
        conn.execute('''
        INSERT INTO vocabulary (word, definition, example, song_title, artist)
        VALUES (?, ?, ?, ?, ?)
        ''', (word, definition, example, song_title, artist))
        conn.commit()

def get_vocabulary():
    with get_db_connection() as conn:
        cursor = conn.execute('SELECT * FROM vocabulary ORDER BY created_at DESC')
        return cursor.fetchall()
