import datetime
import unittest

from dateutil.tz import tzutc

import src.utils.post_util as post_util
from src.datatypes.game import Game
from src.datatypes.game_info import GameInfo
from src.datatypes.goal import Goal
from src.datatypes.penalty import Penalty
from src.datatypes.period import Period
from src.datatypes.shootout import Shootout
from src.datatypes.team_stats import TeamStats
from src.datatypes.teams import Team
from src.utils.post_util import Table


# TODO: add tests for each table function
# TODO: Update game objects with new values after APIv2 implementation
class TestPostUtils(unittest.TestCase):

    def setUp(self) -> None:
        self.maxDiff = None
        # unittest.util._MAX_LENGTH = 20000
        # pass

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
        self.assertEqual(expected, post_util.get_game_details(game))

    def test_get_body(self):
        game = Game(id=2022020158, away_team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), home_team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), start_time=datetime.datetime(2022, 11, 2, 2, 30, tzinfo=tzutc()), end_time=None, game_info=GameInfo(current_period='SO', game_clock='FINAL'), away_team_stats=TeamStats(goals=6, shots=44, blocked=9, hits=19, fo_wins=0.553846, giveaways=10, takeaways=10, pp_fraction='0/4', periods=[Period(goals=3, shots=17, period_number=1, ordinal_number='1st'), Period(goals=1, shots=15, period_number=2, ordinal_number='2nd'), Period(goals=1, shots=9, period_number=3, ordinal_number='3rd'), Period(goals=0, shots=3, period_number=4, ordinal_number='OT')], shootout=Shootout(scores=2, attempts=2, has_been_played=True)), home_team_stats=TeamStats(goals=5, shots=44, blocked=17, hits=16, fo_wins=0.446154, giveaways=10, takeaways=10, pp_fraction='1/3', periods=[Period(goals=2, shots=10, period_number=1, ordinal_number='1st'), Period(goals=2, shots=18, period_number=2, ordinal_number='2nd'), Period(goals=1, shots=14, period_number=3, ordinal_number='3rd'), Period(goals=0, shots=2, period_number=4, ordinal_number='OT')], shootout=Shootout(scores=1, attempts=3, has_been_played=True)), goals=[Goal(period='1st', time='05:16', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even Strength', goalie='', description='Adam Henrique (1) wrist shot, assists: Kevin Shattenkirk (3)', video_url='https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId=6335809960112'), Goal(period='1st', time='06:18', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Even Strength', goalie='', description='Erik Karlsson (7) wrist shot, assists: Evgeny Svechnikov (3), Tomas Hertl (6)', video_url='https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId=6335811710112'), Goal(period='1st', time='06:41', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Even Strength', goalie='', description='Erik Karlsson (8) slap shot, assists: Jaycob Megna (4), Nico Sturm (1)', video_url='https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId=6335810655112'), Goal(period='1st', time='10:52', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even Strength', goalie='', description='Frank Vatrano (4) wrist shot, assists: Isac Lundestrom (4), Jakob Silfverberg (1)', video_url='https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId=6335810159112'), Goal(period='1st', time='19:45', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even Strength', goalie='', description='Adam Henrique (2) backhand shot, assists: Trevor Zegras (2), Kevin Shattenkirk (4)', video_url='https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId=6335808677112'), Goal(period='2nd', time='03:28', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Power Play', goalie='', description='Timo Meier (2) backhand shot, assists: Alexander Barabanov (4), Erik Karlsson (6)', video_url='https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId=6335810650112'), Goal(period='2nd', time='15:10', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even Strength', goalie='', description='Ryan Strome (2) deflected shot, assists: John Klingberg (3), Troy Terry (7)', video_url='https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId=6335810252112'), Goal(period='2nd', time='15:31', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Even Strength', goalie='', description='Timo Meier (3)  shot, assists: None', video_url='https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId=6335810713112'), Goal(period='3rd', time='11:31', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even Strength', goalie='', description='Max Comtois (2) wrist shot, assists: Troy Terry (8), Nathan Beaulieu (1)', video_url='https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId=6335811310112'), Goal(period='3rd', time='17:48', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Even Strength', goalie='', description='Erik Karlsson (9) wrist shot, assists: Alexander Barabanov (5), Tomas Hertl (7)', video_url='https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId=6335810352112'), Goal(period='SO', time='00:00', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even Strength', goalie='', description='Troy Terry (4) backhand shot, assists: None', video_url='')], penalties=[Penalty(period='1st', time='08:55', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), type='Minor', min=2, description='Max Comtois holding against Evgeny Svechnikov'), Penalty(period='1st', time='08:55', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), type='Minor', min=2, description='Evgeny Svechnikov roughing against Max Comtois'), Penalty(period='2nd', time='03:05', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), type='Minor', min=2, description='Max Jones holding-the-stick against Steven Lorentz'), Penalty(period='2nd', time='03:33', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), type='Major', min=5, description='Luke Kunin fighting against Nathan Beaulieu'), Penalty(period='2nd', time='03:33', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), type='Major', min=5, description='Nathan Beaulieu fighting against Luke Kunin'), Penalty(period='2nd', time='04:48', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), type='Minor', min=2, description='Steven Lorentz tripping against Troy Terry'), Penalty(period='2nd', time='08:56', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), type='Minor', min=2, description='Kevin Labanc hooking against Mason McTavish'), Penalty(period='2nd', time='12:31', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), type='Minor', min=2, description='Trevor Zegras slashing against Matt Benning'), Penalty(period='2nd', time='16:06', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), type='Minor', min=2, description='Logan Couture interference against Isac Lundestrom'), Penalty(period='2nd', time='19:05', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), type='Minor', min=2, description='Derek Grant roughing against Radim Simek'), Penalty(period='3rd', time='17:48', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), type='Misconduct', min=10, description='Kevin Shattenkirk misconduct'), Penalty(period='OT', time='00:22', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), type='Minor', min=2, description='Erik Karlsson holding against Troy Terry')])
        expected = """| Time Clock |
|:-:|
| FINAL |

&nbsp;

| Team | 1st | 2nd | 3rd | OT | SO | Total |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| ![ANA](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png) ANA | 3 | 1 | 1 | 0 | 2/2 | 6 |
| ![SJS](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png) SJS | 2 | 2 | 1 | 0 | 1/3 | 5 |

&nbsp;

| Team | Shots | Hits | Blocked | FO Wins | Giveaways | Takeaways | Power Plays |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| ![ANA](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png) ANA | 44 | 19 | 9 | 55.4% | 10 | 10 | 0/4 |
| ![SJS](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png) SJS | 44 | 16 | 17 | 44.6% | 10 | 10 | 1/3 |

&nbsp;

| Period | Time | Team | Strength | Goalie | Description |
|:-:|:-:|:-:|:-:|:-:|:-:|
| SO | 00:00 | ![ANA](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png) ANA | Even Strength |  | Troy Terry (4) backhand shot, assists: None |
| 3rd | 17:48 | ![SJS](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png) SJS | Even Strength |  | [Erik Karlsson (9) wrist shot, assists: Alexander Barabanov (5), Tomas Hertl (7)](https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId=6335810352112) |
| 3rd | 11:31 | ![ANA](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png) ANA | Even Strength |  | [Max Comtois (2) wrist shot, assists: Troy Terry (8), Nathan Beaulieu (1)](https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId=6335811310112) |
| 2nd | 15:31 | ![SJS](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png) SJS | Even Strength |  | [Timo Meier (3)  shot, assists: None](https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId=6335810713112) |
| 2nd | 15:10 | ![ANA](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png) ANA | Even Strength |  | [Ryan Strome (2) deflected shot, assists: John Klingberg (3), Troy Terry (7)](https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId=6335810252112) |
| 2nd | 03:28 | ![SJS](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png) SJS | Power Play |  | [Timo Meier (2) backhand shot, assists: Alexander Barabanov (4), Erik Karlsson (6)](https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId=6335810650112) |
| 1st | 19:45 | ![ANA](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png) ANA | Even Strength |  | [Adam Henrique (2) backhand shot, assists: Trevor Zegras (2), Kevin Shattenkirk (4)](https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId=6335808677112) |
| 1st | 10:52 | ![ANA](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png) ANA | Even Strength |  | [Frank Vatrano (4) wrist shot, assists: Isac Lundestrom (4), Jakob Silfverberg (1)](https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId=6335810159112) |
| 1st | 06:41 | ![SJS](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png) SJS | Even Strength |  | [Erik Karlsson (8) slap shot, assists: Jaycob Megna (4), Nico Sturm (1)](https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId=6335810655112) |
| 1st | 06:18 | ![SJS](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png) SJS | Even Strength |  | [Erik Karlsson (7) wrist shot, assists: Evgeny Svechnikov (3), Tomas Hertl (6)](https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId=6335811710112) |
| 1st | 05:16 | ![ANA](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png) ANA | Even Strength |  | [Adam Henrique (1) wrist shot, assists: Kevin Shattenkirk (3)](https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId=6335809960112) |

&nbsp;

| Period | Time | Team | Type | Min | Description |
|:-:|:-:|:-:|:-:|:-:|:-:|
| OT | 00:22 | ![SJS](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png) SJS | Minor | 2 | Erik Karlsson holding against Troy Terry |
| 3rd | 17:48 | ![ANA](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png) ANA | Misconduct | 10 | Kevin Shattenkirk misconduct |
| 2nd | 19:05 | ![ANA](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png) ANA | Minor | 2 | Derek Grant roughing against Radim Simek |
| 2nd | 16:06 | ![SJS](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png) SJS | Minor | 2 | Logan Couture interference against Isac Lundestrom |
| 2nd | 12:31 | ![ANA](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png) ANA | Minor | 2 | Trevor Zegras slashing against Matt Benning |
| 2nd | 08:56 | ![SJS](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png) SJS | Minor | 2 | Kevin Labanc hooking against Mason McTavish |
| 2nd | 04:48 | ![SJS](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png) SJS | Minor | 2 | Steven Lorentz tripping against Troy Terry |
| 2nd | 03:33 | ![ANA](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png) ANA | Major | 5 | Nathan Beaulieu fighting against Luke Kunin |
| 2nd | 03:33 | ![SJS](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png) SJS | Major | 5 | Luke Kunin fighting against Nathan Beaulieu |
| 2nd | 03:05 | ![ANA](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png) ANA | Minor | 2 | Max Jones holding-the-stick against Steven Lorentz |
| 1st | 08:55 | ![SJS](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png) SJS | Minor | 2 | Evgeny Svechnikov roughing against Max Comtois |
| 1st | 08:55 | ![ANA](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png) ANA | Minor | 2 | Max Comtois holding against Evgeny Svechnikov |

&nbsp;

#### Start Times

| PT | MT | CT | ET | AT |
|:-:|:-:|:-:|:-:|:-:|
| 07:30PM | 08:30PM | 09:30PM | 10:30PM | 11:30PM |

&nbsp;

I am open source! Report issues, contribute, and fund me [on my GitHub page](https://github.com/dandroid126/lemmy-nhl-gdt-bot)!
"""
        body = post_util.get_gdt_body(game)
        print(body)
        self.assertEqual(expected, body)

    def test_get_body_scheduled(self):
        game = Game(id=2023010001, away_team=Team(id=26, abbreviation='LAK', city='Los Angeles', name='Kings', logo_url='https://lemmy.ca/pictrs/image/ffa7e866-dd9a-430b-a3a1-61ef62dff3d9.png'), home_team=Team(id=53, abbreviation='ARI', city='Arizona', name='Coyotes', logo_url='https://lemmy.ca/pictrs/image/c700df7c-41d6-405b-81c2-7b7610aa400b.png'), start_time=datetime.datetime(2023, 9, 23, 4, 5, tzinfo=tzutc()), end_time=None, game_info=GameInfo(current_period='', game_clock='--'), away_team_stats=TeamStats(goals=0, shots=0, blocked=0, hits=0, fo_wins='0.0', giveaways=0, takeaways=0, pp_fraction='0/0', periods=[], shootout=Shootout(scores=0, attempts=0, has_been_played=False)), home_team_stats=TeamStats(goals=0, shots=0, blocked=0, hits=0, fo_wins='0.0', giveaways=0, takeaways=0, pp_fraction='0/0', periods=[], shootout=Shootout(scores=0, attempts=0, has_been_played=False)), goals=[], penalties=[])
        expected = """| Time Clock |
|:-:|
| -- |

&nbsp;

| Team | Total |
|:-:|:-:|
| ![LAK](https://lemmy.ca/pictrs/image/ffa7e866-dd9a-430b-a3a1-61ef62dff3d9.png) LAK | 0 |
| ![ARI](https://lemmy.ca/pictrs/image/c700df7c-41d6-405b-81c2-7b7610aa400b.png) ARI | 0 |

&nbsp;

| Team | Shots | Hits | Blocked | FO Wins | Giveaways | Takeaways | Power Plays |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| ![LAK](https://lemmy.ca/pictrs/image/ffa7e866-dd9a-430b-a3a1-61ef62dff3d9.png) LAK | 0 | 0 | 0 | 0.0% | 0 | 0 | 0/0 |
| ![ARI](https://lemmy.ca/pictrs/image/c700df7c-41d6-405b-81c2-7b7610aa400b.png) ARI | 0 | 0 | 0 | 0.0% | 0 | 0 | 0/0 |









&nbsp;

#### Start Times

| PT | MT | CT | ET | AT |
|:-:|:-:|:-:|:-:|:-:|
| 09:05PM | 10:05PM | 11:05PM | 12:05AM | 01:05AM |

&nbsp;

I am open source! Report issues, contribute, and fund me [on my GitHub page](https://github.com/dandroid126/lemmy-nhl-gdt-bot)!
"""
        body = post_util.get_gdt_body(game)
        print(body)
        self.assertEqual(expected, body)

    def test_game_clock_game_in_progress(self):
        game_info = GameInfo(current_period="2nd", game_clock="12:34")
        expected = """| Time Clock |
|:-:|
| 2nd - 12:34 |"""
        self.assertEqual(post_util.get_time_clock(game_info).render(), expected)

    def test_game_clock_final(self):
        game_info = GameInfo(current_period="3rd", game_clock="Final")
        expected = """| Time Clock |
|:-:|
| Final |"""
        self.assertEqual(post_util.get_time_clock(game_info).render(), expected)

    def test_get_daily_thread_body(self):
        games = [
            Game(id=2022020158, away_team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), home_team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), start_time=datetime.datetime(2022, 11, 2, 2, 30, tzinfo=tzutc()), end_time=datetime.datetime(2022, 11, 2, 5, 35, 23, tzinfo=tzutc()), game_info=GameInfo(current_period='SO', game_clock='Final'), away_team_stats=TeamStats(goals=6, shots=44, blocked=9, hits=19, fo_wins='55.4', giveaways=10, takeaways=10, pp_fraction='0/4', periods=[Period(goals=3, shots=17, period_number=1, ordinal_number='1st'), Period(goals=1, shots=15, period_number=2, ordinal_number='2nd'), Period(goals=1, shots=9, period_number=3, ordinal_number='3rd'), Period(goals=0, shots=3, period_number=4, ordinal_number='OT')], shootout=Shootout(scores=2, attempts=2, has_been_played=True)), home_team_stats=TeamStats(goals=5, shots=44, blocked=17, hits=16, fo_wins='44.6', giveaways=10, takeaways=10, pp_fraction='1/3', periods=[Period(goals=2, shots=10, period_number=1, ordinal_number='1st'), Period(goals=2, shots=18, period_number=2, ordinal_number='2nd'), Period(goals=1, shots=14, period_number=3, ordinal_number='3rd'), Period(goals=0, shots=2, period_number=4, ordinal_number='OT')], shootout=Shootout(scores=1, attempts=3, has_been_played=True)), goals=[Goal(period='1st', time='05:16', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Adam Henrique (1) Wrist Shot, assists: Kevin Shattenkirk (3)'), Goal(period='1st', time='06:18', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Even', goalie='Stolarz', description='Erik Karlsson (7) Wrist Shot, assists: Evgeny Svechnikov (3), Tomas Hertl (6)'), Goal(period='1st', time='06:41', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Even', goalie='Stolarz', description='Erik Karlsson (8) Slap Shot, assists: Jaycob Megna (4), Nico Sturm (1)'), Goal(period='1st', time='10:52', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Frank Vatrano (4) Wrist Shot, assists: Isac Lundestrom (4), Jakob Silfverberg (1)'), Goal(period='1st', time='19:45', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Adam Henrique (2) Backhand, assists: Trevor Zegras (2), Kevin Shattenkirk (4)'), Goal(period='2nd', time='03:28', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Power Play', goalie='Stolarz', description='Timo Meier (2) Backhand, assists: Alexander Barabanov (4), Erik Karlsson (6)'), Goal(period='2nd', time='15:10', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Ryan Strome (2) Deflected, assists: John Klingberg (3), Troy Terry (7)'), Goal(period='2nd', time='15:31', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Even', goalie='Stolarz', description='Timo Meier (3) , assists: none'), Goal(period='3rd', time='11:31', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Max Comtois (2) Wrist Shot, assists: Troy Terry (8), Nathan Beaulieu (1)'), Goal(period='3rd', time='17:48', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Even', goalie='Stolarz', description='Erik Karlsson (9) Wrist Shot, assists: Alexander Barabanov (5), Tomas Hertl (7)'), Goal(period='SO', time='00:00', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), strength='Even', goalie='Stolarz', description='Logan Couture - Wrist Shot'), Goal(period='SO', time='00:00', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Trevor Zegras - Backhand'), Goal(period='SO', time='00:00', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), strength='Even', goalie='Kahkonen', description='Troy Terry - Backhand')], penalties=[Penalty(period='1st', time='08:55', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), type='Minor', min=2, description='Max Comtois Holding against Evgeny Svechnikov'), Penalty(period='1st', time='08:55', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), type='Minor', min=2, description='Evgeny Svechnikov Roughing against Max Comtois'), Penalty(period='2nd', time='03:05', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), type='Minor', min=2, description='Max Jones Holding the stick against Steven Lorentz'), Penalty(period='2nd', time='03:33', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), type='Major', min=5, description='Luke Kunin Fighting against Nathan Beaulieu'), Penalty(period='2nd', time='03:33', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), type='Major', min=5, description='Nathan Beaulieu Fighting against Luke Kunin'), Penalty(period='2nd', time='04:48', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), type='Minor', min=2, description='Steven Lorentz Tripping against Troy Terry'), Penalty(period='2nd', time='08:56', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), type='Minor', min=2, description='Kevin Labanc Hooking against Mason McTavish'), Penalty(period='2nd', time='12:31', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), type='Minor', min=2, description='Trevor Zegras Slashing against Matt Benning'), Penalty(period='2nd', time='16:06', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), type='Minor', min=2, description='Logan Couture Interference against Isac Lundestrom'), Penalty(period='2nd', time='19:05', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), type='Minor', min=2, description='Derek Grant Roughing against Radim Simek'), Penalty(period='3rd', time='17:48', team=Team(id=24, abbreviation='ANA', city='Anaheim', name='Ducks', logo_url='https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png'), type='Misconduct', min=10, description='Kevin Shattenkirk Misconduct'), Penalty(period='OT', time='00:22', team=Team(id=28, abbreviation='SJS', city='San Jose', name='Sharks', logo_url='https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png'), type='Minor', min=2, description='Erik Karlsson Holding against Troy Terry')]),
            Game(id=2023010001, away_team=Team(id=26, abbreviation='LAK', city='Los Angeles', name='Kings', logo_url='https://lemmy.ca/pictrs/image/ffa7e866-dd9a-430b-a3a1-61ef62dff3d9.png'), home_team=Team(id=53, abbreviation='ARI', city='Arizona', name='Coyotes', logo_url='https://lemmy.ca/pictrs/image/c700df7c-41d6-405b-81c2-7b7610aa400b.png'), start_time=datetime.datetime(2023, 9, 23, 4, 5, tzinfo=tzutc()), end_time=None, game_info=GameInfo(current_period='', game_clock='--'), away_team_stats=TeamStats(goals=0, shots=0, blocked=0, hits=0, fo_wins='0.0', giveaways=0, takeaways=0, pp_fraction='0/0', periods=[], shootout=Shootout(scores=0, attempts=0, has_been_played=False)), home_team_stats=TeamStats(goals=0, shots=0, blocked=0, hits=0, fo_wins='0.0', giveaways=0, takeaways=0, pp_fraction='0/0', periods=[], shootout=Shootout(scores=0, attempts=0, has_been_played=False)), goals=[], penalties=[])
        ]
        expected = """| Match up | Time | Link |
|:-:|:-:|:-:|
| ![ANA](https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png) ANA 6 - ![SJS](https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png) SJS 5 | Final |  |
| ![LAK](https://lemmy.ca/pictrs/image/ffa7e866-dd9a-430b-a3a1-61ef62dff3d9.png) LAK - ![ARI](https://lemmy.ca/pictrs/image/c700df7c-41d6-405b-81c2-7b7610aa400b.png) ARI | 12:05AM EDT |  |
    
&nbsp;

I am open source! Report issues, contribute, and fund me [on my GitHub page](https://github.com/dandroid126/lemmy-nhl-gdt-bot)!"""
        self.assertEqual(post_util.get_daily_thread_body(games), expected)


if __name__ == '__main__':
    unittest.main()
