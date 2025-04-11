import sqlite3

conn = sqlite3.connect('vulnerable.db')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS users')
c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, email TEXT)')
c.execute("INSERT INTO users (username, email) VALUES ('admin', 'admin@example.com')")
c.execute("INSERT INTO users (username, email) VALUES ('guest', 'guest@example.com')")
conn.commit()
conn.close()
