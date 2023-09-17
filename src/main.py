from dotenv import load_dotenv
import os
import time

from src.utils import nhl_api_client, constants, post_utils, db_client, datetime_utils, logger
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


get_env_variables()
db_client.initialize(constants.DB_PATH)
# TODO:
#  change this to current day
#  With the current implementation games will be updated for two days before they are no longer updated.
#   This will cover if a game goes past midnight, but it might be excessive. REVISIT THIS LATER.
lemmy_client = LemmyClient(lemmy_instance, bot_name, password, community_name)

is_interrupted = False
while not is_interrupted:
    games = nhl_api_client.get_games('2022-10-31', '2022-11-1')
    for game in games:
        try:
            if game is None:
                continue
            post_id = db_client.get_post_id(game.id)
            current_time = datetime_utils.get_current_time_as_utc()
            if datetime_utils.is_time_to_make_post(current_time, game.start_time, None): # TODO: change this back to game.end_time
                if post_id is not None:
                    lemmy_client.update_post(post_utils.get_title(game), post_utils.get_body(game), post_id)
                else:
                    lemmy_client.create_post(post_utils.get_title(game), post_utils.get_body(game), game.id)
            else:
                logger.d(TAG, f"The post was not created/updated for game '{game.id}' due to the time. current_time: {current_time}; start_time: {game.start_time}; end_time: {game.end_time}")
        except Exception as e:
            logger.e(TAG, "Some exception occurred while processing a game.", e)
    time.sleep(DELAY_BETWEEN_UPDATING_POSTS)
