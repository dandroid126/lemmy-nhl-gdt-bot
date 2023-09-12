from datetime import datetime, timedelta, date
from dateutil import parser
import pytz

EST = pytz.timezone('US/Eastern')
START_TIME_FORMAT = "%I:%M%p %Z"
MINUTES_BEFORE_POST = 60


def is_time_to_make_post(current_time, game_start_time):
    return current_time + timedelta(minutes=MINUTES_BEFORE_POST) > game_start_time


def get_current_time_as_utc():
    return datetime.now(tz=pytz.utc)


def parse_datetime(datetime_string: str):
    return parser.parse(datetime_string)


def today():
    return date.today()


def yesterday():
    return date.today() - timedelta(days=1)
