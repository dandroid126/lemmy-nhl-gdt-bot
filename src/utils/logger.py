import logging
import sys
from logging.handlers import RotatingFileHandler
import os

from src.utils import constants

# Shamelessly borrowed this idea from this link:
# https://stackoverflow.com/questions/19425736/how-to-redirect-stdout-and-stderr-to-logger-in-python
class StreamToLogger(object):
    def __init__(self, logger: logging.Logger, level: int = logging.INFO):
        """
        Initialize a new instance of the StreamToLogger class.

        Args:
            logger (logging.Logger): The logger to use.
            level (int): The logging level to use. Defaults to logging.INFO.

        Returns:
            None
        """
        self.logger = logger
        self.level = level
        self.linebuf = ''

    def write(self, buf: str):
        """
        Write the buffer to the logger.

        Args:
            buf (str): The buffer to write.

        Returns:
            None
        """
        for line in buf.rstrip().splitlines():
            if not buf == "^":
                self.logger.log(self.level, line.rstrip())

    def flush(self):
        """
        Do nothing instead of flushing the buffer.

        Returns:
            None
        """
        pass


if not os.path.exists(constants.OUT_PATH):
    os.makedirs(constants.OUT_PATH)

# Logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Formatter
formatter = logging.Formatter(fmt='%(asctime)s nhl-gameday-bot [%(process)d]: [%(levelname)s] %(message)s',
                              datefmt='%b %d %H:%M:%S')

# File Handler
file_handler = logging.handlers.RotatingFileHandler(filename=f'{constants.OUT_PATH}/log.txt',
                                                    maxBytes=1 * constants.MEGABYTE,
                                                    backupCount=20)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# stdout Handler
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.addFilter(lambda record: record.levelno <= logging.WARN)
stdout_handler.setFormatter(formatter)

# stderr Handler
stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.ERROR)
stderr_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)
logger.addHandler(stderr_handler)
sys.stdout = StreamToLogger(logger, logging.INFO)
sys.stderr = StreamToLogger(logger, logging.ERROR)


def d(tag: str, text: str):
    """
    Log a debug message.

    Args:
        tag: The tag of the caller (usually the class or file name).
        text: The message to log.

    Returns:
        None
    """
    logger.debug(f"[{tag}]\t{text}")


def i(tag: str, text: str):
    """
    Log an info message.

    Args:
        tag: The tag of the caller (usually the class or file name).
        text: The message to log.

    Returns:
        None
    """
    logger.info(f"[{tag}]\t{text}")


def w(tag, text):
    """
    Log a warning message.

    Args:
        tag: The tag of the caller (usually the class or file name).
        text: The message to log.

    Returns:
        None
    """
    logger.warning(f"[{tag}]\t{text}")


def e(tag, text, error=None):
    """
    Log an error message.

    Args:
        tag: The tag of the caller (usually the class or file name).
        text: The message to log.
        error: The error to log.

    Returns:
        None
    """
    logger.error(f"[{tag}]\t{text}\nError:{error}")
