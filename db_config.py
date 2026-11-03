# db_config.py
from pathlib import Path

# Point to mydatabase.db in the project folder
DB_PATH = Path(__file__).parent / "mydatabase.db"


SQLALCHEMY_URL = f"sqlite:///{DB_PATH.as_posix()}"
SQLITE3_PATH = str(DB_PATH)  # plain string path for sqlite3