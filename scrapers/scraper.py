import requests
import time

from datetime import datetime

from db import get_connection


class WebScraper(object):
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def incr(self):
        self.new_records += 1

    def execute(self):
        self.execution_time = datetime.now()
        self.start_time = time.time()
        self.new_records = 0

    def save_log(self):
        query = 'INSERT INTO logs (execution_date, new_records, execution_time, execution_code, agent_id) VALUES ' \
                '(%s, %s, %s, %s, %s);'

        self.cursor.execute(query, (self.execution_time, self.new_records, time.time() - self.start_time, 0,
                                    self.agent_id))
        self.conn.commit()


def log_decorator(func):
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        self.save_log()
        self.conn.close()
    return wrapper
