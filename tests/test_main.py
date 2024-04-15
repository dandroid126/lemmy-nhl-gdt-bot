import unittest
from datetime import datetime
from unittest.mock import MagicMock

import main
from src.datatypes.game import Game
from src.db.comments.comments_dao import comments_dao
from src.db.comments.comments_record import CommentsRecord
from src.db.daily_threads.daily_threads_dao import daily_threads_dao
from src.db.daily_threads.daily_threads_record import DailyThreadsRecord
from src.db.game_day_threads.game_day_threads_dao import game_day_threads_dao
from src.utils import datetime_util
from src.utils import logger
from src.utils import post_util
from src.utils.environment_util import environment_util
from src.utils.lemmy_client import lemmy_client


class TestHandleDailyThread(unittest.TestCase):

    def test_empty_games_list(self):
        # Set up
        games = []

        # Execute
        result = main.handle_daily_thread(games)

        # Verify
        self.assertIsNone(result)

    def test_less_than_2_games_and_no_games_requre_a_daily_thread(self):
        # Set up
        games = [Game(2023020193, None, None, datetime.now(), None, None, None, None, None, None)]
        environment_util.comment_post_types = []

        # Execute
        result = main.handle_daily_thread(games)

        # Verify
        self.assertIsNone(result)

    def test_less_than_2_games_and_games_require_a_daily_thread(self):
        # Set up
        games = [Game(2023020193, None, None, datetime.now(), None, None, None, None, None, None)]
        environment_util.comment_post_types = ["PRESEASON", "REGULAR"]

        # Execute
        result = main.handle_daily_thread(games)

        # Verify
        self.assertIsNone(result)

    def test_no_games_scheduled_for_current_day(self):
        # Set up
        games = [Game(2023020193, None, None, datetime(2022, 1, 1), None, None, None, None, None, None)]

        # Execute
        result = main.handle_daily_thread(games)

        # Verify
        self.assertIsNone(result)

    def test_existing_daily_thread(self):
        # Save old values
        old_daily_threads_dao_get_daily_thread = daily_threads_dao.get_daily_thread
        lemmy_client_update_daily_thread = lemmy_client.update_daily_thread
        post_util_get_daily_thread_title = post_util.get_daily_thread_title
        post_util_get_daily_thread_body = post_util.get_daily_thread_body

        # Set up
        games = [Game(2023020193, None, None, datetime.now(), None, None, None, None, None, None), Game(2023020194, None, None, datetime.now(), None, None, None, None, None, None)]
        daily_thread = DailyThreadsRecord(12341234, "2023-11-10", True)
        daily_threads_dao.get_daily_thread = MagicMock(return_value=daily_thread)
        lemmy_client.update_daily_thread = MagicMock(return_value=daily_thread)
        post_util.get_daily_thread_title = MagicMock(return_value="title")
        post_util.get_daily_thread_body = MagicMock(return_value="body")

        # Execute
        result = main.handle_daily_thread(games)

        # Verify
        self.assertEqual(result, daily_thread)
        lemmy_client.update_daily_thread.assert_called_with(daily_thread.post_id, post_util.get_daily_thread_title(daily_thread.date), post_util.get_daily_thread_body(games))

        # Restore
        daily_threads_dao.get_daily_thread = old_daily_threads_dao_get_daily_thread
        lemmy_client.update_daily_thread = lemmy_client_update_daily_thread
        post_util.get_daily_thread_title = post_util_get_daily_thread_title
        post_util.get_daily_thread_body = post_util_get_daily_thread_body

    def test_create_new_daily_thread(self):
        # Save old values
        old_daily_threads_dao_get_daily_thread = daily_threads_dao.get_daily_thread
        lemmy_client_create_daily_thread = lemmy_client.create_daily_thread
        lemmy_client_feature_daily_thread = lemmy_client.feature_daily_thread
        post_util_get_daily_thread_title = post_util.get_daily_thread_title
        post_util_get_daily_thread_body = post_util.get_daily_thread_body

        # Set up
        games = [Game(2023020193, None, None, datetime.now(), None, None, None, None, None, None), Game(2023020194, None, None, datetime.now(), None, None, None, None, None, None)]
        created_daily_thread = DailyThreadsRecord(12341234, str(datetime.today()), True)
        daily_threads_dao.get_daily_thread = MagicMock(return_value=None)
        lemmy_client.create_daily_thread = MagicMock(return_value=created_daily_thread)
        lemmy_client.feature_daily_thread = MagicMock(return_value=None)
        post_util.get_daily_thread_title = MagicMock(return_value="title")
        post_util.get_daily_thread_body = MagicMock(return_value="body")

        # Execute
        result = main.handle_daily_thread(games)

        # Verify
        self.assertEqual(result, created_daily_thread)
        lemmy_client.create_daily_thread.assert_called_with(datetime_util.get_current_day_as_idlw(), post_util.get_daily_thread_title(), post_util.get_daily_thread_body())
        lemmy_client.feature_daily_thread.assert_called_with(created_daily_thread.post_id)

        # Restore
        daily_threads_dao.get_daily_thread = old_daily_threads_dao_get_daily_thread
        lemmy_client.create_daily_thread = lemmy_client_create_daily_thread
        lemmy_client.feature_daily_thread = lemmy_client_feature_daily_thread
        post_util.get_daily_thread_title = post_util_get_daily_thread_title
        post_util.get_daily_thread_body = post_util_get_daily_thread_body


class TestHandleGameDayThread(unittest.TestCase):

    def test_handle_game_day_thread_existing_post_time_to_make_post(self):
        # Save old values
        old_post_util_get_title = post_util.get_title
        old_post_util_get_gdt_body = post_util.get_gdt_body
        old_game_day_threads_dao_get_game_day_thread = game_day_threads_dao.get_game_day_thread
        old_lemmy_client_update_game_day_thread = lemmy_client.update_game_day_thread
        old_datetime_util_is_time_to_make_post = datetime_util.is_time_to_make_post

        # Set up
        game = Game(2023020193, None, None, datetime.now(), None, None, None, None, None, None)
        post = DailyThreadsRecord(123, "2023-11-10", True)
        post_util.get_title = MagicMock(return_value="title")
        post_util.get_gdt_body = MagicMock(return_value="body")
        game_day_threads_dao.get_game_day_thread = MagicMock(return_value=post)
        lemmy_client.update_game_day_thread = MagicMock()
        datetime_util.is_time_to_make_post = MagicMock(return_value=True)

        # Execute
        main.handle_game_day_thread(game)

        # Verify
        game_day_threads_dao.get_game_day_thread.assert_called_once_with(2023020193)
        post_util.get_title.assert_called_once_with(game)
        post_util.get_gdt_body.assert_called_once_with(game)
        lemmy_client.update_game_day_thread.assert_called_once_with(post_util.get_title.return_value, post_util.get_gdt_body.return_value, 123)

        # Restore
        post_util.get_title = old_post_util_get_title
        post_util.get_gdt_body = old_post_util_get_gdt_body
        game_day_threads_dao.get_game_day_thread = old_game_day_threads_dao_get_game_day_thread
        lemmy_client.update_game_day_thread = old_lemmy_client_update_game_day_thread
        datetime_util.is_time_to_make_post = old_datetime_util_is_time_to_make_post

    def test_handle_game_day_thread_existing_post_time_not_to_make_post(self):
        # Save old values
        old_post_util_get_title = post_util.get_title
        old_post_util_get_gdt_body = post_util.get_gdt_body
        old_game_day_threads_dao_get_game_day_thread = game_day_threads_dao.get_game_day_thread
        old_lemmy_client_update_game_day_thread = lemmy_client.update_game_day_thread
        old_datetime_util_is_time_to_make_post = datetime_util.is_time_to_make_post

        # Set up
        game = Game(2023020193, None, None, datetime.now(), None, None, None, None, None, None)
        post = DailyThreadsRecord(123, "2023-11-10", True)
        post_util.get_title = MagicMock(return_value="title")
        post_util.get_gdt_body = MagicMock(return_value="body")
        game_day_threads_dao.get_game_day_thread = MagicMock(return_value=post)
        lemmy_client.update_game_day_thread = MagicMock()
        datetime_util.is_time_to_make_post = MagicMock(return_value=False)

        # Execute
        main.handle_game_day_thread(game)

        # Verify
        game_day_threads_dao.get_game_day_thread.assert_called_once_with(2023020193)
        post_util.get_title.assert_not_called()
        post_util.get_gdt_body.assert_not_called()
        lemmy_client.update_game_day_thread.assert_not_called()

        # Restore
        post_util.get_title = old_post_util_get_title
        post_util.get_gdt_body = old_post_util_get_gdt_body
        game_day_threads_dao.get_game_day_thread = old_game_day_threads_dao_get_game_day_thread
        lemmy_client.update_game_day_thread = old_lemmy_client_update_game_day_thread
        datetime_util.is_time_to_make_post = old_datetime_util_is_time_to_make_post

    def test_handle_game_day_thread_new_post(self):
        # Save old values
        old_post_util_get_title = post_util.get_title
        old_post_util_get_gdt_body = post_util.get_gdt_body
        old_game_day_threads_dao_get_game_day_thread = game_day_threads_dao.get_game_day_thread
        old_lemmy_client_create_game_day_thread = lemmy_client.create_game_day_thread
        old_datetime_util_is_time_to_make_post = datetime_util.is_time_to_make_post

        # Set up
        game = Game(2023020193, None, None, datetime.now(), None, None, None, None, None, None)
        game_day_threads_dao.get_game_day_thread = MagicMock(return_value=None)
        lemmy_client.create_game_day_thread = MagicMock()
        post_util.get_title = MagicMock(return_value="title")
        post_util.get_gdt_body = MagicMock(return_value="body")
        datetime_util.is_time_to_make_post = MagicMock(return_value=True)

        # Execute
        main.handle_game_day_thread(game)

        # Verify
        game_day_threads_dao.get_game_day_thread.assert_called_once_with(2023020193)
        post_util.get_title.assert_called_once_with(game)
        post_util.get_gdt_body.assert_called_once_with(game)
        lemmy_client.create_game_day_thread.assert_called_once_with(post_util.get_title.return_value, post_util.get_gdt_body.return_value, 2023020193)

        # Restore
        post_util.get_title = old_post_util_get_title
        post_util.get_gdt_body = old_post_util_get_gdt_body
        game_day_threads_dao.get_game_day_thread = old_game_day_threads_dao_get_game_day_thread
        lemmy_client.create_game_day_thread = old_lemmy_client_create_game_day_thread
        datetime_util.is_time_to_make_post = old_datetime_util_is_time_to_make_post

    def test_handle_game_day_thread_time_not_reached(self):
        # Save old values
        old_post_util_get_title = post_util.get_title
        old_post_util_get_gdt_body = post_util.get_gdt_body
        old_game_day_threads_dao_get_game_day_thread = game_day_threads_dao.get_game_day_thread
        old_lemmy_client_create_game_day_thread = lemmy_client.create_game_day_thread
        old_datetime_util_is_time_to_make_post = datetime_util.is_time_to_make_post

        # Set up
        game = Game(2023020193, None, None, datetime.now(), None, None, None, None, None, None)
        post = DailyThreadsRecord(123, "2023-11-10", True)
        game_day_threads_dao.get_game_day_thread = MagicMock(return_value=post)
        lemmy_client.update_game_day_thread = MagicMock()
        datetime_util.is_time_to_make_post = MagicMock(return_value=False)
        logger.i = MagicMock()

        # Execute
        main.handle_game_day_thread(game)

        # Verify
        game_day_threads_dao.get_game_day_thread.assert_called_once_with(2023020193)
        datetime_util.is_time_to_make_post.assert_called_once()
        logger.i.assert_called_once()

        # Restore
        post_util.get_title = old_post_util_get_title
        post_util.get_gdt_body = old_post_util_get_gdt_body
        game_day_threads_dao.get_game_day_thread = old_game_day_threads_dao_get_game_day_thread
        lemmy_client.create_game_day_thread = old_lemmy_client_create_game_day_thread
        datetime_util.is_time_to_make_post = old_datetime_util_is_time_to_make_post

    def test_handle_game_day_thread_time_reached(self):
        # Save old values
        old_game_day_threads_dao_get_game_day_thread = game_day_threads_dao.get_game_day_thread
        old_lemmy_client_update_game_day_thread = lemmy_client.update_game_day_thread
        old_datetime_util_is_time_to_make_post = datetime_util.is_time_to_make_post
        old_post_util_get_title = post_util.get_title
        old_post_util_get_gdt_body = post_util.get_gdt_body

        # Set up
        game = Game(2023020193, None, None, datetime.now(), None, None, None, None, None, None)
        post = DailyThreadsRecord(123, "2023-11-10", True)
        game_day_threads_dao.get_game_day_thread = MagicMock(return_value=post)
        lemmy_client.update_game_day_thread = MagicMock()
        datetime_util.is_time_to_make_post = MagicMock(return_value=True)
        post_util.get_title = MagicMock(return_value="title")
        post_util.get_gdt_body = MagicMock(return_value="body")

        # Execute
        main.handle_game_day_thread(game)

        # Verify
        game_day_threads_dao.get_game_day_thread.assert_called_once_with(2023020193)
        datetime_util.is_time_to_make_post.assert_called_once()
        post_util.get_title.assert_called_once_with(game)
        post_util.get_gdt_body.assert_called_once_with(game)
        lemmy_client.update_game_day_thread.assert_called_once_with(post_util.get_title.return_value, post_util.get_gdt_body.return_value, 123)

        # Restore
        game_day_threads_dao.get_game_day_thread = old_game_day_threads_dao_get_game_day_thread
        lemmy_client.update_game_day_thread = old_lemmy_client_update_game_day_thread
        datetime_util.is_time_to_make_post = old_datetime_util_is_time_to_make_post
        post_util.get_title = old_post_util_get_title
        post_util.get_gdt_body = old_post_util_get_gdt_body


class TestHandleComment(unittest.TestCase):
    def test_handle_comment_game_and_daily_thread_none(self):
        # Save old values
        old_logger_d = logger.d
        old_lemmy_client_create_comment = lemmy_client.create_comment

        # Set up
        daily_thread = None
        game = None
        logger.d = MagicMock()
        lemmy_client.create_comment = MagicMock()

        # Execute
        main.handle_comment(daily_thread, game)

        # Verify
        logger.d.assert_called_once_with("main", "Game or daily thread is None. Don't make a post. daily_thread is None: True, game is None: True")
        lemmy_client.create_comment.assert_not_called()

        # Restore
        logger.d = old_logger_d
        lemmy_client.create_comment = old_lemmy_client_create_comment

    def test_handle_comment_existing_comment_time_to_make_post(self):
        # Save old values
        old_comments_dao_get_comment = comments_dao.get_comment
        old_datetime_util_is_time_to_make_post = datetime_util.is_time_to_make_post
        old_post_util_get_game_details = post_util.get_game_details

        # Set up
        game = Game(2023020193, None, None, datetime.now(), None, None, None, None, None, None)
        daily_thread = DailyThreadsRecord(123, "2023-11-10", True)
        comment = CommentsRecord(456, game.id)
        comments_dao.get_comment = MagicMock(return_value=comment)
        datetime_util.is_time_to_make_post = MagicMock(return_value=True)
        post_util.get_game_details = MagicMock(return_value="game_details")
        lemmy_client.create_comment = MagicMock()
        lemmy_client.update_comment = MagicMock()

        # Execute
        main.handle_comment(daily_thread, game)

        # Verify
        lemmy_client.update_comment.assert_called_once_with(456, "game_details")
        lemmy_client.create_comment.assert_not_called()

        # Restore
        comments_dao.get_comment = old_comments_dao_get_comment
        datetime_util.is_time_to_make_post = old_datetime_util_is_time_to_make_post
        post_util.get_game_details = old_post_util_get_game_details

    def test_handle_comment_no_existing_comment_time_to_make_post(self):
        # Save old values
        old_comments_dao_get_comment = comments_dao.get_comment
        old_datetime_util_is_time_to_make_post = datetime_util.is_time_to_make_post
        old_post_util_get_game_details = post_util.get_game_details

        # Set up
        game = Game(2023020193, None, None, datetime.now(), None, None, None, None, None, None)
        daily_thread = DailyThreadsRecord(123, "2023-11-10", True)
        comments_dao.get_comment = MagicMock(return_value=None)
        datetime_util.is_time_to_make_post = MagicMock(return_value=True)
        post_util.get_game_details = MagicMock(return_value="game_details")
        lemmy_client.create_comment = MagicMock()
        lemmy_client.update_comment = MagicMock()

        # Execute
        main.handle_comment(daily_thread, game)

        # Verify
        lemmy_client.update_comment.assert_not_called()
        lemmy_client.create_comment.assert_called_once_with(daily_thread.post_id, game.id, "game_details")

        # Restore
        comments_dao.get_comment = old_comments_dao_get_comment
        datetime_util.is_time_to_make_post = old_datetime_util_is_time_to_make_post
        post_util.get_game_details = old_post_util_get_game_details

    def test_handle_comment_not_time_to_make_post(self):
        # Save old values
        old_comments_dao_get_comment = comments_dao.get_comment
        old_datetime_util_is_time_to_make_post = datetime_util.is_time_to_make_post
        old_lemmy_client_update_comment = lemmy_client.update_comment
        old_lemmy_client_create_comment = lemmy_client.create_comment
        old_logger_i = logger.i

        # Set up
        game = Game(2023020193, None, None, datetime.now(), None, None, None, None, None, None)
        daily_thread = DailyThreadsRecord(123, "2023-11-10", True)
        comments_dao.get_comment = MagicMock(return_value=None)
        datetime_util.is_time_to_make_post = MagicMock(return_value=False)
        lemmy_client.create_comment = MagicMock()
        lemmy_client.update_comment = MagicMock()
        logger.i = MagicMock()


        # Execute
        main.handle_comment(daily_thread, game)

        # Verify
        lemmy_client.update_comment.assert_not_called()
        lemmy_client.create_comment.assert_not_called()
        logger.i.assert_called_once()

        # Restore
        comments_dao.get_comment = old_comments_dao_get_comment
        datetime_util.is_time_to_make_post = old_datetime_util_is_time_to_make_post
        lemmy_client.update_comment = old_lemmy_client_update_comment
        lemmy_client.create_comment = old_lemmy_client_create_comment
        logger.i = old_logger_i


if __name__ == '__main__':
    unittest.main()
