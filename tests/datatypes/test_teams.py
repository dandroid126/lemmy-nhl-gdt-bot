import unittest

from src.datatypes.teams import Teams


class TestTeams(unittest.TestCase):
    def test_get_team_from_abbreviation(self):
        self.assertEqual(Teams['SJS'], Teams.SJS)

    def test_get_default_team(self):
        self.assertEqual(Teams['BAD ABBREVIATION'], Teams.ERR)

if __name__ == '__main__':
    unittest.main()
