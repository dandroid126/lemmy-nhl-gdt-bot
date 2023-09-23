import logging
import sys
from logging.handlers import RotatingFileHandler
import os

from src.utils import constants


# https://stackoverflow.com/questions/19425736/how-to-redirect-stdout-and-stderr-to-logger-in-python
class StreamToLogger(object):
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            if not buf == "^":
                self.logger.log(self.level, line.rstrip())

    def flush(self):
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


def d(tag, text):
    logger.debug(f"[{tag}]\t{text}")


def i(tag, text):
    logger.info(f"[{tag}]\t{text}")


def w(tag, text):
    logger.warning(f"[{tag}]\t{text}")


def e(tag, text, error=None):
    logger.error(f"[{tag}]\t{text}\nError:{error}")
