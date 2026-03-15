import sqlite3
from datetime import datetime

DB_NAME = "maskgen.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mask_text TEXT,
            target_url TEXT,
            redirect_code TEXT UNIQUE,
            created_at TEXT,
            clicks INTEGER DEFAULT 0
        )''')

def save_link(mask, target, code):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO links (mask_text, target_url, redirect_code, created_at) VALUES (?, ?, ?, ?)",
                     (mask, target, code, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

def get_target(code):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute("SELECT target_url FROM links WHERE redirect_code = ?", (code,))
        row = cursor.fetchone()
        if row:
            conn.execute("UPDATE links SET clicks = clicks + 1 WHERE redirect_code = ?", (code,))
            return row[0]
    return None

def get_all_links():
    with sqlite3.connect(DB_NAME) as conn:
        return conn.execute("SELECT * FROM links").fetchall()
