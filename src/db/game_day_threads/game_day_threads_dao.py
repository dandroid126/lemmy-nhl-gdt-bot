from typing import Optional

from src.db.db_manager import DbManager, db_manager
from src.db.game_day_threads.game_day_threads_record import GameDayThreadRecord
from src.utils import logger

# Keeping these here for reference, but don't use them because formatted strings in queries are bad.
# TABLE_POSTS = 'game_day_threads'
# COLUMN_POST_ID = 'post_id'
# COLUMN_GAME_ID = 'game_id'

TAG = "GameDayThreadsDao"


class GameDayThreadsDao:
    def __init__(self, db_manager: DbManager):
        self.db_manager = db_manager

    def get_game_day_thread(self, game_id: int) -> Optional[GameDayThreadRecord]:
        query = "SELECT * FROM game_day_threads WHERE game_id=?"
        params = (game_id,)
        logger.i(TAG, f"get_post_id(): executing {query} with params {params}")
        val = self.db_manager.cursor.execute(query, params).fetchone()
        if val is not None:
            return GameDayThreadRecord(val[0], val[1])
        return None

    def insert_game_day_thread(self, post_id: int, game_id: int):
        query = "INSERT INTO game_day_threads VALUES(?, ?)"
        params = (post_id, game_id)
        logger.i(TAG, f"insert_post(): executing {query} with params {params}")
        self.db_manager.cursor.execute(query, params)
        self.db_manager.connection.commit()
        return post_id


game_day_threads_dao = GameDayThreadsDao(db_manager)
