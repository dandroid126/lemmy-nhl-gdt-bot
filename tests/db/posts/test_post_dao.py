import os
import unittest

from src.db.db_manager import DbManager
from src.db.posts.post_dao import PostDao
from src.db.posts.post_record import PostType
from tests import test_constants


class TestDbClient(unittest.TestCase):

    def setUp(self):
        if os.path.exists(test_constants.TEST_DB_PATH):
            os.remove(test_constants.TEST_DB_PATH)
        else:
            print("test.db doesn't exist. Skipping deleting it.")
        db_manager = DbManager(test_constants.TEST_DB_PATH)
        self.post_dao = PostDao(db_manager)

    def test_insert_and_get_post_id(self):
        post_id = 1234
        game_id = 4321
        post_type = PostType.GAME_DAY_THREAD
        self.assertTrue(self.post_dao.insert_post(post_id, game_id, post_type))
        self.assertEqual(self.post_dao.get_post_id(game_id), post_id)

    def test_insert_and_get_post(self):
        post_id = 1111
        game_id = 2222
        post_type = PostType.COMMENT
        self.assertTrue(self.post_dao.insert_post(post_id, game_id, post_type))
        post_record = self.post_dao.get_post(game_id)
        print(post_record)
        self.assertEqual(post_record.post_id, post_id, "post_id didn't match")
        self.assertEqual(post_record.game_id, game_id, "game_id didn't match")
        self.assertEqual(post_record.post_type, post_type, "post_type didn't match")


if __name__ == '__main__':
    unittest.main()
