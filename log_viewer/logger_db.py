from sqlalchemy import create_engine, Column, String, Integer, Sequence, Enum
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base
import threading
import datetime
import random
import logging
from dev_interactions import FW_LOG_MODULE_TYPE  # Import the enum
from log_def import Log, Base  # Import the Log class


class DatabaseThread(threading.Thread):
    def __init__(self, db_name):
        threading.Thread.__init__(self)
        self.engine = create_engine('sqlite:///' + db_name)
        Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        self.session = Session()

        # If log db is not empty, get the last read id
        inspector = inspect(self.engine)
        table_names = inspector.get_table_names()
        if 'logs' in table_names:
            self.log_id = 0
            if self.session.query(Log).count() > 0:
                self.log_id = self.session.query(Log).order_by(Log.id.desc()).first().id
                self.log_id += 1
        self.last_read_id = 0
        self.query = self.session.query(Log)

    def insert_log(self, log):

        self.session.add(log)
        self.session.commit()

        # Check if total logs is greater than 20000
        total_logs = self.session.query(Log).count()
        if total_logs > 20000:
            # Get the first 10000 logs
            logs_to_delete = self.session.query(Log).order_by(asc(Log.id)).limit(10000)
            for log in logs_to_delete:
                self.session.delete(log)
            self.session.commit()

    def set_logs_filter(self, attribute, value, operator='=='):
        """
        Set the filter for the logs.

        Args:
            attribute (str): The attribute to filter on: 'level', 'file', 'src_function_name'.
            value (str): The value to filter on.
            operator (str): The operator to use for the filter (e.g., '==', '!=').

        Returns:
            None
        """
        if operator == '==':
            self.query = self.query.filter(getattr(Log, attribute).like('%' + value + '%'))
        elif operator == '!=':
            self.query = self.query.filter(getattr(Log, attribute) != value)


    def get_all_logs(self):
            """
            Retrieve all logs from the database.

            Returns:
                A list of Log objects representing all the logs in the database.
            """
            return self.query.all()

    def get_new_logs(self):
        """
        Retrieves new logs from the database.

        If self.last_read_id is None, retrieves all logs.
        Otherwise, retrieves logs with an id greater than self.last_read_id.

        Returns:
            A list of Log objects representing the new logs.
        """
        if self.last_read_id is None:
            logs = self.session.query(Log).all()
            logging.debug(f"Retrieved all logs: {logs}")
        else:
            logs = self.session.query(Log).filter(Log.id > self.last_read_id).all()
            logging.debug(f"Retrieved logs with id greater than {self.last_read_id}: {logs}")

        if logs:
            self.last_read_id = logs[-1].id

        return logs

    def close(self):
        self.session.close()
