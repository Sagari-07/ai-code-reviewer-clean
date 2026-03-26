# database.py
import sqlite3
from datetime import datetime

DB_NAME = "code_history.db"

# ---------------- CREATE TABLE ---------------- #
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS code_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


# ---------------- INSERT CODE ---------------- #
def insert_code(code: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO code_history (code, created_at) VALUES (?, ?)",
        (code, now)
    )

    conn.commit()
    conn.close()


# ---------------- GET HISTORY ---------------- #
def get_history(limit: int = 50):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, code, created_at FROM code_history ORDER BY id DESC LIMIT ?",
        (limit,)
    )

    rows = cursor.fetchall()
    conn.close()

    return [
        {"id": row[0], "code": row[1], "created_at": row[2]}
        for row in rows
    ]