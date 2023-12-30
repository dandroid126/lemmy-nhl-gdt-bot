from typing import Optional

from src.db.comments.comments_record import CommentsRecord
from src.db.db_manager import db_manager, DbManager
from src.utils import logger

# Keeping these here for reference, but don't use them because formatted strings in queries are bad.
# TABLE_COMMENTS = 'comments'
# COLUMN_COMMENT_ID = 'comment_id'
# COLUMN_GAME_ID = 'game_id'

TAG = "CommentsDao"


class CommentsDao:
    def __init__(self, db_manager: DbManager):
        """
        Initializes an instance of the class.

        Args:
            db_manager (DbManager): The database manager object.
        """
        self.db_manager = db_manager

    def get_comment(self, game_id: int) -> Optional[CommentsRecord]:
        """
        Retrieve a single comment record from the database based on the given game ID.

        Args:
            game_id (int): The ID of the game.

        Returns:
            Optional[CommentsRecord]: The comment record if it exists, None otherwise.
        """
        query = "SELECT * FROM comments WHERE game_id=?"
        params = (game_id,)
        logger.i(TAG, f"get_comment_id(): executing {query} with params {params}")
        val = self.db_manager.cursor.execute(query, params).fetchone()
        if val is not None:
            return CommentsRecord(val[0], val[1])
        return None

    def insert_comment(self, comment_id: int, game_id: int) -> int:
        """
        Insert a comment into the database.

        Args:
            comment_id (int): The ID of the comment.
            game_id (int): The ID of the game.

        Returns:
            int: The inserted comment ID.
        """
        query = "INSERT INTO comments VALUES(?, ?)"
        params = (comment_id, game_id)
        logger.i(TAG, f"insert_comment(): executing {query} with params {params}")
        self.db_manager.cursor.execute(query, params)
        self.db_manager.connection.commit()
        return comment_id


comments_dao = CommentsDao(db_manager)
