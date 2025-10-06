from flask import Flask, render_template, redirect, request, session
from helper import login_required
from database import init_tables, register_user, login_user

app = Flask(__name__)
app.config["SECRET_KEY"] = "b588233c5c433d7ffdf5416feb6ce40a"

with app.app_context():
    init_tables()


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        return redirect("/logout")
    return render_template("index.html", username=session.get("username"))


@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if login_user(username, password):
            session["username"] = username
            return redirect("/")
        else:
            msg = "Invalid username or password"

    return render_template("login.html", msg=msg)


@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        error = register_user(username, password)
        if error:
            msg = error
        else:
            login_user(username, password)

    return render_template("register.html", msg=msg)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/clear-session")
def clear_session():
    session.clear()
    return "Session cleared!"


if __name__ == "__main__":
    app.run(debug=True)
