import os
import unittest

from src.utils import constants, db_client


class TestDbClient(unittest.TestCase):
    def setUp(self):
        test_db_path = f"{constants.OUT_PATH}/test.db"
        os.remove(test_db_path)
        db_client.initialize(test_db_path)

    def test_insert_and_get(self):
        db_client.insert_row(1234, 4321)
        self.assertEqual(db_client.get_post_id(4321), 1234)


if __name__ == '__main__':
    unittest.main()
