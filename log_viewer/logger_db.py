from sqlalchemy import create_engine, Column, String, Integer, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base
import threading
import datetime

Base = declarative_base()

class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, Sequence('log_id_seq'), primary_key=True)
    date = Column(String)
    level = Column(String)
    log = Column(String)


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

    def insert_log(self, date, level, log):
        new_log = Log(id=self.log_id, date=date, level=level, log=log)
        self.session.add(new_log)
        self.session.commit()
        self.log_id += 1

    def get_all_logs(self):
        return self.session.query(Log).all()

    def get_new_logs(self):
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
    # logs = db_thread.get_all_logs()
    # for log in logs:
    #     print(log.id, log.date, log.level, log.log)
    db_thread.insert_log(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'INFO', 'This is an info message')
    db_thread.insert_log(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'ERROR', 'This is an error message')
    db_thread.insert_log(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'WARNING', 'This is a warning message')
    logs = db_thread.get_new_logs()
    for log in logs:
        print(log.id, log.date, log.level, log.log)
    db_thread.close()