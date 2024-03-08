from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import datetime
import sqlite3
import time

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_position = 0

    def on_modified(self, event):
        # Connect to the SQLite database
        conn = sqlite3.connect('logs.db')
        c = conn.cursor()

        with open('shared_log_file.txt', 'r') as f:
            # Move to the last read position
            f.seek(self.last_position)
            lines = f.readlines()
            for line in lines:
                # Insert a row of data
                c.execute("INSERT INTO logs VALUES (?, ?)", (str(datetime.datetime.now()), line))
                print(f'Added the line "{line}" to the database')

            # Save the last position
            self.last_position = f.tell()

        # Save (commit) the changes
        conn.commit()
        # Close the connection
        conn.close()


# Innitialize the loggs database
conn = sqlite3.connect('logs.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS logs (date text, log text)''')
conn.commit()
conn.close()

event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path='shared_log_file.txt', recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()