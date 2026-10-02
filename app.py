from flask import Flask
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
LOG_PATH = BASE_DIR / "live.log"

if __name__ == "__main__":
    app.run(debug=True)