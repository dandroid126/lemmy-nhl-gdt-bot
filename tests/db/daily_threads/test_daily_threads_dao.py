import os
import random
import sys
import unittest
import uuid

import test_constants
from src.db.daily_threads.daily_threads_dao import DailyThreadsDao
from src.db.db_manager import DbManager
from src.utils import datetime_util


class TestDailyThreadsDao(unittest.TestCase):
    def setUp(self):
        if os.path.exists(test_constants.TEST_DB_PATH):
            os.remove(test_constants.TEST_DB_PATH)
        else:
            print("test.db doesn't exist. Skipping deleting it.")
        db_manager = DbManager(test_constants.TEST_DB_PATH)
        self.daily_threads_dao = DailyThreadsDao(db_manager)

    def test_get_most_recent_daily_thread(self):
        random.seed(str(uuid.uuid4()))
        yesterday_post_id = random.randint(0, sys.maxsize)
        today_post_id = random.randint(0, sys.maxsize)
        tomorrow_post_id = random.randint(0, sys.maxsize)
        yesterday = datetime_util.yesterday()
        today = datetime_util.today()
        tomorrow = datetime_util.tomorrow()
        self.daily_threads_dao.insert_daily_thread(yesterday_post_id, yesterday)
        self.daily_threads_dao.insert_daily_thread(today_post_id, today)
        self.daily_threads_dao.insert_daily_thread(tomorrow_post_id, tomorrow)
        self.assertEqual(self.daily_threads_dao.get_most_recent_daily_thread().date, tomorrow)


if __name__ == '__main__':
    unittest.main()
