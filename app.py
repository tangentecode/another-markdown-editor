from flask import Flask, render_template, redirect, request, session
from helper import login_required


app = Flask(__name__)


@login_required
@app.route("/", methods=["GET", "POST"])
def index():
    # Login required
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # if request.method == "POST":
    # Database queries

    # GET
    return render_template("login.html")
