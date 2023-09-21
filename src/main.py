from dotenv import load_dotenv
import os

from src.utils import nhl_api_client, constants, post_utils, db_client, datetime_utils, logger
from src.utils.signal_util import SignalUtil
from src.utils.lemmy_client import LemmyClient

global bot_name
global password
global lemmy_instance
global community_name

TAG = "main"

DELAY_BETWEEN_UPDATING_POSTS = 60


def get_env_variables():
    load_dotenv()
    global bot_name
    global password
    global lemmy_instance
    global community_name
    bot_name = os.getenv('BOT_NAME')
    password = os.getenv('PASSWORD')
    lemmy_instance = os.getenv('LEMMY_INSTANCE')
    community_name = os.getenv('COMMUNITY_NAME')
    if not lemmy_instance.startswith('https://'):
        lemmy_instance = f"https://{lemmy_instance}"


signal_util = SignalUtil()
get_env_variables()
db_client.initialize(constants.DB_PATH)
lemmy_client = LemmyClient(lemmy_instance, bot_name, password, community_name)

while not signal_util.is_interrupted:
    try:
        games = nhl_api_client.get_games(str(datetime_utils.yesterday()), str(datetime_utils.tomorrow()))
        # games = nhl_api_client.get_games('2022-10-31', '2022-11-01')
        for game in games:
            try:
                if game is None:
                    continue
                post_id = db_client.get_post_id(game.id)
                current_time = datetime_utils.get_current_time_as_utc()
                if datetime_utils.is_time_to_make_post(current_time, game.start_time, game.end_time):
                    if post_id is not None:
                        lemmy_client.update_post(post_utils.get_title(game), post_utils.get_body(game), post_id)
                    else:
                        lemmy_client.create_post(post_utils.get_title(game), post_utils.get_body(game), game.id)
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
            # time.sleep(DELAY_BETWEEN_UPDATING_POSTS)
            signal_util.wait(DELAY_BETWEEN_UPDATING_POSTS)
    except InterruptedError as e:
        logger.e(TAG, "main: An InterruptedError was raised while sleeping.", e)

logger.i(TAG, f"main: Reached the end. Shutting down. is_interrupted: {signal_util.is_interrupted}")
