from datetime import datetime, timedelta, date

import pytz
from dateutil import parser

from src.utils import logger

TAG = "datetime_util"

PT = pytz.timezone('US/Pacific')
MT = pytz.timezone('US/Mountain')
CT = pytz.timezone('US/Central')
ET = pytz.timezone('US/Eastern')
AT = pytz.timezone('Canada/Atlantic')
START_TIME_FORMAT = "%I:%M%p %Z"
START_TIME_FORMAT_NO_TZ = "%I:%M%p"
DATE_FORMAT = '%Y-%m-%d'
MINUTES_BEFORE_GAME_START_TO_CREATE_POST = 60
MINUTES_AFTER_GAME_END_TO_UPDATE_POST = 60


def is_time_to_make_post(current_time, game_start_time, game_end_time=None):
    if current_time + timedelta(minutes=MINUTES_BEFORE_GAME_START_TO_CREATE_POST) > game_start_time:
        # Game start time is within bounds to post. Check if the game is over
        if game_end_time is None:
            if current_time > game_start_time + timedelta(hours=6):
                # Game ended over 6 hours ago. Likely the API gave us bad data and the game is actually over.
                logger.w(TAG, "Game ended over 6 hours ago. Likely the API gave us bad data and the game is actually over.")
                return False
            # Game hasn't ended. Either the game is about to start or is currently running.
            logger.i(TAG, "Game hasn't ended. Either the game is about to start or is currently running.")
            return True
        if current_time - timedelta(minutes=MINUTES_AFTER_GAME_END_TO_UPDATE_POST) > game_end_time:
            # Game ended a long time ago. Don't update the post.
            logger.i(TAG, "Game ended a long time ago. Don't update the post.")
            return False
        # Game ended not too long ago. Keep updating the post for a while to get updated stats
        logger.i(TAG, "Game ended not too long ago. Keep updating the post for a while to get updated stats")
        return True
    # Game isn't going to start for a long time. Don't create the post yet
    logger.i(TAG, "Game isn't going to start for a long time. Don't create the post yet")
    return False


def get_current_time_as_utc():
    return datetime.now(tz=pytz.utc)


def parse_datetime(datetime_string: str):
    return parser.parse(datetime_string)


def today():
    return str(date.today())


def tomorrow():
    return str(date.today() + timedelta(days=1))


def yesterday():
    return str(date.today() - timedelta(days=1))


def next_day(start_date: str):
    # bum bum bum bum ba da bum
    return (parser.parse(start_date) + timedelta(days=1)).strftime(DATE_FORMAT)
