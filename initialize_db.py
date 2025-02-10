import sqlite3
import os

# Define Database Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

# Connect to SQLite Database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create Complaints Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image BLOB,
        status TEXT
    )
''')

# Commit and Close
conn.commit()
conn.close()

print(f"✅ Database created successfully at: {DB_PATH}")
