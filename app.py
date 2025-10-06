from flask import Flask, render_template, redirect, request, session

from helper import login_required
from database import init_tables, register_user, login_user
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "b588233c5c433d7ffdf5416feb6ce40a"
with app.app_context():
    init_tables()
msg: str = ""

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # Login required
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get form data
        password: str = request.form.get("password")
        username: str = request.form.get("username")

        # Database queries
        if not (login_user(username, password)):
            register_user(username, password)
        else: 
            session["username"] = username
            return redirect("/")
    # GET
    return render_template("login.html", msg=msg)

if __name__ == "__main__":
    app.run()