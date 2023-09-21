import signal
import threading

TAG = "signal_util"


class SignalUtil:
    is_interrupted = False
    condition = threading.Condition()

    def __init__(self):
        signal.signal(signal.SIGINT, self.interrupt)
        signal.signal(signal.SIGTERM, self.interrupt)

    def interrupt(self, *args):
        self.is_interrupted = True
        from src.utils import logger
        logger.i(TAG, f"interrupted. args: {args}")
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()

    def wait(self, timeout):
        self.condition.acquire()
        self.condition.wait(timeout)
        self.condition.release()
