import unittest

from src.db.posts.post_dao import PostDao
from src.db.db_manager import DbManager
from src.utils.environment_util import EnvironmentUtil
from src.utils.lemmy_client import LemmyClient
from tests import test_constants

TEST_POST_ID = 105088
TEST_GAME_ID = 0


class TestLemmyClient(unittest.TestCase):
    def setUp(self) -> None:
        environment_util = EnvironmentUtil()
        self.db_manager = DbManager(test_constants.TEST_DB_PATH)
        self.post_dao = PostDao(self.db_manager)
        self.lemmy_client = LemmyClient(environment_util.lemmy_instance, environment_util.bot_name, environment_util.password, environment_util.community_name, self.post_dao)

    def test_create_comment(self):
        # This test actually creates a comment on a lemmy instance.
        # Make sure 'LEMMY_INSTANCE=dandroid.app' in your environment file you are running this test with.
        # The post with the post_id in this test on dandroid.app is safe to spam to.
        # Otherwise, change post_id to match a safe to spam post in the instance your bot is running on.
        result = self.lemmy_client.create_comment(TEST_POST_ID, TEST_GAME_ID, "commenting from a unit test!")
        self.assertTrue(result, "Failed to create comment")
        comment_id = self.post_dao.get_post_id(TEST_GAME_ID)
        print(f"comment_id: {comment_id}")
        self.assertTrue(comment_id != -1, "Failed to retrieve comment from the db")

    def test_get_post(self):
        result = self.post_dao.get_post(TEST_GAME_ID)
        print(result)


if __name__ == '__main__':
    unittest.main()
