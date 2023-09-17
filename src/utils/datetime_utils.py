from datetime import datetime, timedelta, date
from dateutil import parser
import pytz

EST = pytz.timezone('US/Eastern')
START_TIME_FORMAT = "%I:%M%p %Z"
MINUTES_BEFORE_GAME_START_TO_CREATE_POST = 60
MINUTES_AFTER_GAME_END_TO_UPDATE_POST = 60


def is_time_to_make_post(current_time, game_start_time, game_end_time=None):
    if current_time + timedelta(minutes=MINUTES_BEFORE_GAME_START_TO_CREATE_POST) > game_start_time:
        # Game start time is within bounds to post. Check if the game is over
        if game_end_time is None:
            # Game hasn't ended. Either the game is about to start or is currently running.
            return True
        if current_time - timedelta(minutes=MINUTES_AFTER_GAME_END_TO_UPDATE_POST) > game_end_time:
            # Game ended a long time ago. Don't update the post.
            return False
        # Game ended not too long ago. Keep updating the post for a while to get updated stats
        return True
    # Game isn't going to start for a long time. Don't create the post yet
    return False


def get_current_time_as_utc():
    return datetime.now(tz=pytz.utc)


def parse_datetime(datetime_string: str):
    return parser.parse(datetime_string)


def today():
    return date.today()


def yesterday():
    return date.today() - timedelta(days=1)
