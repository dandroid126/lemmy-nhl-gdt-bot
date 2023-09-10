from dotenv import load_dotenv
import os

from src import nhl_api_client, constants, db_client, post_utils
from src.lemmy_client import LemmyClient

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
#  check if time is less than an hour from now
games = nhl_api_client.get_games('2022-10-31')
lemmy_client = LemmyClient(lemmy_instance, bot_name, password, community_name)
if db_client.get_post_id(games[0].id) is not None:
    lemmy_client.update_post(post_utils.get_title(games[0]), post_utils.get_body(games[0]), games[0].id)
else:
    lemmy_client.create_post(post_utils.get_title(games[0]), post_utils.get_body(games[0]), games[0].id)
