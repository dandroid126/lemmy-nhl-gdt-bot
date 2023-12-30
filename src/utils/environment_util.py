from typing import Optional

from dotenv import load_dotenv
import os

from src.datatypes.teams import Teams, Team
from src.datatypes.game import GameType
from src.utils import logger

TAG = "EnvironmentUtil"


class EnvironmentUtil:
    _BOT_NAME = 'BOT_NAME'
    _PASSWORD = 'PASSWORD'
    _LEMMY_INSTANCE = 'LEMMY_INSTANCE'
    _COMMUNITY_NAME = 'COMMUNITY_NAME'
    _COMMENT_POST_TYPES = 'COMMENT_POST_TYPES'
    _GDT_POST_TYPES = 'GDT_POST_TYPES'
    _TEAMS = 'TEAMS'
    _ENVIRONMENT_VARIABLE_NAMES = [_BOT_NAME, _PASSWORD, _LEMMY_INSTANCE, _COMMUNITY_NAME, _COMMENT_POST_TYPES, _GDT_POST_TYPES, _TEAMS]

    def __init__(self, dotenv_path: Optional[str] = None):
        """
        Load the environment variables from the .env file.

        Args:
            dotenv_path: The path to the .env file.

        Returns:
            None
        """
        for environment_variable_name in self._ENVIRONMENT_VARIABLE_NAMES:
            if os.environ.get(environment_variable_name):
                del os.environ[environment_variable_name]
        load_dotenv(dotenv_path=dotenv_path)
        self.bot_name = os.getenv(self._BOT_NAME)
        self.password = os.getenv(self._PASSWORD)
        self.lemmy_instance = os.getenv(self._LEMMY_INSTANCE)
        self.community_name = os.getenv(self._COMMUNITY_NAME)
        self.comment_post_types = self.parse_game_types(os.getenv(self._COMMENT_POST_TYPES))
        self.gdt_post_types = self.parse_game_types(os.getenv(self._GDT_POST_TYPES))
        self.teams = self.parse_teams(os.getenv(self._TEAMS))
        if not self.lemmy_instance.startswith('https://'):
            self.lemmy_instance = f"https://{self.lemmy_instance}"
        logger.i(TAG, "Environment loaded")

    @staticmethod
    def parse_game_types(game_types: str):
        """
        Parse the game types from the environment variable.

        Args:
            game_types: The game types to parse.

        Returns:
            The parsed game types.
        """
        if not game_types:
            return []
        return [GameType[game_type] for game_type in game_types.split(',')]

    @staticmethod
    def parse_teams(teams: str) -> list[Team]:
        """
        Parse the teams from the environment variable.

        Args:
            teams: The teams to parse.

        Returns:
            The parsed teams.
        """
        if teams:
            return [Teams[team].value for team in teams.split(',')]
        else:
            return Teams.get_all_teams()


# Set the environment_util instance to be used globally
environment_util = EnvironmentUtil()
