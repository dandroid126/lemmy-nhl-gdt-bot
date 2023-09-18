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

    # def tearDown(self):
    #     if os.path.exists(TEST_DB_PATH):
    #         os.remove(TEST_DB_PATH)

    def test_insert_and_get(self):
        self.assertTrue(db_client.insert_post(1234, 4321, db_client.POST_TYPE_GDT))
        self.assertEqual(db_client.get_post_id(4321), 1234)

    def test_get_db_schema(self):
        self.assertEqual(db_client.get_db_schema_version(), db_client.DB_SCHEMA_VERSION)

    def test_upgrade_db_schema(self):
        db_client.DB_SCHEMA_VERSION = db_client.DB_SCHEMA_VERSION + 1
        db_client.upgrade_db_schema()
        self.assertEqual(db_client.get_db_schema_version(), db_client.DB_SCHEMA_VERSION)


if __name__ == '__main__':
    unittest.main()
