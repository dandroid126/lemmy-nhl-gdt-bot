import random
import sys
import unittest
import uuid

from src.db.comments.comments_dao import CommentsDao
from src.db.daily_threads.daily_threads_dao import DailyThreadsDao
from src.db.db_manager import DbManager
from src.db.game_day_threads.game_day_threads_dao import GameDayThreadsDao
from src.utils import datetime_util
from src.utils.environment_util import EnvironmentUtil
from src.utils.lemmy_client import LemmyClient
from tests import test_constants

TEST_POST_ID = 105088


class TestLemmyClient(unittest.TestCase):
    def setUp(self) -> None:
        environment_util = EnvironmentUtil()
        self.db_manager = DbManager(test_constants.TEST_DB_PATH)
        self.game_day_threads_dao = GameDayThreadsDao(self.db_manager)
        self.daily_threads_dao = DailyThreadsDao(self.db_manager)
        self.comments_dao = CommentsDao(self.db_manager)
        self.lemmy_client = LemmyClient(environment_util.lemmy_instance, environment_util.bot_name,
                                        environment_util.password, environment_util.community_name,
                                        self.game_day_threads_dao, self.daily_threads_dao, self.comments_dao)

    def test_create_comment(self):
        # This test actually creates a comment on a lemmy instance.
        # Make sure the combination of 'LEMMY_INSTANCE' (set in the environment file) and post_id are safe to spam to.
        # One safe combination is 'LEMMY_INSTANCE=dandroid.app' and post_id=105088
        random.seed(str(uuid.uuid4()))
        game_id = random.randint(0, sys.maxsize)
        print(f"generated game_id: {game_id}")
        result_comment_id = self.lemmy_client.create_comment(TEST_POST_ID, game_id, f"commenting from a unit test! generated game_id: {game_id}")
        self.assertNotEqual(result_comment_id, -1, "Failed to create comment")
        print(f"result_comment_id: {result_comment_id}")
        comment_id = self.comments_dao.get_comment(game_id).comment_id
        print(f"comment_id: {comment_id}")
        self.assertNotEqual(comment_id, -1, "Failed to retrieve comment from the db")
        self.assertEqual(comment_id, result_comment_id, "Comment IDs don't match.")

    def test_create_game_day_thread(self):
        # This test actually creates a post on a lemmy instance.
        # Make sure the 'COMMUNITY_NAME' in the environment file you are running this test with is safe to spam to.
        # 'COMMUNITY_NAME=test@dandroid.app' is safe to spam to.
        random.seed(str(uuid.uuid4()))
        game_id = random.randint(0, sys.maxsize)
        result_post_id = self.lemmy_client.create_game_day_thread("unit test title", f"unit test body. generated game_id: {game_id}", game_id)
        self.assertNotEqual(result_post_id, -1, "Failed to create game day thread")
        post_id = self.game_day_threads_dao.get_game_day_thread(game_id).post_id
        print(f"post_id: {post_id}")
        self.assertNotEqual(post_id, -1, "Failed to retrieve comment from the db")
        self.assertEqual(post_id, result_post_id, "Post IDs don't match.")

    def test_create_daily_thread(self):
        # This test actually creates a post on a lemmy instance.
        # Make sure the 'COMMUNITY_NAME' in the environment file you are running this test with is safe to spam to.
        # 'COMMUNITY_NAME=test@dandroid.app' is safe to spam to.
        # random.seed(str(uuid.uuid4()))
        # game_id = random.randint(0, sys.maxsize)
        most_recent_daily_thread = self.daily_threads_dao.get_most_recent_daily_thread()
        if most_recent_daily_thread:
            date = datetime_util.next_day(most_recent_daily_thread.date)
        else:
            date = datetime_util.today()
        result_post_id = self.lemmy_client.create_daily_thread(date, "daily thread unit test", f"daily thread unit test body. date: {date}")
        self.assertNotEqual(result_post_id, -1, "Failed to create game day thread")
        post_id = self.daily_threads_dao.get_daily_thread(date).post_id
        print(f"post_id: {post_id}")
        self.assertNotEqual(post_id, -1, "Failed to retrieve comment from the db")
        self.assertEqual(post_id, result_post_id, "Post IDs don't match.")



    # def test_get_post(self):
    #     result = self.game_day_threads_dao.get_post(TEST_GAME_ID)
    #     print(result)


if __name__ == '__main__':
    unittest.main()
