from typing import Optional

from dotenv import load_dotenv
import os

from src.datatypes.teams import Teams, Team
from src.datatypes.game import GameType
from src.utils import logger

TAG = "EnvironmentUtil"


class EnvironmentUtil:
    __BOT_NAME = 'BOT_NAME'
    __PASSWORD = 'PASSWORD'
    __LEMMY_INSTANCE = 'LEMMY_INSTANCE'
    __COMMUNITY_NAME = 'COMMUNITY_NAME'
    __COMMENT_POST_TYPES = 'COMMENT_POST_TYPES'
    __GDT_POST_TYPES = 'GDT_POST_TYPES'
    __TEAMS = 'TEAMS'
    __ENVIRONMENT_VARIABLE_NAMES = [__BOT_NAME, __PASSWORD, __LEMMY_INSTANCE, __COMMUNITY_NAME, __COMMENT_POST_TYPES, __GDT_POST_TYPES, __TEAMS]

    def __init__(self, dotenv_path: Optional[str] = None):
        for environment_variable_name in self.__ENVIRONMENT_VARIABLE_NAMES:
            if os.environ.get(environment_variable_name):
                del os.environ[environment_variable_name]
        load_dotenv(dotenv_path=dotenv_path)
        self.bot_name = os.getenv(self.__BOT_NAME)
        self.password = os.getenv(self.__PASSWORD)
        self.lemmy_instance = os.getenv(self.__LEMMY_INSTANCE)
        self.community_name = os.getenv(self.__COMMUNITY_NAME)
        self.comment_post_types = self.parse_game_types(os.getenv(self.__COMMENT_POST_TYPES))
        self.gdt_post_types = self.parse_game_types(os.getenv(self.__GDT_POST_TYPES))
        self.teams = self.parse_teams(os.getenv(self.__TEAMS))
        if not self.lemmy_instance.startswith('https://'):
            self.lemmy_instance = f"https://{self.lemmy_instance}"
        logger.i(TAG, "Environment loaded")

    @staticmethod
    def parse_game_types(game_types: str):
        if not game_types:
            return []
        return [GameType[game_type] for game_type in game_types.split(',')]

    @staticmethod
    def parse_teams(teams: str) -> list[Team]:
        if teams:
            return [Teams[team].value for team in teams.split(',')]
        else:
            return Teams.get_all_teams()
