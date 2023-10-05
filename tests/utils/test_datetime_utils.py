import unittest
from datetime import datetime, timedelta

from src.utils import datetime_util


class TestDatetimeUtils(unittest.TestCase):
    def test_is_time_to_make_post_too_early_start_no_end(self):
        current_time = datetime.now()
        start_time = current_time + timedelta(minutes=datetime_util.MINUTES_BEFORE_GAME_START_TO_CREATE_POST + 1)
        self.assertFalse(datetime_util.is_time_to_make_post(current_time, start_time))

    def test_is_time_to_make_post_equal_start_no_end(self):
        current_time = datetime.now()
        start_time = current_time + timedelta(minutes=datetime_util.MINUTES_BEFORE_GAME_START_TO_CREATE_POST)
        self.assertFalse(datetime_util.is_time_to_make_post(current_time, start_time))

    def test_is_time_to_make_post_game_running(self):
        current_time = datetime.now()
        start_time = current_time - timedelta(hours=1)
        self.assertTrue(datetime_util.is_time_to_make_post(current_time, start_time))

    def test_is_time_to_make_post_game_recently_ended(self):
        current_time = datetime.now()
        start_time = current_time - timedelta(hours=3)
        end_time = current_time - timedelta(minutes=datetime_util.MINUTES_AFTER_GAME_END_TO_UPDATE_POST - 1)
        self.assertTrue(datetime_util.is_time_to_make_post(current_time, start_time, end_time))

    def test_is_time_to_make_post_too_late_end(self):
        current_time = datetime.now()
        start_time = current_time - timedelta(hours=5)
        end_time = current_time - timedelta(minutes=datetime_util.MINUTES_AFTER_GAME_END_TO_UPDATE_POST + 1)
        self.assertFalse(datetime_util.is_time_to_make_post(current_time, start_time, end_time))

    def test_bad_api_data_no_end_time(self):
        current_time = datetime.now()
        start_time = current_time - timedelta(hours=6, minutes=1)
        self.assertFalse(datetime_util.is_time_to_make_post(current_time, start_time))

    def test_is_time_to_make_post_equal_end(self):
        current_time = datetime.now()
        start_time = current_time + timedelta(hours=3)
        end_time = current_time
        self.assertFalse(datetime_util.is_time_to_make_post(current_time, start_time, end_time))

    def test_next_day(self):
        today = datetime_util.today()
        tomorrow = datetime_util.tomorrow()
        self.assertEqual(datetime_util.next_day(today), tomorrow)


if __name__ == '__main__':
    unittest.main()
