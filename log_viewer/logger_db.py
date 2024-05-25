from sqlalchemy import create_engine, inspect, asc, text
from sqlalchemy.orm import sessionmaker
import threading
import logging
from log_def import Log, Base  # Import the Log class
import time

class DatabaseThread(threading.Thread):
    def __init__(self, db_name):
        threading.Thread.__init__(self)
        self._lock = threading.Lock()
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

        # # Check if total logs is greater than 20000
        # total_logs = self.session.query(Log).count()
        # if total_logs > 20000:
        #     # Get the first 10000 logs
        #     logs_to_delete = self.session.query(Log).order_by(asc(Log.id)).limit(10000)
        #     for log in logs_to_delete:
        #         self.session.delete(log)
        #     self.session.commit()

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
        while not self.session.is_active:
            logging.debug("Waiting for session to become active...")
            time.sleep(1)  # Wait for 1 second

        if self.last_read_id is None:
            logs = self.session.query(Log).all()
            logging.debug(f"Retrieved all logs: {logs}")
        else:
            logs = self.session.query(Log).filter(Log.id > self.last_read_id).all()
            logging.debug(f"Retrieved logs with id greater than {self.last_read_id}: {logs}")

        if logs:
            self.last_read_id = logs[-1].id

        return logs

    def clear_logs(self):
        """
        Clear all logs from the database.

        Returns:
            None
        """
        self.session.query(Log).delete()
        self.session.commit()

    def filter_logs(self, column_name, filter_value):
        """
        Filters logs based on the specified column name and filter value.

        Args:
            column_name (str): The name of the column to filter on.
            filter_value: The value to filter for in the specified column.

        Returns:
            list: A list of logs that match the filter criteria.
        """
        with self._lock:
            stmt = text(f"SELECT * FROM logs WHERE {column_name} = :filter_value")
            logs = self.session.query(Log).from_statement(stmt).params(filter_value=filter_value).all()
        return logs

    def close(self):
        self.session.close()
