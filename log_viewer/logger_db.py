from sqlalchemy import create_engine, Column, String, Integer, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base
import threading
import datetime
import random

Base = declarative_base()

class Log(Base):
    """
    Represents a log entry in the database.

    Attributes:
        id (int): The unique identifier of the log entry.
        timestamp (str): The timestamp of when the log entry was created.
        file (str): The file name associated with the log entry.
        line (int): The line number in the file where the log entry occurred.
        level (str): The log level of the entry (e.g., INFO, WARNING, ERROR).
        msg (str): The log message.
    """
    __tablename__ = 'logs'

    id = Column(Integer, Sequence('log_id_seq'), primary_key=True)
    timestamp = Column(Integer)
    file = Column(String)
    line = Column(Integer)
    level = Column(String)
    msg = Column(String)


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

    def insert_log(self, timestamp, file, line, level, msg):
        """
        Inserts a new log entry into the database.

        Args:
            date (datetime): The date and time of the log entry.
            level (str): The log level (e.g., INFO, WARNING, ERROR).
            msg (str): The log message.

        Returns:
            None
        """
        new_log = Log(id=self.log_id, timestamp=timestamp, file=file, line=line, level=level, msg=msg)
        self.session.add(new_log)
        self.session.commit()
        self.log_id += 1

    def get_all_logs(self):
            """
            Retrieve all logs from the database.

            Returns:
                A list of Log objects representing all the logs in the database.
            """
            return self.session.query(Log).all()

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
            else:
                logs = self.session.query(Log).filter(Log.id > self.last_read_id).all()

            if logs:
                self.last_read_id = logs[-1].id

            return logs

    def close(self):
        self.session.close()


if __name__ == '__main__':
    db_thread = DatabaseThread('logs.db')
    db_thread.start()
    db_thread.join()
    db_thread.insert_log(
        timestamp=datetime.datetime.now(),
        file='fileA.c',
        line=random.randint(1,1000),
        level='INFO',
        msg='This is a test log message'
    )
    logs = db_thread.get_new_logs()
    for log in logs:
        print(log.id, log.timestamp, log.level, log.msg)
    db_thread.close()