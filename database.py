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
