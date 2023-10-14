from typing import Optional

from src.db.daily_threads.daily_threads_record import DailyThreadsRecord
from src.db.db_manager import DbManager
from src.utils import logger

# Keeping these here for reference, but don't use them because formatted strings in queries are bad.
# TABLE_DAILY_THREADS = 'daily_threads'
# COLUMN_DAILY_THREAD_ID = 'daily_thread_id'
# COLUMN_GAME_ID = 'game_id'

TAG = "DailyThreadsDao"


class DailyThreadsDao:
    def __init__(self, db_manager: DbManager):
        self.db_manager = db_manager

    def get_daily_thread(self, date: str) -> Optional[DailyThreadsRecord]:
        query = "SELECT * FROM daily_threads WHERE date=?"
        params = (date,)
        logger.i(TAG, f"get_daily_thread_id(): executing {query} with params {params}")
        val = self.db_manager.cursor.execute(query, params).fetchone()
        if val is not None:
            return DailyThreadsRecord(val[0], val[1], val[2])
        return None

    def get_most_recent_daily_thread(self) -> Optional[DailyThreadsRecord]:
        query = "SELECT * FROM daily_threads ORDER BY date DESC"
        logger.i(TAG, f"get_daily_thread_id(): executing {query}")
        val = self.db_manager.cursor.execute(query).fetchone()
        if val is not None:
            return DailyThreadsRecord(val[0], val[1], val[2])
        return None

    def insert_daily_thread(self, post_id: int, date: str, is_featured: bool) -> Optional[DailyThreadsRecord]:
        query = "INSERT INTO daily_threads VALUES(?, ?, ?) RETURNING *"
        params = (post_id, date, is_featured)
        logger.i(TAG, f"insert_daily_thread(): executing {query} with params {params}")
        val = self.db_manager.cursor.execute(query, params).fetchone()
        self.db_manager.connection.commit()
        if val is not None:
            return DailyThreadsRecord(val[0], val[1], val[2])
        return None

    def feature_daily_thread(self, post_id):
        query = "UPDATE daily_threads SET is_featured = true WHERE post_id=? RETURNING *"
        params = (post_id,)
        logger.i(TAG, f"feature_daily_thread(): executing {query} with params {params}")
        val = self.db_manager.cursor.execute(query, params).fetchone()
        if val is not None:
            return DailyThreadsRecord(val[0], val[1], val[2])
        return None

    def unfeature_daily_thread(self, post_id):
        query = "UPDATE daily_threads SET is_featured = false WHERE post_id=? RETURNING *"
        params = (post_id,)
        logger.i(TAG, f"feature_daily_thread(): executing {query} with params {params}")
        val = self.db_manager.cursor.execute(query, params).fetchone()
        if val is not None:
            return DailyThreadsRecord(val[0], val[1], val[2])
        return None

    def get_featured_daily_threads(self):
        query = "SELECT * FROM daily_threads WHERE is_featured=true"
        logger.i(TAG, f"get_featured_daily_threads(): executing {query}")
        vals = self.db_manager.cursor.execute(query).fetchall()
        out = []
        for val in vals:
            out.append(DailyThreadsRecord(val[0], val[1], val[2]))
        return out
