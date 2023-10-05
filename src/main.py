from src.db.comments.comments_dao import CommentsDao
from src.db.daily_threads.daily_threads_dao import DailyThreadsDao
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

while not signal_util.is_interrupted:
    try:
        games = nhl_api_client.get_games(datetime_util.yesterday(), datetime_util.tomorrow())
        # games = nhl_api_client.get_games('2022-10-31', '2022-11-01')
        for game in games:
            try:
                if game is None:
                    continue
                post = game_day_threads_dao.get_game_day_thread(game.id)
                post_id = post.post_id if post else None
                current_time = datetime_util.get_current_time_as_utc()
                if datetime_util.is_time_to_make_post(current_time, game.start_time, game.end_time):
                    if post_id is not None:
                        lemmy_client.update_game_day_thread(post_util.get_title(game), post_util.get_body(game), post_id)
                    else:
                        lemmy_client.create_game_day_thread(post_util.get_title(game), post_util.get_body(game), game.id)
                else:
                    logger.i(TAG, f"main: The post was not created/updated for game '{game.id}' due to the time. current_time: {current_time}; start_time: {game.start_time}; end_time: {game.end_time}")
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
