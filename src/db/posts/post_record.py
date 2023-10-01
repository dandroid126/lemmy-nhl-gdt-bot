from dataclasses import dataclass
from enum import Enum


class PostType(Enum):
    GAME_DAY_THREAD = 1
    DAILY_DISCUSSION_THREAD = 2
    COMMENT = 3


@dataclass
class PostRecord:
    post_id: int
    game_id: int
    post_type: PostType
