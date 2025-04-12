import sqlite3

# Connect to database
conn = sqlite3.connect('vulnerable.db')
c = conn.cursor()

# Drop existing table and create a new one with the 'password' field
c.execute('DROP TABLE IF EXISTS users')
c.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        email TEXT,
        password TEXT
    )
''')

# Insert test data into the table with plain text passwords (vulnerable for this lab)
c.execute("INSERT INTO users (username, email, password) VALUES ('admin', 'admin@example.com', 'admin123')")
c.execute("INSERT INTO users (username, email, password) VALUES ('guest', 'guest@example.com', 'guest123')")

# Commit changes and close the connection
conn.commit()
conn.close()
