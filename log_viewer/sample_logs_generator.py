'''
Generate logs for testing the log viewer

Two methods:
1) Writing directly to the log db.
2) Writing to a shared log file.
'''

import time
import random
import datetime
import argparse
from dev_interactions import FW_LOG_MODULE_TYPE
from logger_db import DatabaseThread
from log_def import Log
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

    def __init__(self, db_thread, num_of_logs=1000):
        self.db_thread = db_thread
        self.levels = ['INFO', 'WARNING', 'ERROR']
        self.files = ['fileA.c', 'fileB.c', 'fileC.c']
        self.num_of_logs = num_of_logs

    def generate_logs(self):
        """
        Generates a list of logs.

        Returns:
            list: A list of logs, where each log is a tuple containing the log information.
        """
        logs = [tuple] * self.num_of_logs
        for i in range(self.num_of_logs):
            date = datetime.datetime.now()
            level = random.choice(self.levels)
            file = random.choice(self.files)
            line = random.randint(1, 1000)
            src_function_name = f'function_{random.randint(1, 10)}'
            # get a random message from the internet, should be up to 15 words
            message = ' '.join(random.sample(['The', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog', 'at', 'midnight', 'in', 'the', 'forest'], random.randint(1, 5)))
            log_group = random.choice(list(FW_LOG_MODULE_TYPE))  # Choose a random log group
            print(log_group)
            logs[i] = (date, file, line, src_function_name, level, log_group, message)  # Add the log group to the log tuple
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
            self.db_thread.insert_log(log[0], log[1], log[2], log[3], log[4], log[5], log[6])
            delay = random.uniform(0, 0.01)
            time.sleep(delay)
        self.db_thread.close()

    def write_to_shared_log_file(self):
        """
        Writes generated logs to a shared log file.

        This method generates logs using the `generate_logs` method and appends them to a shared log file named 'shared_log_file.txt'.
        Each log entry is written in the format: '<log[0]>,<log[1]>,<log[2]>\n'.
        The method also introduces a random delay between writing each log entry, ranging from 0 to 0.5 seconds.

        Parameters:
            None

        Returns:
            None
        """
        for log in self.generate_logs():
            with open('shared_log_file.txt', 'a', encoding='utf-8') as f:
                f.write(f'{log[0]},{log[1]},{log[2]},{log[3]},{log[4]},{log[5]}\n')
            delay = random.uniform(0, 0.01)
            time.sleep(delay)

    def slow_log_gen(self, num_of_logs=1000, max_delay=1):
        """
        Generate logs with a delay between each log.

        This method generates logs with a delay between each log entry. The delay is a random value between 0 and `max_delay` mili-sconds.

        Parameters:
            num_of_logs (int): The number of logs to generate.
            max_delay (int): The maximum delay between each log entry.

        Returns:
            None
        """
        for i in range(num_of_logs):
            date = datetime.datetime.now()
            level = random.choice(self.levels)
            file = random.choice(self.files)
            line = random.randint(1, 1000)
            src_function_name = f'function_{random.randint(1, 10)}'
            message = ' '.join(random.sample(['The', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog', 'at', 'midnight', 'in', 'the', 'forest'], random.randint(1, 5)))
            log_group = random.choice(list(FW_LOG_MODULE_TYPE)).name # Choose a random log group
            log = Log(date, file, line, src_function_name, level, log_group, message)
            self.db_thread.insert_log(log)
            delay = random.uniform(0, max_delay) / 1000
            time.sleep(delay)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Generate logs.')
    parser.add_argument('--write_to', default='sql_db', choices=['txt_log_file', 'sql_db'], help='Destination of writing logs')
    parser.add_argument('--num_of_logs', type=int, default=1000, help='Number of logs to generate')

    args = parser.parse_args()
    print(f'numm_of_logs: {args.num_of_logs}')

    db_thread = DatabaseThread('logs.db')
    log_generator = LogGenerator(db_thread, num_of_logs=args.num_of_logs)
    if args.write_to == 'sql_db':
        log_generator.write_logs_to_db()
    elif args.write_to == 'txt_log_file':
        log_generator.write_to_shared_log_file()

    db_thread.close()