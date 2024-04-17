from typing import Final
import logger
from logger import Logger
import src.utils.constants as constants

from src.utils.environment_util import environment_util

LOGGER: Final[Logger] = Logger(constants.OUT_PATH, environment_util.log_level, environment_util.log_file_max_mb * logger.MEGABYTE, environment_util.log_file_backup_count, environment_util.error_backup_count)
