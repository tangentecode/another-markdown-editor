from flask import Flask, render_template, redirect, request, session, url_for
from helper import login_required, to_html, test_html
from database import init_tables, register_user, login_user, append_line, fetch_content, fetch_files

app = Flask(__name__)
app.config["SECRET_KEY"] = "b588233c5c433d7ffdf5416feb6ce40a"

with app.app_context():
    init_tables()

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    username: str = session.get("username")

    if request.method == "POST":
        submittet_form: str = request.form.get("form_name")

        if submittet_form == "logout":
            return redirect("/logout")

        elif submittet_form == "new_file":
            filename = request.form.get("filename")
            return redirect(url_for("editor", filename=filename))

    files: tuple[str] = fetch_files(username)
    return render_template("index.html", username=username, files=files)

@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST":
        username: str = request.form.get("username")
        password: str = request.form.get("password")

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
        username: str = request.form.get("username", "").strip()
        password: str = request.form.get("password", "").strip()
        if not username:
            msg = "Username is required"
        elif not password:
            msg = "Password is required"
        else:
            error = register_user(username, password)
            if error:
                msg = error
            else:
                return redirect("/login")

    return render_template("register.html", msg=msg)
		
@app.route("/editor/<filename>", methods=["GET", "POST"])
@login_required
def editor(filename: str):
    username: str = session.get("username")

    if request.method == "POST":
        line = request.form.get("line")
        if line:
            append_line(filename, line + "\n", username)

    md_content = fetch_content(filename, username)
    html_content = test_html(md_content)
    return render_template("editor.html", filename=filename, content=html_content)
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/clear-session")
def clear_session():
    session.clear()
    return "Session cleared!"

if __name__ == "__main__":
    app.run()
