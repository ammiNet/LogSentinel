import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "users.db"


username = input("Enter admin username: ")
password = input("Enter admin password: ")


connection = sqlite3.connect(DB_PATH)

connection.execute(
    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
    (username, password, "admin")
)

connection.commit()
connection.close()

print("Admin account created successfully! you can login now in dashboard")