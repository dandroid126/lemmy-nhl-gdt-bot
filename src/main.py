from typing import Optional

from src.datatypes.game import Game
from src.db.comments.comments_dao import CommentsDao
from src.db.daily_threads.daily_threads_dao import DailyThreadsDao
from src.db.daily_threads.daily_threads_record import DailyThreadsRecord
from src.db.db_manager import DbManager
from src.db.game_day_threads.game_day_threads_dao import GameDayThreadsDao
from src.utils import nhl_api_client, constants, post_util, datetime_util, logger
from src.utils.environment_util import EnvironmentUtil
from src.utils.lemmy_client import LemmyClient
from src.utils.signal_util import SignalUtil

TAG = "main"

DELAY_BETWEEN_UPDATING_POSTS = 30

signal_util = SignalUtil()
environment_util = EnvironmentUtil()
db_manager = DbManager(constants.DB_PATH)
game_day_threads_dao = GameDayThreadsDao(db_manager)
daily_threads_dao = DailyThreadsDao(db_manager)
comments_dao = CommentsDao(db_manager)
lemmy_client = LemmyClient(environment_util.lemmy_instance, environment_util.bot_name, environment_util.password,
                           environment_util.community_name, game_day_threads_dao, daily_threads_dao, comments_dao)


def handle_daily_thread(games: list[Game]) -> Optional[DailyThreadsRecord]:
    if not games:
        logger.d(TAG, "List of games is empty. Exiting.")
        return None
    current_day_idlw = datetime_util.get_current_day_as_idlw()
    filtered_games = list(filter(lambda game: datetime_util.is_same_day(game.start_time, current_day_idlw), games))
    if not filtered_games:
        logger.d(TAG, "No games today. Don't create a daily post.")
        return None
    daily_thread = daily_threads_dao.get_daily_thread(current_day_idlw)
    if daily_thread:
        lemmy_client.update_daily_thread(daily_thread.post_id, post_util.get_daily_thread_title(current_day_idlw), post_util.get_daily_thread_body(filtered_games))
        return daily_thread
    # Create daily thread
    return lemmy_client.create_daily_thread(current_day_idlw, post_util.get_daily_thread_title(current_day_idlw), post_util.get_daily_thread_body(filtered_games))


def handle_game_day_thread(game: Game):
    post = game_day_threads_dao.get_game_day_thread(game.id)
    post_id = post.post_id if post else None
    current_time = datetime_util.get_current_time_as_utc()
    if datetime_util.is_time_to_make_post(current_time, game.start_time, game.end_time):
        if post_id is not None:
            lemmy_client.update_game_day_thread(post_util.get_title(game), post_util.get_gdt_body(game), post_id)
        else:
            lemmy_client.create_game_day_thread(post_util.get_title(game), post_util.get_gdt_body(game), game.id)
    else:
        logger.i(TAG,f"main: The post was not created/updated for game '{game.id}' due to the time. current_time: {current_time}; start_time: {game.start_time}; end_time: {game.end_time}")


def handle_comment(daily_thread: DailyThreadsRecord, game: Game):
    if not game or not daily_thread:
        logger.d(TAG, f"Game or daily thread is None. Don't make a post. daily_thread is None: {daily_thread is None}, game is None: {game is None}")
        return
    comment = comments_dao.get_comment(game.id)
    comment_id = comment.comment_id if comment else None
    current_time = datetime_util.get_current_time_as_utc()
    if datetime_util.is_time_to_make_post(current_time, game.start_time, game.end_time):
        if comment_id is not None:
            lemmy_client.update_comment(comment_id, post_util.get_game_details(game))
        else:
            lemmy_client.create_comment(daily_thread.post_id, game.id, post_util.get_game_details(game))
    else:
        logger.i(TAG,f"main: The comment was not created/updated for game '{game.id}' due to the time. current_time: {current_time}; start_time: {game.start_time}; end_time: {game.end_time}")


while not signal_util.is_interrupted:
    try:
        games = nhl_api_client.get_games(datetime_util.yesterday(), datetime_util.tomorrow())
        if not games:
            continue
        daily_thread = handle_daily_thread(games)
        for game in games:
            try:
                if game is None:
                    logger.d(TAG, "Game is None. Skip making a post for this game.")
                    continue
                game_type = game.get_game_type()
                if game_type in environment_util.gdt_post_types:
                    handle_game_day_thread(game)
                elif game_type in environment_util.comment_post_types:
                    handle_comment(daily_thread, game)
            except InterruptedError as e:
                # If an InterruptedError is raised while processing games,
                #  we need to break out before the catch-all below catches it and does nothing.
                logger.e(TAG, "main: An InterruptedError was raised while processing games.", e)
                break
            except Exception as e:
                logger.e(TAG, "main: Some exception occurred while processing a game.", e)
        if not signal_util.is_interrupted:
            # If interrupted, don't sleep. Just exit.
            signal_util.wait(DELAY_BETWEEN_UPDATING_POSTS)
    except InterruptedError as e:
        logger.e(TAG, "main: An InterruptedError was raised while sleeping.", e)

logger.i(TAG, f"main: Reached the end. Shutting down. is_interrupted: {signal_util.is_interrupted}")
