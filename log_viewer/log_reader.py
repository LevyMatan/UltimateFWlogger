import subprocess
import re
from logger_db import DatabaseThread
from watchdog.events import FileSystemEventHandler
from datetime import datetime
class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_position = 0
        self.log_id = 0
        self.db_thread = DatabaseThread('logs.db')
        self.db_thread.start()

        # Start the FwDeviceMockup process
        self.process = subprocess.Popen(['./FwDeviceMockup'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

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
        # Read the output from the FwDeviceMockup process
        output = self.process.stdout.readline().decode('utf-8')

        # Parse the output
        match = re.match(r'\[(\w+)\] (.*): (.*)', output)
        if match:
            level = match.group(1)
            source = match.group(2)
            message = match.group(3)

            # Insert a row of data
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.db_thread.insert_log(log_id=self.log_id, timestamp=timestamp, level=level, message=message, source=source)
            self.log_id += 1

    def close(self):
        self.db_thread.close()
        self.process.terminate()