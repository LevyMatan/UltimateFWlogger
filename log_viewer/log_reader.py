'''
log_reader.py is a Python script that reads the output from a subprocess and processes it into log entries.
It uses the Log class from log_def.py to represent log entries and the DatabaseThread class from logger_db.py to interact with the database.
Currently only a specific process is supported and it is hardcoded in the script.
The script reads the output from the subprocess, parses the log entries, and inserts them into a database.

Example usage:
    log_reader = LogReader()
    # Do something
    log_reader.close()

'''

import subprocess
from datetime import datetime
import threading
import re
from logger_db import DatabaseThread
from log_def import Log

class LogReader():
    """
    The LogReader class reads the output from a subprocess and processes it into log entries.

    It reads the output from a subprocess, parses the log entries, and inserts them into a database.

    Attributes:
        last_position (int): The last position read from the output.
        db_thread (DatabaseThread): The thread responsible for interacting with the database.
        process (subprocess.Popen): The subprocess that generates the log output.
        output_thread (threading.Thread): The thread responsible for reading the output from the subprocess.

    Methods:
        __init__(): Initializes the LogReader object.
        read_output(): Reads the output from the subprocess and processes it.
        process_output(output): Processes a single line of output and inserts it into the database.
        close(): Closes the LogReader object and terminates the subprocess.
    """

    def __init__(self):
        """
        Initializes the LogReader object.

        This method initializes the LogReader object by setting the initial values for the attributes,
        starting the database thread, starting the subprocess, and starting the output thread.

        Returns:
            None
        """
        self.last_position = 0
        self.db_thread = DatabaseThread('logs.db')
        self.db_thread.start()

        # Start the FwDeviceMockup process
        self.process = subprocess.Popen(['/Users/matanlevy/GitHub/UltimateFWlogger/build/standalone/FwDeviceMockup'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # Start a thread to read the output
        self.output_thread = threading.Thread(target=self.read_output)
        self.output_thread.start()

    def read_output(self):
        """
        Reads the output from the subprocess and processes it.

        This method continuously reads the output from the subprocess and calls the process_output method
        to process each line of output.

        Returns:
            None
        """
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
        Processes a single line of output and inserts it into the database.

        This method parses a single line of output into timestamp, level, file, line, source function name,
        and message. It then creates a Log object and inserts it into the database using the db_thread.

        Args:
            output (str): The line of output to process.

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
        """
        Closes the LogReader object and terminates the subprocess.

        This method closes the LogReader object by closing the db_thread and terminating the subprocess.

        Returns:
            None
        """
        self.db_thread.close()
        self.process.terminate()


if __name__ == '__main__':
    log_reader = LogReader()
