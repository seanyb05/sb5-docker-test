from app import main

from pathlib import Path
import os

base_dir = Path(__file__).resolve().parent.parent
DB_FILE = Path(base_dir.joinpath("data").joinpath("db_url.txt"))

main.delete_last_line(DB_FILE)