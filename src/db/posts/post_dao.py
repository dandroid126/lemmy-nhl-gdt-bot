from typing import Optional

from src.db.db_manager import DbManager
from src.db.posts.post_record import PostType, PostRecord
from src.utils import logger

# Keeping these here for reference, but don't use them because formatted strings in queries are bad.
# TABLE_POSTS = 'posts'
# COLUMN_POST_ID = 'post_id'
# COLUMN_GAME_ID = 'game_id'
# COLUMN_POST_TYPE = 'post_type'

TAG = "PostDao"


class PostDao:
    def __init__(self, db_manager: DbManager):
        self.db_manager = db_manager

    def get_post_id(self, game_id: int):
        query = "SELECT post_id FROM posts WHERE game_id=?"
        params = (game_id,)
        logger.i(TAG, f"get_post_id(): executing {query} with params {params}")
        val = self.db_manager.cursor.execute(query, params).fetchone()
        if val is not None:
            return val[0]
        return None

    def get_post(self, game_id: int) -> Optional[PostRecord]:
        query = "SELECT * FROM posts WHERE game_id=?"
        params = (game_id,)
        logger.i(TAG, f"get_post_id(): executing {query} with params {params}")
        val = self.db_manager.cursor.execute(query, params).fetchone()
        if val is not None:
            return PostRecord(val[0], val[1], PostType(val[2]))
        return None

    def insert_post(self, post_id: int, game_id: int, post_type: PostType):
        query = "INSERT INTO posts VALUES(?, ?, ?)"
        params = (post_id, game_id, post_type.value)
        logger.i(TAG, f"insert_post(): executing {query} with params {params}")
        self.db_manager.cursor.execute(query, params)
        self.db_manager.connection.commit()
        return True
