import unittest

from src.datatypes.game import Game, GameType


class TestGame(unittest.TestCase):
    def test_get_game_type_real_id_regular(self):
        game = Game(2022020158, None, None, None, None, None, None, None, None, None)
        self.assertEqual(game.get_game_type(), GameType.REGULAR)

    def test_get_game_type_real_id_preseason(self):
        game = Game(2023010002, None, None, None, None, None, None, None, None, None)
        self.assertEqual(game.get_game_type(), GameType.PRESEASON)

    def test_get_game_type_fake_id_regular(self):
        game = Game(9999929999, None, None, None, None, None, None, None, None, None)
        self.assertEqual(game.get_game_type(), GameType.REGULAR)

    def test_get_game_type_fake_id_preseason(self):
        game = Game(9999919999, None, None, None, None, None, None, None, None, None)
        self.assertEqual(game.get_game_type(), GameType.PRESEASON)

    def test_get_game_type_fake_id_postseason(self):
        game = Game(9999939999, None, None, None, None, None, None, None, None, None)
        self.assertEqual(game.get_game_type(), GameType.POSTSEASON)


if __name__ == '__main__':
    unittest.main()
