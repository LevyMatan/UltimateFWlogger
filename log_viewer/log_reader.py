from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from logger_db import DatabaseThread
import datetime
import time

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_position = 0
        self.log_id = 0
        self.db_thread = DatabaseThread('logs.db')
        self.db_thread.start()

    def on_modified(self, event):
        """
        Callback method triggered when the shared log file is modified.

        This method reads the newly added lines in the shared log file,
        parses them into timestamp, level, and message, and inserts them
        into the database.

        Args:
            event: The event object representing the file modification.

        Returns:
            None
        """
        with open('shared_log_file.txt', 'r', encoding='utf-8') as f:
            # Move to the last read position
            f.seek(self.last_position)
            lines = f.readlines()
            for line in lines:
                # Insert a row of data
                line = line.split(',')
                timestamp = line[0]
                level = line[1]
                message = line[2]
                self.db_thread.insert_log(log_id=self.log_id, timestamp=timestamp, level=level, message=message)
                self.log_id += 1

        # Update the last read position
        with open('shared_log_file.txt', 'r', encoding='utf-8') as f:
            self.last_position = f.tell()

    def close(self):
        self.db_thread.close()

event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path='shared_log_file.txt', recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
    event_handler.close()
observer.join()