"""
database.py — MASKGEN SQLite persistence layer.
Handles all database operations: init, save, lookup, and analytics.
"""

import sqlite3
import threading
from datetime import datetime
from contextlib import contextmanager

DB_NAME = "maskgen.db"

# Thread-safe lock — Flask thread and CLI thread both write concurrently
_db_lock = threading.Lock()


@contextmanager
def _get_connection():
    """Context manager that ensures the connection is closed."""
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Initialize the database schema."""
    with _db_lock:
        with _get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS links (
                    id            INTEGER PRIMARY KEY AUTOINCREMENT,
                    mask_text     TEXT    NOT NULL,
                    target_url    TEXT    NOT NULL,
                    redirect_code TEXT    UNIQUE NOT NULL,
                    created_at    TEXT    NOT NULL,
                    clicks        INTEGER DEFAULT 0,
                    last_accessed TEXT    DEFAULT NULL
                )
            ''')
            conn.commit()


def save_link(mask: str, target: str, code: str) -> int | None:
    """
    Persist a new masked link.
    Returns the numeric ID on success, None on redirect_code collision.
    """
    with _db_lock:
        try:
            with _get_connection() as conn:
                cursor = conn.execute(
                    "INSERT INTO links (mask_text, target_url, redirect_code, created_at) "
                    "VALUES (?, ?, ?, ?)",
                    (mask, target, code, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None


def get_target(code: str):
    """
    Look up a redirect code and atomically increment its click counter.
    Returns target URL or None.
    """
    with _db_lock:
        with _get_connection() as conn:
            row = conn.execute(
                "SELECT target_url FROM links WHERE redirect_code = ?", (code,)
            ).fetchone()
            if row:
                conn.execute(
                    "UPDATE links SET clicks = clicks + 1, last_accessed = ? "
                    "WHERE redirect_code = ?",
                    (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), code)
                )
                conn.commit()
                return row["target_url"]
    return None


def get_all_links() -> list:
    """Return all link rows ordered by creation time."""
    with _db_lock:
        with _get_connection() as conn:
            # Convert rows to dicts so they can be used after connection is closed
            rows = conn.execute(
                "SELECT id, mask_text, target_url, redirect_code, "
                "created_at, clicks, last_accessed "
                "FROM links ORDER BY id ASC"
            ).fetchall()
            return [dict(row) for row in rows]


def delete_link(link_id: int) -> bool:
    """Delete a link by numeric ID. Returns True if a row was removed."""
    with _db_lock:
        with _get_connection() as conn:
            cursor = conn.execute("DELETE FROM links WHERE id = ?", (link_id,))
            conn.commit()
            return cursor.rowcount > 0
