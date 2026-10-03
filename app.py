from flask import Flask, request, render_template, redirect, url_for, session
from pathlib import Path
from datetime import datetime
import sqlite3       # importing the sql database

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


# function for saving security logs

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

        # checking if username and password were entered

        if not username or not password:
            return "Username and password are required"

        # saving user into database

        connection = getting_db()

        connection.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        connection.commit()
        connection.close()

        # saving registration event in log

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

            return "Login successful"

        return "Invalid username or password"

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)