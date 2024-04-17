from typing import Optional

from src.db.daily_threads.daily_threads_record import DailyThreadsRecord
from src.db.db_manager import DbManager, db_manager
from src.utils.log_util import LOGGER

# Keeping these here for reference, but don't use them because formatted strings in queries are bad.
# TABLE_DAILY_THREADS = 'daily_threads'
# COLUMN_DAILY_THREAD_ID = 'daily_thread_id'
# COLUMN_GAME_ID = 'game_id'

TAG = "DailyThreadsDao"


class DailyThreadsDao:
    def __init__(self, db_manager: DbManager):
        self.db_manager = db_manager

    def get_daily_thread(self, date: str) -> Optional[DailyThreadsRecord]:
        """
        Retrieves the daily thread record for a given date.

        Args:
            date (str): The date for which to retrieve the daily thread record.

        Returns:
            Optional[DailyThreadsRecord]: The daily thread record if found, None otherwise.
        """
        query = "SELECT * FROM daily_threads WHERE date=?"
        params = (date,)
        LOGGER.i(TAG, f"get_daily_thread_id(): executing {query} with params {params}")
        val = self.db_manager.cursor.execute(query, params).fetchone()
        if val is not None:
            return DailyThreadsRecord(val[0], val[1], val[2])
        return None

    def get_most_recent_daily_thread(self) -> Optional[DailyThreadsRecord]:
        """
        Retrieves the most recent daily thread from the database.

        Returns:
            Optional[DailyThreadsRecord]: The most recent daily thread, or None if no thread is found.
        """
        query = "SELECT * FROM daily_threads ORDER BY date DESC"
        LOGGER.i(TAG, f"get_daily_thread_id(): executing {query}")
        val = self.db_manager.cursor.execute(query).fetchone()
        if val is not None:
            return DailyThreadsRecord(val[0], val[1], val[2])
        return None

    def insert_daily_thread(self, post_id: int, date: str, is_featured: bool) -> Optional[DailyThreadsRecord]:
        """
        Insert a new daily thread into the database.

        Args:
            post_id (int): The ID of the post associated with the daily thread.
            date (str): The date of the daily thread.
            is_featured (bool): Whether the daily thread is featured or not.

        Returns:
            Optional[DailyThreadsRecord]: The inserted daily thread record, if successful. Otherwise, None.
        """
        query = "INSERT INTO daily_threads VALUES(?, ?, ?) RETURNING *"
        params = (post_id, date, is_featured)
        LOGGER.i(TAG, f"insert_daily_thread(): executing {query} with params {params}")
        val = self.db_manager.cursor.execute(query, params).fetchone()
        self.db_manager.connection.commit()
        if val is not None:
            return DailyThreadsRecord(val[0], val[1], val[2])
        return None

    def feature_daily_thread(self, post_id):
        """
        Updates the `is_featured` field of the `daily_threads` table for a specific `post_id`.

        Args:
            post_id (int): The ID of the post to be featured.

        Returns:
            DailyThreadsRecord or None: The updated `DailyThreadsRecord` object if the update was successful,
                                       otherwise returns `None`.
        """
        query = "UPDATE daily_threads SET is_featured = true WHERE post_id=? RETURNING *"
        params = (post_id,)
        LOGGER.i(TAG, f"feature_daily_thread(): executing {query} with params {params}")
        val = self.db_manager.cursor.execute(query, params).fetchone()
        self.db_manager.connection.commit()
        if val is not None:
            return DailyThreadsRecord(val[0], val[1], val[2])
        return None

    def unfeature_daily_thread(self, post_id):
        """
        Updates the `is_featured` field of the `daily_threads` table to false for a given `post_id`.

        Args:
            post_id (int): The ID of the post to unfeature.

        Returns:
            DailyThreadsRecord or None: The updated `DailyThreadsRecord` object if the update was successful,
            otherwise `None`.
        """
        query = "UPDATE daily_threads SET is_featured = false WHERE post_id=? RETURNING *"
        params = (post_id,)
        LOGGER.i(TAG, f"feature_daily_thread(): executing {query} with params {params}")
        val = self.db_manager.cursor.execute(query, params).fetchone()
        self.db_manager.connection.commit()
        if val is not None:
            return DailyThreadsRecord(val[0], val[1], val[2])
        return None

    def get_featured_daily_threads(self):
        """
        Retrieves a list of featured daily threads from the database.

        Returns:
            list: A list of DailyThreadsRecord objects representing the featured daily threads.
        """
        query = "SELECT * FROM daily_threads WHERE is_featured=true"
        LOGGER.i(TAG, f"get_featured_daily_threads(): executing {query}")
        vals = self.db_manager.cursor.execute(query).fetchall()
        out = []
        for val in vals:
            out.append(DailyThreadsRecord(val[0], val[1], val[2]))
        return out


daily_threads_dao = DailyThreadsDao(db_manager)
