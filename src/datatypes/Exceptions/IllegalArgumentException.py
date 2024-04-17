from src.utils.log_util import LOGGER


class IllegalArgumentException(Exception):
    def __init__(self, tag, message):
        """
        Initialize the class with a tag and message.

        Args:
        - tag (str): The tag for the log message.
        - message (str): The log message.

        Returns:
        None
        """
        self.message = message
        LOGGER.e(tag, self.message)
        super().__init__(message)
