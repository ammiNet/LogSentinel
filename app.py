from flask import Flask
from pathlib import Path
from datetime import datetime
import sqlite3       # importing the sql database

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(debug=True)