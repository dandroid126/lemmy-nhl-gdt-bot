from pythorhead import Lemmy

from src import constants, db_client


class LemmyClient:
    def __init__(self, lemmy_instance, bot_name, password, community_name):
        self.lemmy_instance = lemmy_instance
        self.bot_name = bot_name
        self.password = password
        self.community_name = community_name

        self.lemmy = Lemmy(self.lemmy_instance)
        self.lemmy.log_in(self.bot_name, self.password)
        self.community_id = self.lemmy.discover_community(self.community_name)

    def create_post(self, title, body, game_id):
        post_id = self.lemmy.post.create(self.community_id, name=title, body=body)['post_view']['post']['id']
        db_client.insert_row(post_id, game_id)

    def update_post(self, title, body, game_id):
        post_id = db_client.get_post_id(game_id)
        self.lemmy.post.edit(post_id=post_id, name=title, body=body)
