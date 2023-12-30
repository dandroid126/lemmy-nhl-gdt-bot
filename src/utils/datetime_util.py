from datetime import datetime, timedelta, date
from typing import Optional

import pytz
from dateutil import parser

from src.utils import logger

TAG = "datetime_util"

IDLW = pytz.timezone('Etc/GMT+12')
PT = pytz.timezone('US/Pacific')
MT = pytz.timezone('US/Mountain')
CT = pytz.timezone('US/Central')
ET = pytz.timezone('US/Eastern')
AT = pytz.timezone('Canada/Atlantic')
START_TIME_FORMAT = "%I:%M%p %Z"
START_TIME_FORMAT_NO_TZ = "%I:%M%p"
DATE_FORMAT = '%Y-%m-%d'
DATE_TITLE_FORMAT = '%d %b %Y'
MINUTES_BEFORE_GAME_START_TO_CREATE_POST = 60
MINUTES_AFTER_GAME_END_TO_UPDATE_POST = 60


def is_time_to_make_post(current_time: datetime, game_start_time: datetime, game_end_time: Optional[datetime] = None):
    """
    Check if it is time to make a post based on the current time, the game start time, and the optional game end time.

    Args:
        current_time (datetime): The current time.
        game_start_time (datetime): The start time of the game.
        game_end_time (datetime, optional): The end time of the game. Defaults to None.

    Returns:
        bool: True if it is time to make a post, False otherwise.
    """
    if current_time + timedelta(minutes=MINUTES_BEFORE_GAME_START_TO_CREATE_POST) > game_start_time:
        # Game start time is within bounds to post. Check if the game is over
        if game_end_time is None:
            # if current_time > game_start_time + timedelta(hours=6):
                # Game ended over 6 hours ago. Likely the API gave us bad data and the game is actually over.
                # logger.w(TAG, "Game ended over 6 hours ago. Likely the API gave us bad data and the game is actually over.")
                # return False
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


def get_current_day_as_idlw():
    """
    Get the current day in the IDLW timezone.

    Args:
        None

    Returns:
        str: The current day in the IDLW timezone.

    """
    return datetime.now(tz=IDLW).strftime(DATE_FORMAT)


def get_current_time_as_utc():
    """
    Get the current time in the UTC timezone.

    Args:
        None

    Returns:
        datetime: The current time in the UTC timezone.
    """
    return datetime.now(tz=pytz.utc)


def parse_datetime(datetime_string: str):
    """
    Parse a datetime string into a datetime object.

    Args:
        datetime_string (str): The datetime string to parse.

    Returns:
        datetime: The parsed datetime object.
    """
    return parser.parse(datetime_string)


def get_day_as_title_formatted(day: str):
    """
    Parse a datetime string into the format desired for the daily discussion thread title.

    Args:
        day (str): The datetime string to parse.

    Returns:
        str: The parsed datetime string in the format desired for the daily discussion thread title.
    """
    return parser.parse(day).strftime(DATE_TITLE_FORMAT)


def today():
    """
    Get the current date in the current timezone.
    TODO: revisit this. It may be better to have repeatable timezones.

    Args:
        None

    Returns:
        str: The current date in the current timezone.
    """
    return str(date.today())


def tomorrow():
    """
    Get the tomorrow's date in the current timezone.
    TODO: revisit this. It may be better to have repeatable timezones.

    Args:
        None

    Returns:
        str: Tomorrow's date in the current timezone.
    """
    return str(date.today() + timedelta(days=1))


def yesterday():
    """
    Get the yesterday's date in the current timezone.
    TODO: revisit this. It may be better to have repeatable timezones.

    Args:
        None

    Returns:
        str: Yesterday's date in the current timezone.
    """
    return str(date.today() - timedelta(days=1))


def next_day(start_date: str):
    """
    Get the next day's date in the current timezone.

    Args:
        start_date (str): The start date in the current timezone.

    Returns:
        str: The next day's date in the current timezone.
    """
    # bum bum bum bum ba da bum
    return (parser.parse(start_date) + timedelta(days=1)).strftime(DATE_FORMAT)


def is_same_day(start_time: datetime, day: str):
    """
    Check if the start time is in the same day as the given day.
    # TODO: revisit this. There has to be a better way to do this.

    Args:
        start_time (datetime): The start time.
        day (str): The day to check.

    Returns:
        bool: True if the start time is in the same day as the given day.
    """
    return start_time.astimezone(ET).strftime(DATE_FORMAT) == day
