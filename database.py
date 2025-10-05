from flask import url_for, redirect, flash
import sqlite3
from helper import hash_pwd, verify_hash

# Esatblishing connection and cursor globally
conn = sqlite3.connect("server.db")
cursor = conn.cursor()


def init_tables() -> None:
    # Create users table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """
    )


def register_user(username: str, password: str) -> None:
    # Hash username, password
    hashed_password: str = hash_pwd(password)
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("username", "hashed_password"),
    )


def login_user(username: str, password: str) -> None:
    cursor.execute("SELECT password FROM users WHERE username = ?)", (username,))
    hashed_password: str = cursor.fetchone()
    if verify_hash(password, hashed_password):
        flash(f"{username} succesfully logged in!")
        redirect(url_for("index"))


conn.commit()  # Save changes
conn.close()  # Closing connection
