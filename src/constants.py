import os
from typing import Final
import pytz

SCRIPT_PATH: Final = os.path.realpath(__file__)
DIR_PATH: Final = f"{os.path.dirname(SCRIPT_PATH)}/../"
OUT_PATH: Final = f"{DIR_PATH}/out/"
DB_PATH: Final = f"{OUT_PATH}/gdt_bot.db"

MEGABYTE: Final = 1024 * 1024

EST = pytz.timezone('US/Eastern')
START_TIME_FORMAT = "%I:%M%p %Z"
