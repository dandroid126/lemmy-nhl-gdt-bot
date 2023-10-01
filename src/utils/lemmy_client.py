import pydash
from pythorhead import Lemmy

from src.db.posts.post_record import PostType
from src.utils import logger

TAG = 'LemmyClient'

DICT_KEY_POST_VIEW = 'post_view'
DICT_KEY_POST = 'post'
DICT_KEY_ID = 'id'


class LemmyClient:
    def __init__(self, lemmy_instance, bot_name, password, community_name, post_dao):
        self.lemmy_instance = lemmy_instance
        self.bot_name = bot_name
        self.password = password
        self.community_name = community_name
        self.post_dao = post_dao

        self.lemmy = Lemmy(self.lemmy_instance)
        self.lemmy.log_in(self.bot_name, self.password)
        self.community_id = self.lemmy.discover_community(self.community_name)
        if self.community_id is None:
            logger.e(TAG, f"Community {community_name} not found")
            raise ValueError(f"Community {community_name} not found")

    def create_post(self, title, body, game_id):
        post_id = pydash.get(self.lemmy.post.create(self.community_id, name=title, body=body), f"{DICT_KEY_POST_VIEW}.{DICT_KEY_POST}.{DICT_KEY_ID}", -1)
        if post_id == -1:
            logger.e(TAG, f"Failed to create post for game {game_id}")
            return False
        return self.post_dao.insert_post(post_id, game_id, PostType.GAME_DAY_THREAD)

    def update_post(self, title, body, post_id):
        self.lemmy.post.edit(post_id=post_id, name=title, body=body)

    def create_comment(self, post_id, game_id, content):
        comment_id = pydash.get(self.lemmy.comment.create(post_id=post_id, content=content), f"comment_view.comment.id", -1)
        if comment_id == -1:
            logger.e(TAG, f"Failed to create comment. post_id: {post_id}; game_id: {game_id}")
            return False
        return self.post_dao.insert_post(comment_id, game_id, PostType.COMMENT)

    def update_comment(self, comment_id, content):
        self.lemmy.comment.edit(comment_id=comment_id, content=content)
