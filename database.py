from flask import g
from helper import hash_pwd, verify_hash
import sqlite3


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("database.db")
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_tables():
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            content TEXT NOT NULL,
            username TEXT NOT NULL,
            UNIQUE(username, filename)
        )
        """
    )
    db.commit()


def fetch_content(filename: str, username: str) -> str:
    db = get_db()
    cursor = db.execute(
        "SELECT content FROM files WHERE username = ? AND filename = ?",
        (username, filename),
    )
    row = cursor.fetchone()
    if row:
        return row["content"]
    return ""


def fetch_files(username: str) -> tuple[str]:
    db = get_db()
    cursor = db.execute("SELECT filename FROM files WHERE username = ?", (username,))
    rows = cursor.fetchall()
    files: tuple[str] = tuple(r["filename"] for r in rows)
    return files


def append_line(filename: str, line: str, username: str):
    db = get_db()

    db.execute(
        """
        INSERT OR IGNORE INTO files (username, filename, content)
        VALUES (?, ?, '')
        """,
        (username, filename),
    )

    db.execute(
        """
        UPDATE files
        SET content = COALESCE(content, '') || CHAR(10) || ?
        WHERE username = ? AND filename = ?
        """,
        (line, username, filename),
    )

    db.commit()


def delete_char(filename: str, username: str):
    db = get_db()

    cur = db.execute(
        "SELECT content FROM files WHERE filename = ? AND username = ?",
        (filename, username),
    )
    row = cur.fetchone()
    if not row:
        return

    content = row["content"]
    if len(content) == 0:
        return

    content = content[:-1]  # remove last character

    db.execute(
        "UPDATE files SET content = ? WHERE filename = ? AND username = ?",
        (content, filename, username),
    )
    db.commit()


def delete_file(filename: str, username: str):
    db = get_db()
    db.execute(
        """
        DELETE FROM files
        WHERE filename = ? AND username = ?
        """,
        (filename, username),
    )
    db.commit()


def register_user(username: str, password: str):
    db = get_db()
    hashed_password = hash_pwd(password)
    try:
        db.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password),
        )
        db.commit()
        return None
    except sqlite3.IntegrityError:
        return "Username already taken"


def login_user(username: str, password: str) -> bool:
    db = get_db()
    cursor = db.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    if row is None:
        return False
    return verify_hash(password, row["password"])

