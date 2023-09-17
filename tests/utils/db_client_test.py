import os
import unittest

from src.utils import constants, db_client

TEST_DB_PATH = f"{constants.OUT_PATH}/test.db"


class TestDbClient(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)
        else:
            print("test.db doesn't exist. Skipping deleting it.")
        db_client.initialize(TEST_DB_PATH)

    def test_insert_and_get(self):
        db_client.insert_row(1234, 4321, db_client.POST_TYPE_GDT)
        self.assertEqual(db_client.get_post_id(4321), 1234)


if __name__ == '__main__':
    unittest.main()
