import datetime
import unittest

from dateutil.tz import tzlocal

from src.datatypes.teams import Teams
from src.datatypes.game import Game
from src.datatypes.period import Period
from src.datatypes.shootout import Shootout
from src.datatypes.team_stats import TeamStats
from src.utils import post_utils
from src.utils.post_utils import Table


class TestPostUtils(unittest.TestCase):

    def test_basic_table(self):
        expected = """| Header 1 | Header 2 |
|:-:|:-:|
| Value 1 | Value 2 |"""
        table = Table()
        table.set(0, 0, "Header 1")
        table.set(0, 1, "Value 1")
        table.set(1, 0, "Header 2")
        table.set(1, 1, "Value 2")
        print(table.render())
        self.assertEqual(expected, table.render())

    def test_table_with_hole(self):
        expected = """| Header 1 | Header 2 |  |  |  |  |
|:-:|:-:|:-:|:-:|:-:|:-:|
| Value 1 | Value 2 |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  | Value 5 |"""
        table = Table()
        table.set(0, 0, "Header 1")
        table.set(0, 1, "Value 1")
        table.set(1, 0, "Header 2")
        table.set(1, 1, "Value 2")
        table.set(5, 5, "Value 5")
        print(table.render())
        self.assertEqual(expected, table.render())

    def test_get_body_in_progress(self):
        game = Game(id=2022020158, away_team=Teams.ANA.value, home_team=Teams.SJS.value,
                    start_time=datetime.datetime(2022, 11, 2, 2, 30, tzinfo=tzlocal()), game_clock='Final',
                    away_team_stats=TeamStats(goals=6, shots=44, blocked=9, hits=19, fo_wins='55.4', giveaways=10,
                                              takeaways=10, pp_opportunities=4, pp_goals=0, pp_percentage='0.0',
                                              periods=[
                                                  Period(goals=3, shots=17, period_number=1, ordinal_number='1st'),
                                                  Period(goals=1, shots=15, period_number=2, ordinal_number='2nd')],
                                              shootout=Shootout(scores=2, attempts=2, has_been_played=False)),
                    home_team_stats=TeamStats(goals=5, shots=44, blocked=17, hits=16, fo_wins='44.6', giveaways=10,
                                              takeaways=10, pp_opportunities=3, pp_goals=1, pp_percentage='33.3',
                                              periods=[
                                                  Period(goals=2, shots=10, period_number=1, ordinal_number='1st'),
                                                  Period(goals=2, shots=18, period_number=2, ordinal_number='2nd')],
                                              shootout=Shootout(scores=1, attempts=3, has_been_played=False)))
        expected = """| Time Clock |
|:-:|
| Final |

&nbsp;

| Team | 1st | 2nd | Total |
|:-:|:-:|:-:|:-:|
| ![Anaheim Ducks](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png "nhl_ana") ANA | 3 | 1 | 6 |
| ![San Jose Sharks](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png "nhl_sjs") SJS | 2 | 2 | 5 |

&nbsp;

| Team | Shots | Hits | Blocked | FO Wins | Giveaways | Takeaways | Power Plays |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| ![Anaheim Ducks](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png "nhl_ana") ANA | 44 | 19 | 9 | 55.4% | 10 | 10 | 0/4 |
| ![San Jose Sharks](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png "nhl_sjs") SJS | 44 | 16 | 17 | 44.6% | 10 | 10 | 1/3 |
"""
        body = post_utils.get_body(game)
        print(body)
        self.assertEqual(expected, post_utils.get_body(game))

    def test_get_body_regulation(self):
        game = Game(id=2022020158, away_team=Teams.ANA.value, home_team=Teams.SJS.value,
                    start_time=datetime.datetime(2022, 11, 2, 2, 30, tzinfo=tzlocal()), game_clock='Final',
                    away_team_stats=TeamStats(goals=6, shots=44, blocked=9, hits=19, fo_wins='55.4', giveaways=10,
                                              takeaways=10, pp_opportunities=4, pp_goals=0, pp_percentage='0.0',
                                              periods=[
                                                  Period(goals=3, shots=17, period_number=1, ordinal_number='1st'),
                                                  Period(goals=1, shots=15, period_number=2, ordinal_number='2nd'),
                                                  Period(goals=1, shots=9, period_number=3, ordinal_number='3rd')],
                                              shootout=Shootout(scores=2, attempts=2, has_been_played=False)),
                    home_team_stats=TeamStats(goals=5, shots=44, blocked=17, hits=16, fo_wins='44.6', giveaways=10,
                                              takeaways=10, pp_opportunities=3, pp_goals=1, pp_percentage='33.3',
                                              periods=[
                                                  Period(goals=2, shots=10, period_number=1, ordinal_number='1st'),
                                                  Period(goals=2, shots=18, period_number=2, ordinal_number='2nd'),
                                                  Period(goals=1, shots=14, period_number=3, ordinal_number='3rd')],
                                              shootout=Shootout(scores=1, attempts=3, has_been_played=False)))
        expected = """| Time Clock |
|:-:|
| Final |

&nbsp;

| Team | 1st | 2nd | 3rd | Total |
|:-:|:-:|:-:|:-:|:-:|
| ![Anaheim Ducks](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png "nhl_ana") ANA | 3 | 1 | 1 | 6 |
| ![San Jose Sharks](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png "nhl_sjs") SJS | 2 | 2 | 1 | 5 |

&nbsp;

| Team | Shots | Hits | Blocked | FO Wins | Giveaways | Takeaways | Power Plays |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| ![Anaheim Ducks](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png "nhl_ana") ANA | 44 | 19 | 9 | 55.4% | 10 | 10 | 0/4 |
| ![San Jose Sharks](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png "nhl_sjs") SJS | 44 | 16 | 17 | 44.6% | 10 | 10 | 1/3 |
"""
        body = post_utils.get_body(game)
        print(body)
        self.assertEqual(expected, post_utils.get_body(game))

    def test_get_body_ot(self):
        game = Game(id=2022020158, away_team=Teams.ANA.value, home_team=Teams.SJS.value,
                    start_time=datetime.datetime(2022, 11, 2, 2, 30, tzinfo=tzlocal()), game_clock='Final',
                    away_team_stats=TeamStats(goals=6, shots=44, blocked=9, hits=19, fo_wins='55.4', giveaways=10,
                                              takeaways=10, pp_opportunities=4, pp_goals=0, pp_percentage='0.0',
                                              periods=[
                                                  Period(goals=3, shots=17, period_number=1, ordinal_number='1st'),
                                                  Period(goals=1, shots=15, period_number=2, ordinal_number='2nd'),
                                                  Period(goals=1, shots=9, period_number=3, ordinal_number='3rd'),
                                                  Period(goals=0, shots=3, period_number=4, ordinal_number='OT')],
                                              shootout=Shootout(scores=2, attempts=2, has_been_played=False)),
                    home_team_stats=TeamStats(goals=5, shots=44, blocked=17, hits=16, fo_wins='44.6', giveaways=10,
                                              takeaways=10, pp_opportunities=3, pp_goals=1, pp_percentage='33.3',
                                              periods=[
                                                  Period(goals=2, shots=10, period_number=1, ordinal_number='1st'),
                                                  Period(goals=2, shots=18, period_number=2, ordinal_number='2nd'),
                                                  Period(goals=1, shots=14, period_number=3, ordinal_number='3rd'),
                                                  Period(goals=0, shots=2, period_number=4, ordinal_number='OT')],
                                              shootout=Shootout(scores=1, attempts=3, has_been_played=False)))
        expected = """| Time Clock |
|:-:|
| Final |

&nbsp;

| Team | 1st | 2nd | 3rd | OT | Total |
|:-:|:-:|:-:|:-:|:-:|:-:|
| ![Anaheim Ducks](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png "nhl_ana") ANA | 3 | 1 | 1 | 0 | 6 |
| ![San Jose Sharks](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png "nhl_sjs") SJS | 2 | 2 | 1 | 0 | 5 |

&nbsp;

| Team | Shots | Hits | Blocked | FO Wins | Giveaways | Takeaways | Power Plays |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| ![Anaheim Ducks](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png "nhl_ana") ANA | 44 | 19 | 9 | 55.4% | 10 | 10 | 0/4 |
| ![San Jose Sharks](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png "nhl_sjs") SJS | 44 | 16 | 17 | 44.6% | 10 | 10 | 1/3 |
"""
        body = post_utils.get_body(game)
        print(body)
        self.assertEqual(expected, post_utils.get_body(game))

    def test_get_body_shootout(self):
        game = Game(id=2022020158, away_team=Teams.ANA.value, home_team=Teams.SJS.value,
                    start_time=datetime.datetime(2022, 11, 2, 2, 30, tzinfo=tzlocal()), game_clock='Final',
                    away_team_stats=TeamStats(goals=6, shots=44, blocked=9, hits=19, fo_wins='55.4', giveaways=10,
                                              takeaways=10, pp_opportunities=4, pp_goals=0, pp_percentage='0.0',
                                              periods=[Period(goals=3, shots=17, period_number=1, ordinal_number='1st'),
                                                       Period(goals=1, shots=15, period_number=2, ordinal_number='2nd'),
                                                       Period(goals=1, shots=9, period_number=3, ordinal_number='3rd'),
                                                       Period(goals=0, shots=3, period_number=4, ordinal_number='OT')],
                                              shootout=Shootout(scores=2, attempts=2, has_been_played=True)),
                    home_team_stats=TeamStats(goals=5, shots=44, blocked=17, hits=16, fo_wins='44.6', giveaways=10,
                                              takeaways=10, pp_opportunities=3, pp_goals=1, pp_percentage='33.3',
                                              periods=[Period(goals=2, shots=10, period_number=1, ordinal_number='1st'),
                                                       Period(goals=2, shots=18, period_number=2, ordinal_number='2nd'),
                                                       Period(goals=1, shots=14, period_number=3, ordinal_number='3rd'),
                                                       Period(goals=0, shots=2, period_number=4, ordinal_number='OT')],
                                              shootout=Shootout(scores=1, attempts=3, has_been_played=True)))
        expected = """| Time Clock |
|:-:|
| Final |

&nbsp;

| Team | 1st | 2nd | 3rd | OT | SO | Total |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| ![Anaheim Ducks](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png "nhl_ana") ANA | 3 | 1 | 1 | 0 | 2/2 | 6 |
| ![San Jose Sharks](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png "nhl_sjs") SJS | 2 | 2 | 1 | 0 | 1/3 | 5 |

&nbsp;

| Team | Shots | Hits | Blocked | FO Wins | Giveaways | Takeaways | Power Plays |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| ![Anaheim Ducks](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png "nhl_ana") ANA | 44 | 19 | 9 | 55.4% | 10 | 10 | 0/4 |
| ![San Jose Sharks](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png "nhl_sjs") SJS | 44 | 16 | 17 | 44.6% | 10 | 10 | 1/3 |
"""
        body = post_utils.get_body(game)
        print(body)
        self.assertEqual(expected, post_utils.get_body(game))


if __name__ == '__main__':
    unittest.main()
