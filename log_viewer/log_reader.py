import subprocess
import re
from logger_db import DatabaseThread
from datetime import datetime
from log_def import Log
import threading
class LogReader():
    def __init__(self):
        self.last_position = 0
        self.db_thread = DatabaseThread('logs.db')
        self.db_thread.start()

        # Start the FwDeviceMockup process
        self.process = subprocess.Popen(['/Users/matanlevy/GitHub/UltimateFWlogger/build/standalone/FwDeviceMockup'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # Start a thread to read the output
        self.output_thread = threading.Thread(target=self.read_output)
        self.output_thread.start()

    def read_output(self):
        while True:
            # Read a line of output
            output = self.process.stdout.readline().decode('utf-8')

            # If the line is empty and the process has ended, break the loop
            if output == '' and self.process.poll() is not None:
                break

            # Process the output
            self.process_output(output)

    def process_output(self, output):
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
        # Parse the output
        match = re.match(r'\[(\w+)\] (.*):(\d+):(\w+): (.*)', output)
        if match:
            level = match.group(1)
            file = match.group(2)
            line = match.group(3)
            src_function_name = match.group(4)
            message = match.group(5)

            # Insert a row of data
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log = Log(timestamp=timestamp, level=level, msg=message, src_function_name=src_function_name, file=file, line=line, log_group='LOG_MOD_INIT')
            self.db_thread.insert_log(log)

    def close(self):
        self.db_thread.close()
        self.process.terminate()




if __name__ == '__main__':
    log_reader = LogReader()
