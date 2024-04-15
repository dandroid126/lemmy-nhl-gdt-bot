import os
import unittest

import tests.test_constants as test_constants
from src.db.db_manager import DbManager
from src.db.game_day_threads.game_day_threads_dao import GameDayThreadsDao


class TestGameDayThreadsClient(unittest.TestCase):

    def setUp(self):
        if os.path.exists(test_constants.TEST_DB_PATH):
            os.remove(test_constants.TEST_DB_PATH)
        else:
            print("test.db doesn't exist. Skipping deleting it.")
        db_manager = DbManager(test_constants.TEST_DB_PATH)
        self.game_day_threads_dao = GameDayThreadsDao(db_manager)

    def test_insert_and_get_post_id(self):
        post_id = 1234
        game_id = 4321
        # post_type = PostType.GAME_DAY_THREAD
        self.assertTrue(self.game_day_threads_dao.insert_game_day_thread(post_id, game_id))
        self.assertEqual(self.game_day_threads_dao.get_game_day_thread(game_id).post_id, post_id)

    def test_insert_and_get_post(self):
        post_id = 1111
        game_id = 2222
        # post_type = PostType.COMMENT
        self.assertTrue(self.game_day_threads_dao.insert_game_day_thread(post_id, game_id))
        post_record = self.game_day_threads_dao.get_game_day_thread(game_id)
        print(post_record)
        self.assertEqual(post_record.post_id, post_id, "post_id didn't match")
        self.assertEqual(post_record.game_id, game_id, "game_id didn't match")
        # self.assertEqual(post_record.post_type, post_type, "post_type didn't match")


if __name__ == '__main__':
    unittest.main()
