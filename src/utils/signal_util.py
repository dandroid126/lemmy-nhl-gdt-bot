import signal
import threading

TAG = "signal_util"


class SignalUtil:
    """
    Utility class for handling signals such as SIGINT and SIGTERM.
    """
    is_interrupted = False
    condition = threading.Condition()

    def __init__(self):
        """
        Initialize the SignalUtil
        """

        # Register the interrupt function for SIGINT and SIGTERM
        signal.signal(signal.SIGINT, self.interrupt)
        signal.signal(signal.SIGTERM, self.interrupt)

    def interrupt(self, *args):
        """
        Handle interruptions of the program to release resources and exit gracefully

        Args:
            *args: The arguments.

        Returns:
            None
        """
        self.is_interrupted = True
        from src.utils import logger
        logger.i(TAG, f"interrupt(): interrupted. args: {args}")
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()

    def wait(self, timeout: float):
        """
        Wait function that allows for the program to gracefully exit if interrupted. Use this function in the main loop instead of time.sleep().

        Args:
            timeout: The amount of time to wait in seconds

        Returns:

        """
        self.condition.acquire()
        self.condition.wait(timeout)
        self.condition.release()


# Initialize the SignalUtil instance to be used globally
signal_util = SignalUtil()
