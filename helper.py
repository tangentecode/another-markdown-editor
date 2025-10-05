from flask import flash, redirect, url_for, session, request
from functools import wraps
from argon2 import PasswordHasher


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in
        if "user_id" not in session:
            flash("Please login to access this Page")
            # Redirect to login page, with "next" parameter to return after login
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def hash_pwd(pwd: str) -> str:
    ph = PasswordHasher()
    return ph.hash(pwd)


def verify_hash(pwd_login: str, pwd_hash: str) -> bool:
    ph = PasswordHasher()
    try:
        if ph.verify(pwd_hash, pwd_login):
            return True
    except Exception:
        return False
