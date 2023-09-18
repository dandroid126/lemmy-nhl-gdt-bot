import datetime
import unittest

from dateutil.tz import tzutc

from src.datatypes.goal import Goal
from src.datatypes.penalty import Penalty
from src.datatypes.teams import Team
from src.datatypes.game import Game
from src.datatypes.period import Period
from src.datatypes.shootout import Shootout
from src.datatypes.team_stats import TeamStats
from src.utils import post_utils
from src.utils.post_utils import Table


# TODO: add tests for each table function
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

    def test_empty_game(self):
        game = None
        expected = ""
        self.assertEqual(expected, post_utils.get_body(game))

    def test_get_body(self):
        game = Game(id=2022020158, away_team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), home_team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), start_time=datetime.datetime(2022, 11, 2, 2, 30, tzinfo=tzutc()), end_time=datetime.datetime(2022, 11, 2, 5, 35, 23, tzinfo=tzutc()), game_clock='Final', away_team_stats=TeamStats(goals=6, shots=44, blocked=9, hits=19, fo_wins='55.4', giveaways=10, takeaways=10, pp_opportunities=4, pp_goals=0, pp_percentage='0.0', periods=[Period(goals=3, shots=17, period_number=1, ordinal_number='1st'), Period(goals=1, shots=15, period_number=2, ordinal_number='2nd'), Period(goals=1, shots=9, period_number=3, ordinal_number='3rd'), Period(goals=0, shots=3, period_number=4, ordinal_number='OT')], shootout=Shootout(scores=2, attempts=2, has_been_played=True)), home_team_stats=TeamStats(goals=5, shots=44, blocked=17, hits=16, fo_wins='44.6', giveaways=10, takeaways=10, pp_opportunities=3, pp_goals=1, pp_percentage='33.3', periods=[Period(goals=2, shots=10, period_number=1, ordinal_number='1st'), Period(goals=2, shots=18, period_number=2, ordinal_number='2nd'), Period(goals=1, shots=14, period_number=3, ordinal_number='3rd'), Period(goals=0, shots=2, period_number=4, ordinal_number='OT')], shootout=Shootout(scores=1, attempts=3, has_been_played=True)), goals=[Goal(period='1st', time='05:16', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Adam Henrique (1) Wrist Shot, assists: Kevin Shattenkirk (3)'), Goal(period='1st', time='06:18', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Even', goalie='Stolarz', description='Erik Karlsson (7) Wrist Shot, assists: Evgeny Svechnikov (3), Tomas Hertl (6)'), Goal(period='1st', time='06:41', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Even', goalie='Stolarz', description='Erik Karlsson (8) Slap Shot, assists: Jaycob Megna (4), Nico Sturm (1)'), Goal(period='1st', time='10:52', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Frank Vatrano (4) Wrist Shot, assists: Isac Lundestrom (4), Jakob Silfverberg (1)'), Goal(period='1st', time='19:45', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Adam Henrique (2) Backhand, assists: Trevor Zegras (2), Kevin Shattenkirk (4)'), Goal(period='2nd', time='03:28', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Power Play', goalie='Stolarz', description='Timo Meier (2) Backhand, assists: Alexander Barabanov (4), Erik Karlsson (6)'), Goal(period='2nd', time='15:10', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Ryan Strome (2) Deflected, assists: John Klingberg (3), Troy Terry (7)'), Goal(period='2nd', time='15:31', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Even', goalie='Stolarz', description='Timo Meier (3) , assists: none'), Goal(period='3rd', time='11:31', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Max Comtois (2) Wrist Shot, assists: Troy Terry (8), Nathan Beaulieu (1)'), Goal(period='3rd', time='17:48', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Even', goalie='Stolarz', description='Erik Karlsson (9) Wrist Shot, assists: Alexander Barabanov (5), Tomas Hertl (7)'), Goal(period='SO', time='00:00', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Even', goalie='Stolarz', description='Logan Couture - Wrist Shot'), Goal(period='SO', time='00:00', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Trevor Zegras - Backhand'), Goal(period='SO', time='00:00', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Troy Terry - Backhand')], penalties=[Penalty(period='1st', time='08:55', team='ANA', type='Minor', min=2, description='Max Comtois Holding against Evgeny Svechnikov'), Penalty(period='1st', time='08:55', team='SJS', type='Minor', min=2, description='Evgeny Svechnikov Roughing against Max Comtois'), Penalty(period='2nd', time='03:05', team='ANA', type='Minor', min=2, description='Max Jones Holding the stick against Steven Lorentz'), Penalty(period='2nd', time='03:33', team='SJS', type='Major', min=5, description='Luke Kunin Fighting against Nathan Beaulieu'), Penalty(period='2nd', time='03:33', team='ANA', type='Major', min=5, description='Nathan Beaulieu Fighting against Luke Kunin'), Penalty(period='2nd', time='04:48', team='SJS', type='Minor', min=2, description='Steven Lorentz Tripping against Troy Terry'), Penalty(period='2nd', time='08:56', team='SJS', type='Minor', min=2, description='Kevin Labanc Hooking against Mason McTavish'), Penalty(period='2nd', time='12:31', team='ANA', type='Minor', min=2, description='Trevor Zegras Slashing against Matt Benning'), Penalty(period='2nd', time='16:06', team='SJS', type='Minor', min=2, description='Logan Couture Interference against Isac Lundestrom'), Penalty(period='2nd', time='19:05', team='ANA', type='Minor', min=2, description='Derek Grant Roughing against Radim Simek'), Penalty(period='3rd', time='17:48', team='ANA', type='Misconduct', min=10, description='Kevin Shattenkirk Misconduct'), Penalty(period='OT', time='00:22', team='SJS', type='Minor', min=2, description='Erik Karlsson Holding against Troy Terry')])
        expected = """| Time Clock |
|:-:|
| Final |

&nbsp;

| Team | 1st | 2nd | 3rd | OT | SO | Total |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| ![Anaheim Ducks](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png "nhl_ana") ANA | 3 | 1 | 1 | 0 | 2/2 | 6 |
| ![San Jose Sharks](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png "nhl_sjs") SJS | 2 | 2 | 1 | 0 | 1/3 | 5 |

&nbsp;

| Team | Shots | Hits | Blocked | FO Wins | Giveaways | Takeaways | Power Plays |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| ![Anaheim Ducks](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png "nhl_ana") ANA | 44 | 19 | 9 | 55.4% | 10 | 10 | 0/4 |
| ![San Jose Sharks](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png "nhl_sjs") SJS | 44 | 16 | 17 | 44.6% | 10 | 10 | 1/3 |

&nbsp;

| Period | Time | Team | Strength | Goalie | Description |
|:-:|:-:|:-:|:-:|:-:|:-:|
| SO | 00:00 | ![Anaheim Ducks](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png "nhl_ana") ANA | Even | Kahkonen | Troy Terry - Backhand |
| SO | 00:00 | ![Anaheim Ducks](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png "nhl_ana") ANA | Even | Kahkonen | Trevor Zegras - Backhand |
| SO | 00:00 | ![San Jose Sharks](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png "nhl_sjs") SJS | Even | Stolarz | Logan Couture - Wrist Shot |
| 3rd | 17:48 | ![San Jose Sharks](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png "nhl_sjs") SJS | Even | Stolarz | Erik Karlsson (9) Wrist Shot, assists: Alexander Barabanov (5), Tomas Hertl (7) |
| 3rd | 11:31 | ![Anaheim Ducks](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png "nhl_ana") ANA | Even | Kahkonen | Max Comtois (2) Wrist Shot, assists: Troy Terry (8), Nathan Beaulieu (1) |
| 2nd | 15:31 | ![San Jose Sharks](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png "nhl_sjs") SJS | Even | Stolarz | Timo Meier (3) , assists: none |
| 2nd | 15:10 | ![Anaheim Ducks](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png "nhl_ana") ANA | Even | Kahkonen | Ryan Strome (2) Deflected, assists: John Klingberg (3), Troy Terry (7) |
| 2nd | 03:28 | ![San Jose Sharks](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png "nhl_sjs") SJS | Power Play | Stolarz | Timo Meier (2) Backhand, assists: Alexander Barabanov (4), Erik Karlsson (6) |
| 1st | 19:45 | ![Anaheim Ducks](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png "nhl_ana") ANA | Even | Kahkonen | Adam Henrique (2) Backhand, assists: Trevor Zegras (2), Kevin Shattenkirk (4) |
| 1st | 10:52 | ![Anaheim Ducks](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png "nhl_ana") ANA | Even | Kahkonen | Frank Vatrano (4) Wrist Shot, assists: Isac Lundestrom (4), Jakob Silfverberg (1) |
| 1st | 06:41 | ![San Jose Sharks](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png "nhl_sjs") SJS | Even | Stolarz | Erik Karlsson (8) Slap Shot, assists: Jaycob Megna (4), Nico Sturm (1) |
| 1st | 06:18 | ![San Jose Sharks](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png "nhl_sjs") SJS | Even | Stolarz | Erik Karlsson (7) Wrist Shot, assists: Evgeny Svechnikov (3), Tomas Hertl (6) |
| 1st | 05:16 | ![Anaheim Ducks](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png "nhl_ana") ANA | Even | Kahkonen | Adam Henrique (1) Wrist Shot, assists: Kevin Shattenkirk (3) |

&nbsp;

| Period | Time | Team | Type | Min | Description |
|:-:|:-:|:-:|:-:|:-:|:-:|
| OT | 00:22 | SJS | Minor | 2 | Erik Karlsson Holding against Troy Terry |
| 3rd | 17:48 | ANA | Misconduct | 10 | Kevin Shattenkirk Misconduct |
| 2nd | 19:05 | ANA | Minor | 2 | Derek Grant Roughing against Radim Simek |
| 2nd | 16:06 | SJS | Minor | 2 | Logan Couture Interference against Isac Lundestrom |
| 2nd | 12:31 | ANA | Minor | 2 | Trevor Zegras Slashing against Matt Benning |
| 2nd | 08:56 | SJS | Minor | 2 | Kevin Labanc Hooking against Mason McTavish |
| 2nd | 04:48 | SJS | Minor | 2 | Steven Lorentz Tripping against Troy Terry |
| 2nd | 03:33 | ANA | Major | 5 | Nathan Beaulieu Fighting against Luke Kunin |
| 2nd | 03:33 | SJS | Major | 5 | Luke Kunin Fighting against Nathan Beaulieu |
| 2nd | 03:05 | ANA | Minor | 2 | Max Jones Holding the stick against Steven Lorentz |
| 1st | 08:55 | SJS | Minor | 2 | Evgeny Svechnikov Roughing against Max Comtois |
| 1st | 08:55 | ANA | Minor | 2 | Max Comtois Holding against Evgeny Svechnikov |

&nbsp;

#### Start Times

| PT | MT | CT | ET | AT |
|:-:|:-:|:-:|:-:|:-:|
| 07:30PM | 08:30PM | 09:30PM | 10:30PM | 11:30PM |

&nbsp;

I am open source! Report issues, contribute, and fund me [on my GitHub page](https://github.com/dandroid126/lemmy-nhl-gdt-bot)!
"""
        body = post_utils.get_body(game)
        print(body)
        self.assertEqual(expected, post_utils.get_body(game))

    def test_get_body_scheduled(self):
        game = Game(id=2023010001, away_team=Team(id=26, abbreviation='LAK', city='Los Angeles', name='Kings', logo_url='https://lemmy.ca/pictrs/image/ffa7e866-dd9a-430b-a3a1-61ef62dff3d9.png'), home_team=Team(id=53, abbreviation='ARI', city='Arizona', name='Coyotes', logo_url='https://lemmy.ca/pictrs/image/c700df7c-41d6-405b-81c2-7b7610aa400b.png'), start_time=datetime.datetime(2023, 9, 23, 4, 5, tzinfo=tzutc()), end_time=None, game_clock='--', away_team_stats=TeamStats(goals=0, shots=0, blocked=0, hits=0, fo_wins='0.0', giveaways=0, takeaways=0, pp_opportunities=0, pp_goals=0, pp_percentage='0.0', periods=[], shootout=Shootout(scores=0, attempts=0, has_been_played=False)), home_team_stats=TeamStats(goals=0, shots=0, blocked=0, hits=0, fo_wins='0.0', giveaways=0, takeaways=0, pp_opportunities=0, pp_goals=0, pp_percentage='0.0', periods=[], shootout=Shootout(scores=0, attempts=0, has_been_played=False)), goals=[], penalties=[])
        expected = """| Time Clock |
|:-:|
| -- |

&nbsp;

| Team | Total |
|:-:|:-:|
| ![Los Angeles Kings](https://lemmy.ca/pictrs/image/ffa7e866-dd9a-430b-a3a1-61ef62dff3d9.png "nhl_lak") LAK | 0 |
| ![Arizona Coyotes](https://lemmy.ca/pictrs/image/c700df7c-41d6-405b-81c2-7b7610aa400b.png "nhl_ari") ARI | 0 |

&nbsp;

| Team | Shots | Hits | Blocked | FO Wins | Giveaways | Takeaways | Power Plays |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| ![Los Angeles Kings](https://lemmy.ca/pictrs/image/ffa7e866-dd9a-430b-a3a1-61ef62dff3d9.png "nhl_lak") LAK | 0 | 0 | 0 | 0.0% | 0 | 0 | 0/0 |
| ![Arizona Coyotes](https://lemmy.ca/pictrs/image/c700df7c-41d6-405b-81c2-7b7610aa400b.png "nhl_ari") ARI | 0 | 0 | 0 | 0.0% | 0 | 0 | 0/0 |









&nbsp;

#### Start Times

| PT | MT | CT | ET | AT |
|:-:|:-:|:-:|:-:|:-:|
| 09:05PM | 10:05PM | 11:05PM | 12:05AM | 01:05AM |

&nbsp;

I am open source! Report issues, contribute, and fund me [on my GitHub page](https://github.com/dandroid126/lemmy-nhl-gdt-bot)!
"""
        body = post_utils.get_body(game)
        print(body)
        self.assertEqual(expected, post_utils.get_body(game))


if __name__ == '__main__':
    unittest.main()
