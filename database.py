import sqlite3

conn = sqlite3.connect("finance.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
password TEXT
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS transactions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
amount REAL,
category TEXT,
date TEXT
)
""")

conn.execute("""
INSERT OR IGNORE INTO users(id,name,email,password)
VALUES(1,'Admin','admin@gmail.com','1234')
""")

conn.commit()
conn.close()

print("Database Created Successfully!")