from typing import Optional

from dotenv import load_dotenv
import os

from src.datatypes.game import GameType
from src.utils import logger

TAG = "EnvironmentUtil"


class EnvironmentUtil:
    def __init__(self, dotenv_path: Optional[str] = None):
        load_dotenv(dotenv_path=dotenv_path, override=True)
        self.bot_name = os.getenv('BOT_NAME')
        self.password = os.getenv('PASSWORD')
        self.lemmy_instance = os.getenv('LEMMY_INSTANCE')
        self.community_name = os.getenv('COMMUNITY_NAME')
        self.comment_post_types = self.parse_game_types(os.getenv('COMMENT_POST_TYPES'))
        self.gdt_post_types = self.parse_game_types(os.getenv('GDT_POST_TYPES'))
        if not self.lemmy_instance.startswith('https://'):
            self.lemmy_instance = f"https://{self.lemmy_instance}"
        logger.i(TAG, "Environment loaded")

    @staticmethod
    def parse_game_types(game_types: str):
        return [GameType[game_type] for game_type in game_types.split(',')]
