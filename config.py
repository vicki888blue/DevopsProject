# config.py
import os
from pathlib import Path

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-insecure-change-me")

    PROJECT_DIR = Path(__file__).parent.resolve()
    PA_USERNAME = "vicki888blue"
    PA_DB_PATH = f"/home/{PA_USERNAME}/mydatabase.db"

    # Choose DB in this order:
    # 1) DATABASE_URL env var (if you set one in Web → Environment variables
    # 2) Absolute path on PythonAnywhere (if the file exists)
    # 3) Local file next to config.py
    if os.getenv("DATABASE_URL"):
        DATABASE_URL = os.getenv("DATABASE_URL")
    elif os.path.exists(PA_DB_PATH):
        DATABASE_URL = f"sqlite:////{PA_DB_PATH}"
    else:
        DATABASE_URL = f"sqlite:///{(PROJECT_DIR / 'mydatabase.db').as_posix()}"

    # Flask‑SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False