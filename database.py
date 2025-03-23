import sqlite3

conn = sqlite3.connect("finbuddy.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT UNIQUE NOT NULL,
    access_token TEXT NOT NULL
)
""")

conn.commit()
conn.close()
