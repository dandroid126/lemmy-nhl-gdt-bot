import logging
from logging.handlers import RotatingFileHandler
import os

from src.utils import constants

if not os.path.exists(constants.OUT_PATH):
    os.makedirs(constants.OUT_PATH)

log_handler = logging.handlers.RotatingFileHandler(f'{constants.OUT_PATH}/log.txt', maxBytes=1 * constants.MEGABYTE,
                                                   backupCount=100)
formatter = logging.Formatter(
    '%(asctime)s nhl-gameday-bot [%(process)d]: %(message)s',
    '%b %d %H:%M:%S')
log_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(log_handler)
logger.setLevel(logging.DEBUG)


def d(tag, text):
    logger.debug(f"[{tag}]\t{text}")


def e(tag, text, error=None):
    logger.error(f"[{tag}]\t{text}\nError:{error}")
