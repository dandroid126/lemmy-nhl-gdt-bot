import unittest

import test_constants
from src.datatypes.teams import Teams
from src.datatypes.game import GameType
from src.utils.environment_util import EnvironmentUtil

EXAMPLE_ENV_FILE = f"{test_constants.TEST_RES_PATH}/environment_example"
EXAMPLE_ENV_FILE_NO_TEAMS = f"{test_constants.TEST_RES_PATH}/environment_example_no_teams"


class TestEnvironmentUtil(unittest.TestCase):

    def test_get_comment_game_types_single(self):
        provided = 'REGULAR'
        expected = [GameType.REGULAR]

        self.assertEqual(EnvironmentUtil.parse_game_types(provided), expected)

    def test_get_game_types_list_of_2(self):
        provided = 'PRESEASON,REGULAR'
        expected = [GameType.PRESEASON, GameType.REGULAR]

        self.assertEqual(EnvironmentUtil.parse_game_types(provided), expected)

    def test_get_comment_game_types_list_of_3(self):
        provided = 'PRESEASON,REGULAR,POSTSEASON'
        expected = [GameType.PRESEASON, GameType.REGULAR, GameType.POSTSEASON]

        self.assertEqual(EnvironmentUtil.parse_game_types(provided), expected)

    def test_get_comment_game_types_list_of_4(self):
        provided = 'PRESEASON,REGULAR,POSTSEASON,ALLSTAR'
        expected = [GameType.PRESEASON, GameType.REGULAR, GameType.POSTSEASON, GameType.ALLSTAR]

        self.assertEqual(EnvironmentUtil.parse_game_types(provided), expected)

    def test_load_example_dotenv(self):
        expected_bot_name = "bot_name"
        expected_password = "bot_password"
        expected_lemmy_instance = "https://lemmy.ml"
        expected_community_name = "some_community_name@lemmy.world"
        expected_comment_posts = [GameType.PRESEASON, GameType.REGULAR]
        expected_gdt_posts = [GameType.POSTSEASON, GameType.ALLSTAR]
        expected_teams = [Teams.SJS.value, Teams.NYR.value, Teams.DAL.value]
        environment_util = EnvironmentUtil(EXAMPLE_ENV_FILE)
        self.assertEqual(expected_bot_name, environment_util.bot_name, "bot_name didn't match")
        self.assertEqual(expected_password, environment_util.password, "password didn't match")
        self.assertEqual(expected_lemmy_instance, environment_util.lemmy_instance, "lemmy_instance didn't match")
        self.assertEqual(expected_community_name, environment_util.community_name, "community_name didn't match")
        self.assertEqual(expected_comment_posts, environment_util.comment_post_types, "comment_post_types didn't match")
        self.assertEqual(expected_gdt_posts, environment_util.gdt_post_types, "gdt_post_types didn't match")
        self.assertEqual(expected_teams, environment_util.teams, "teams didn't match")

    def test_load_example_dotenv_no_teams(self):
        expected_bot_name = "bot_name"
        expected_password = "bot_password"
        expected_lemmy_instance = "https://lemmy.ml"
        expected_community_name = "some_community_name@lemmy.world"
        expected_comment_posts = [GameType.PRESEASON, GameType.REGULAR]
        expected_gdt_posts = [GameType.POSTSEASON, GameType.ALLSTAR]
        expected_teams = Teams.get_all_teams()
        environment_util = EnvironmentUtil(EXAMPLE_ENV_FILE_NO_TEAMS)
        self.assertEqual(expected_bot_name, environment_util.bot_name, "bot_name didn't match")
        self.assertEqual(expected_password, environment_util.password, "password didn't match")
        self.assertEqual(expected_lemmy_instance, environment_util.lemmy_instance, "lemmy_instance didn't match")
        self.assertEqual(expected_community_name, environment_util.community_name, "community_name didn't match")
        self.assertEqual(expected_comment_posts, environment_util.comment_post_types, "comment_post_types didn't match")
        self.assertEqual(expected_gdt_posts, environment_util.gdt_post_types, "gdt_post_types didn't match")
        self.assertEqual(expected_teams, environment_util.teams, "teams didn't match")


if __name__ == '__main__':
    unittest.main()
