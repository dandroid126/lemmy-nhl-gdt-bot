from dotenv import load_dotenv
import os

from src.utils import nhl_api_client, constants, post_utils, db_client, datetime_utils
from src.utils.lemmy_client import LemmyClient

global bot_name
global password
global lemmy_instance
global community_name


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
#  loop all games in day
#  With the current implementation games will be updated for two days before they are no longer updated.
#   This will cover if a game goes past midnight, but it might be excessive. REVISIT THIS LATER.
games = nhl_api_client.get_games('2022-10-31', '2022-11-1')
print(games)
lemmy_client = LemmyClient(lemmy_instance, bot_name, password, community_name)
post_id = db_client.get_post_id(games[0].id)
if datetime_utils.is_time_to_make_post(datetime_utils.get_current_time_as_utc(), games[0].start_time):
    if post_id is not None:
        lemmy_client.update_post(post_utils.get_title(games[0]), post_utils.get_body(games[0]), post_id)
    else:
        lemmy_client.create_post(post_utils.get_title(games[0]), post_utils.get_body(games[0]), games[0].id)
