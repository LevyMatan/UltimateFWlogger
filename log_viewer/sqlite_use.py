import sqlite3

DB_FILE = 'logs.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY,
                        timestamp TEXT,
                        level TEXT,
                        message TEXT
                    )''')
    conn.commit()
    conn.close()

def insert_log(timestamp, level, message):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO logs (timestamp, level, message) VALUES (?, ?, ?)''', (timestamp, level, message))
    conn.commit()
    conn.close()

def get_logs():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM logs''')
    logs = cursor.fetchall()
    conn.close()
    return logs

# Example usage:
# init_db()
# insert_log('2024-03-08T10:00:00', 'INFO', 'Application started.')
# logs = get_logs()
# print(logs)
