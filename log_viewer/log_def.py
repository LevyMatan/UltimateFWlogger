"""
This module defines the Log class, which represents a log entry in the database.

The Log class provides attributes and methods to store and manipulate log entries.

Example usage:
    # Create a new log entry
    log = Log(123456789, 'example.py', 42, 'example_function', 'INFO', FW_LOG_MODULE_TYPE.LOG_MOD_FDB, 'This is an example log message.')
    print(log)
    print(log.to_dict())
"""

from sqlalchemy import Column, Integer, String, Enum, Sequence
from sqlalchemy.orm import declarative_base
from dev_interactions import FW_LOG_MODULE_TYPE

Base = declarative_base()

class Log(Base):
    """
    Represents a log entry in the database.

    Attributes:
        id (int): The unique identifier of the log entry.
        timestamp (str): The timestamp of when the log entry was created.
        file (str): The file name associated with the log entry.
        line (int): The line number in the file where the log entry occurred.
        src_function_name (str): The name of the function where the log entry occurred.
        level (str): The log level of the entry (e.g., INFO, WARNING, ERROR).
        log_group (str): The log group of the entry (e.g., FW_LOG_MODULE_TYPE).
        msg (str): The log message.
    """
    __tablename__ = 'logs'

    id = Column(Integer, Sequence('log_id_seq'), primary_key=True)
    timestamp = Column(Integer)
    file = Column(String)
    line = Column(Integer)
    src_function_name = Column(String)
    level = Column(String)
    log_group = Column(Enum(FW_LOG_MODULE_TYPE))
    msg = Column(String)

    def __init__(self, timestamp, file, line, src_function_name, level, log_group, msg):
        """
        Initializes a log entry object.

        Args:
            timestamp (str): The timestamp of when the log entry was created.
            file (str): The file name associated with the log entry.
            line (int): The line number in the file where the log entry occurred.
            src_function_name (str): The name of the function where the log entry occurred.
            level (str): The log level of the entry (e.g., INFO, WARNING, ERROR).
            log_group (str): The log group of the entry (e.g., FW_LOG_MODULE_TYPE).
            msg (str): The log message.
        """
        self.timestamp = timestamp
        self.file = file
        self.line = line
        self.src_function_name = src_function_name
        self.level = level
        self.log_group = log_group
        self.msg = msg

    def __repr__(self):
        """
        Returns a string representation of the log entry object.

        Returns:
            str: A string representation of the log entry object.
        """
        return f"<Log(id={self.id}, timestamp={self.timestamp}, file={self.file}, line={self.line}, src_function_name={self.src_function_name}, level={self.level}, log_group={self.log_group}, msg={self.msg})>"

    def to_dict(self):
        """
        Converts the log entry object to a dictionary.

        Returns:
            dict: A dictionary representation of the log entry object.
        """
        log_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        log_dict['file_line'] = f"{log_dict['file']}:{log_dict['line']}"
        log_dict['log_group'] = log_dict['log_group'].name
        return log_dict


if __name__ == '__main__':
    # Create a new log entry
    log = Log(123456789, 'example.py', 42, 'example_function', 'INFO', FW_LOG_MODULE_TYPE.LOG_MOD_FDB, 'This is an example log message.')
    print(log)
    print(log.to_dict())
