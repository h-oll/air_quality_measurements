from pathlib import Path
import sqlite3

#conn = sqlite3.connect('./measurements.db')

# looking for db

current_dir = Path('.')
db_dir = current_dir / 'db'
db_file = db_dir / 'measurements.db'

if not db_dir.exists() or not db_dir.is_dir():
	db_dir.mkdir()

db = sqlite3.connect(db_file)
