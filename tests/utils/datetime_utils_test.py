import unittest
from datetime import datetime, timedelta
from src.utils import datetime_utils


class TestDatetimeUtils(unittest.TestCase):
    def test_is_time_to_make_post_greater_than(self):
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=datetime_utils.MINUTES_BEFORE_POST - 1)
        self.assertTrue(datetime_utils.is_time_to_make_post(start_time, end_time))

    def test_is_time_to_make_post_equal(self):
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=datetime_utils.MINUTES_BEFORE_POST)
        self.assertFalse(datetime_utils.is_time_to_make_post(start_time, end_time))

    def test_is_time_to_make_post_less_than(self):
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=datetime_utils.MINUTES_BEFORE_POST + 1)
        self.assertFalse(datetime_utils.is_time_to_make_post(start_time, end_time))


if __name__ == '__main__':
    unittest.main()
