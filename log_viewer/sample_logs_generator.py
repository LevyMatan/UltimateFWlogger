'''
Generate logs for testing the log viewer

Two methods:
1) Writing directly to the log db.
2) Writing to a shared log file.
'''

import time
import random
import datetime

from logger_db import DatabaseThread

class LogGenerator:
    """
    LogGenerator class is responsible for generating and writing logs.

    Attributes:
        db_thread (Thread): The thread used for database operations.
        levels (list): The list of log levels.
        files (list): The list of file names.

    Methods:
        generate_logs(): Generates a list of logs.
        write_logs_to_db(): Writes logs to the database.
        write_to_shared_log_file(): Writes logs to a shared log file.
    """

    def __init__(self, db_thread):
        self.db_thread = db_thread
        self.levels = ['INFO', 'WARNING', 'ERROR']
        self.files = ['fileA.c', 'fileB.c', 'fileC.c']

    def generate_logs(self):
        """
        Generates a list of logs.

        Returns:
            list: A list of logs, where each log is a tuple containing the log information.
        """
        logs = [tuple] * 100
        for i in range(100):
            date = datetime.datetime.now()
            level = random.choice(self.levels)
            file = random.choice(self.files)
            line = random.randint(1, 1000)
            message = f'This is a {level} message from {file} at {date}'
            logs[i] = (date, file, line, level, message)
        return logs

    def write_logs_to_db(self):
        """
        Writes logs to the database.

        This method starts a database thread, generates logs, and inserts them into the database.
        Each log is inserted with a delay of 1 second between each insertion.

        Returns:
            None
        """
        self.db_thread.start()
        for log in self.generate_logs():
            self.db_thread.insert_log(log[0], log[1], log[2], log[3], log[4])
            time.sleep(1)
        self.db_thread.close()

    def write_to_shared_log_file(self):
        """
        Writes generated logs to a shared log file.

        This method generates logs using the `generate_logs` method and appends them to a shared log file named 'shared_log_file.txt'.
        Each log entry is written in the format: '<log[0]>,<log[1]>,<log[2]>\n'.
        The method also introduces a 1-second delay between writing each log entry.

        Parameters:
            None

        Returns:
            None
        """
        for log in self.generate_logs():
            with open('shared_log_file.txt', 'a', encoding='utf-8') as f:
                f.write(f'{log[0]},{log[1]},{log[2]},{log[3]},{log[4]}\n')
            time.sleep(1)


if __name__ == '__main__':
    db_thread = DatabaseThread('logs.db')
    log_generator = LogGenerator(db_thread)
    log_generator.write_logs_to_db()
    log_generator.write_to_shared_log_file()
    db_thread.close()