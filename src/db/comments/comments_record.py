from dataclasses import dataclass

from src.utils.environment_util import environment_util


@dataclass
class CommentsRecord:
    comment_id: int
    game_id: int

    def get_comment_url(self) -> str:
        return f'{environment_util.lemmy_instance}/comment/{self.comment_id}'
