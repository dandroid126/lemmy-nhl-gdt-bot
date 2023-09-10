from src.logger import logger


class IllegalArgumentException(Exception):
    def __init__(self, tag, message):
        self.message = message
        logger.e(tag, self.message)
        super().__init__(message)
