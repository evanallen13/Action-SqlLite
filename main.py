import sqlite3
import os

db_file = 'data/example.db'
os.makedirs(os.path.dirname(db_file), exist_ok=True)

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")

cursor.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')")
cursor.execute("INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com')")

conn.commit()

rows = cursor.execute("SELECT id, name, email FROM users").fetchall()
for row in rows:
    print(row)

num = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
print(f"Total number of users: {num}")
conn.close()

stat_info = os.stat(db_file)
file_size = stat_info.st_size
print(f"File Size: {file_size} bytes")
print(f"File Size: {file_size / (1024 * 1024)} mb")
print(f"File Size: {round(file_size / (1024 * 1024 * 1024), 4)} gb")