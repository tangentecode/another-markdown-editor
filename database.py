from flask import url_for, redirect, flash, g
from helper import hash_pwd, verify_hash
import sqlite3
from flask import g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("database.db", check_same_thread=False)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_tables() -> None:
    db = get_db()
    # Create users table
    db.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """
    )
    db.commit()  # Save changes


def register_user(username: str, password: str) -> None:
    db = get_db()
    # Hash username, password
    hashed_password: str = hash_pwd(password)
    try: 
        db.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("username", "hashed_password"),
        )
    except sqlite3.IntegrityError:
        msg: str = "Username already taken"
    db.commit()  # Save changes


def login_user(username: str, password: str) -> bool:
    db = get_db()
    cursor = db.execute("SELECT password FROM users WHERE username = ?", (username,))
    hashed_password: str = cursor.fetchone()
    if verify_hash(password, hashed_password):
        return True
    db.commit()  # Save changes
    return False

