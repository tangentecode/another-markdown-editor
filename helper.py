from flask import redirect, session, request
from functools import wraps
from argon2 import PasswordHasher
import secrets


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in
        if "username" not in session:
            return redirect("/login")
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


def gen_secret_key():
    print(secrets.token_hex(16))

