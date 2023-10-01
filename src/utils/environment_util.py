from dotenv import load_dotenv
import os

from src.utils import logger

TAG = "EnvironmentUtil"


class EnvironmentUtil:
    def __init__(self):
        load_dotenv()
        self.bot_name = os.getenv('BOT_NAME')
        self.password = os.getenv('PASSWORD')
        self.lemmy_instance = os.getenv('LEMMY_INSTANCE')
        self.community_name = os.getenv('COMMUNITY_NAME')
        if not self.lemmy_instance.startswith('https://'):
            self.lemmy_instance = f"https://{self.lemmy_instance}"
        logger.i(TAG, "Environment loaded")
