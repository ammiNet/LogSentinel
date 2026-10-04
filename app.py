from flask import Flask, request, render_template, redirect, url_for, session
from pathlib import Path
from datetime import datetime
import sqlite3
from analyzer import analyze_logs


app = Flask(__name__)
app.secret_key = "pls-use-your-secret-key"

BASE_DIR = Path(__file__).resolve().parent
LOG_PATH = BASE_DIR / "live.log"
DB_PATH = BASE_DIR / "users.db"


# creating function to get database connection

def getting_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


# function for initializing the database
# creates a table named users, containing id username password and role=user and date/time

def initialize_database():
    connection = getting_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


# initialize the database

initialize_database()


# function for saving the security logs in live.log

def save_log(level, message, username="", ip=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = (
        f"{timestamp} {level} {message} "
        f"username={username} ip={ip}\n"
    )

    with open(LOG_PATH, "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)


# function for getting user's IP address

def get_ip():
    return request.remote_addr or "unknown"


# registration route

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            return "Username and password are required"

        # saving details of user into database

        connection = getting_db()

        try:
            connection.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )

            connection.commit()

        except sqlite3.IntegrityError:
            connection.close()
            return "Username already exists. Please choose another username."

        connection.close()

        save_log("INFO", "User registered", username, get_ip())

        return "Registration successful"

    return render_template("register.html")


# login route

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = getting_db()

        user = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        connection.close()

        if user and user["password"] == password:
            session["username"] = user["username"]
            session["role"] = user["role"]

            save_log("INFO", "Login successful", username, get_ip())

            if user["role"] == "admin":
                return redirect("/dashboard")

            return redirect("/user-dashboard")

        save_log("WARNING", "Login failed", username, get_ip())

        return "Invalid username or password"

    return render_template("login.html")

# admin dashboard route

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        return "Access denied", 403

    search = request.args.get("search", "")
    log_type = request.args.get("log_type", "all")

    log_data = analyze_logs(search, log_type)

    return render_template(
        "dashboard.html",
        username=session["username"],
        log_data=log_data,
        search=search,
        log_type=log_type
    )


# user dashboard route

@app.route("/user-dashboard")
def user_dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template(
        "user_dashboard.html",
        username=session["username"]
    )


# logout route

@app.route("/logout")
def logout():
    username = session.get("username")

    if username:
        save_log("INFO", "Logout", username, get_ip())

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)

