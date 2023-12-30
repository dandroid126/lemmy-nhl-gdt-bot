from dataclasses import dataclass

from src.utils.environment_util import environment_util


@dataclass
class GameDayThreadRecord:
    post_id: int
    game_id: int

    def get_game_day_thread_url(self) -> str:
        """
        Returns the URL for the game day thread post.

        Returns:
            str: The URL for the game day thread post.
        """
        # Generate the URL by combining the lemmy_instance and post_id
        return f'{environment_util.lemmy_instance}/post/{self.post_id}'
