from flask import Flask, render_template, redirect, request, session, url_for
from helper import login_required, to_html
from database import *

# Initialize Flask app, SQL Tables
app = Flask(__name__)
app.config["SECRET_KEY"] = "b588233c5c433d7ffdf5416feb6ce40a"
with app.app_context():
    init_tables()


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # Fetch filenames for the regarding username
    username: str = session.get("username")
    files: tuple[str] = fetch_files(username)

    if request.method == "POST":
        # Retrieve value of current action
        action: str = request.form.get("action")

        # Logout User
        if action == "logout":
            return redirect("/logout")

        # New File
        elif action == "new_file":
            filename = request.form.get("filename")
            return redirect(url_for("editor", filename=filename))

        # Delete File
        elif action in files:  # Associates delete action with correct file
            delete_file(action, username)
            return redirect(url_for("index"))
    files: tuple[str] = fetch_files(username)
    return render_template("index.html", username=username, files=files)


@app.route("/login", methods=["GET", "POST"])
def login():
    msg: str = ""
    if request.method == "POST":
        # Get form content
        username: str = request.form.get("username")
        password: str = request.form.get("password")

        # Login user if the credentials are valid
        if login_user(username, password):
            session["username"] = username
            return redirect("/")  # Redirect to Index
        else:
            msg = "Invalid username or password"  # Displays regarding error message
    return render_template("login.html", msg=msg)


@app.route("/register", methods=["GET", "POST"])
def register():
    msg: str = ""
    if request.method == "POST":
        # Get form content; check if form is empty
        username: str = request.form.get("username", "").strip()
        password: str = request.form.get("password", "").strip()

        # Display regarding error
        if not username:
            msg = "Username is required"
        elif not password:
            msg = "Password is required"
        else:
            error = register_user(username, password)
            if error:
                msg = error
            else:
                # No error; everything was valid
                return redirect("/login")  # Redirect to login page
    return render_template("register.html", msg=msg)


@app.route("/editor/<filename>", methods=["GET", "POST"])  # Filename placeholder
@login_required
def editor(filename: str):
    username: str = session.get("username")

    if request.method == "POST":
        # Retrieve value of current action
        action = request.form.get("action")

        # Append current line if available
        if action == "append":
            line = request.form.get("line")
            if line:
                append_line(filename, line + "\n", username)
        # Delete last character
        elif action == "backspace":
            delete_char(filename, username)

    md_content = fetch_content(filename, username)  # Fetch file content from database
    html_content = to_html(md_content)  # Convert Markdown to Html
    return render_template(
        "editor.html", filename=filename, content=html_content
    )  # Render Html Content


@app.route("/logout")
def logout():
    # Clear the browsers session (Username...) and directly redirect to the login page
    session.clear()
    return redirect("/login")


# Programm main entry point
if __name__ == "__main__":
    # IMPORTANT

    # 1. Code App (iOS)
    app.run()

    # 2. PC
    # app.run(debug=True)

    # 3. Deployment (render.com)
    # app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
