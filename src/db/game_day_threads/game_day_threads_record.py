from dataclasses import dataclass

from src.utils.environment_util import environment_util


@dataclass
class GameDayThreadRecord:
    post_id: int
    game_id: int

    def get_game_day_thread_url(self) -> str:
        return f'{environment_util.lemmy_instance}/post/{self.post_id}'
