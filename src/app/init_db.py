import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS users")

cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

cursor.execute("INSERT INTO users VALUES (1, 'alice', 'admin')")
cursor.execute("INSERT INTO users VALUES (2, 'bob', 'developer')")
cursor.execute("INSERT INTO users VALUES (3, 'charlie', 'intern')")

conn.commit()
conn.close()

print(f"Database created at: {DB_PATH}")
