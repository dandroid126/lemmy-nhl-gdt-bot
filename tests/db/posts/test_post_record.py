import unittest

from src.db.posts.post_record import PostType


class TestPostRecord(unittest.TestCase):
    def test_post_type_values(self):
        self.assertEqual(PostType.GAME_DAY_THREAD.value, 1, "GAME_DAY_THREAD did not match")
        self.assertEqual(PostType.DAILY_DISCUSSION_THREAD.value, 2, "DAILY_DISCUSSION_THREAD did not match")
        self.assertEqual(PostType.COMMENT.value, 3, "COMMENT did not match")

    def test_get_post_type_from_value(self):
        self.assertEqual(PostType.GAME_DAY_THREAD, PostType(1), "GAME_DAY_THREAD did not match")
        self.assertEqual(PostType.DAILY_DISCUSSION_THREAD, PostType(2), "DAILY_DISCUSSION_THREAD did not match")
        self.assertEqual(PostType.COMMENT, PostType(3), "COMMENT did not match")


if __name__ == '__main__':
    unittest.main()
