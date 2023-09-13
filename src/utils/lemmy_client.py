from pythorhead import Lemmy

from src.utils import db_client
from src.utils import logger

TAG = 'LemmyClient'

DICT_KEY_POST_VIEW = 'post_view'
DICT_KEY_POST = 'post'
DICT_KEY_ID = 'id'


class LemmyClient:
    def __init__(self, lemmy_instance, bot_name, password, community_name):
        self.lemmy_instance = lemmy_instance
        self.bot_name = bot_name
        self.password = password
        self.community_name = community_name

        self.lemmy = Lemmy(self.lemmy_instance)
        self.lemmy.log_in(self.bot_name, self.password)
        self.community_id = self.lemmy.discover_community(self.community_name)
        if self.community_id is None:
            logger.e(TAG, f"Community {community_name} not found")
            raise ValueError(f"Community {community_name} not found")

    def create_post(self, title, body, game_id):
        post_id = self.lemmy.post.create(self.community_id, name=title, body=body)[DICT_KEY_POST_VIEW][DICT_KEY_POST][DICT_KEY_ID]
        db_client.insert_row(post_id, game_id)

    def update_post(self, title, body, post_id):
        self.lemmy.post.edit(post_id=post_id, name=title, body=body)
