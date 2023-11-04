from datetime import datetime

from src.datatypes.game import Game
from src.datatypes.game_info import GameInfo
from src.db.comments.comments_dao import comments_dao
from src.db.game_day_threads.game_day_threads_dao import game_day_threads_dao
from src.utils import datetime_util
from src.utils.environment_util import environment_util

FINAL = 'Final'
TIME_CLOCK = 'Time Clock'
TEAM = 'Team'
TOTAL = 'Total'
SO = 'SO'
SHOTS = 'Shots'
HITS = 'Hits'
BLOCKED = 'Blocked'
FO_WINS = 'FO Wins'
GIVEAWAYS = 'Giveaways'
TAKEAWAYS = 'Takeaways'
POWER_PLAYS = 'Power Plays'
PERIOD = 'Period'
TIME = 'Time'
STRENGTH = 'Strength'
GOALIE = 'Goalie'
DESCRIPTION = 'Description'
TYPE = 'Type'
MIN = 'Min'
PT = "PT"
MT = "MT"
CT = "CT"
ET = "ET"
AT = "AT"
LINE_BREAK = "&nbsp;"
MATCH_UP = "Match up"
LINK = "Link"

TEAM_STATS_HEADER_ROW = [TEAM, SHOTS, HITS, BLOCKED, FO_WINS, GIVEAWAYS, TAKEAWAYS, POWER_PLAYS]
GOALS_DETAILS_HEADER_ROW = [PERIOD, TIME, TEAM, STRENGTH, GOALIE, DESCRIPTION]
PENALTY_DETAILS_HEADER_ROW = [PERIOD, TIME, TEAM, TYPE, MIN, DESCRIPTION]
START_TIME_HEADER_ROW = [PT, MT, CT, ET, AT]
DAY_OVERVIEW_HEADER_ROW = [MATCH_UP, TIME, LINK]

FOOTER_TEXT = "I am open source! Report issues, contribute, and fund me [on my GitHub page](https://github.com/dandroid126/lemmy-nhl-gdt-bot)!"


def get_title(game: Game):
    return f"[GDT] {game.away_team.city} {game.away_team.name} at {game.home_team.city} {game.home_team.name} - {get_formatted_game_start_time(game.start_time)}"


def get_gdt_body(game: Game):
    return f"""{get_game_details(game)}

{LINE_BREAK}

{FOOTER_TEXT}
"""


def get_game_details(game: Game):
    if game is None:
        return ""
    time_clock = get_time_clock(game.game_info)
    periods = get_periods(game)
    team_stats = get_team_stats(game)
    goal_details = get_goal_details(game)
    penalty_details = get_penalty_details(game)
    start_time_table = get_start_time_table(game)

    # Render everything
    return f"""{time_clock.render()}

{LINE_BREAK}

{periods.render()}

{LINE_BREAK}

{team_stats.render()}

{LINE_BREAK if goal_details.render() else ""}

{goal_details.render()}

{LINE_BREAK if penalty_details.render() else ""}

{penalty_details.render()}

{LINE_BREAK}

#### Start Times

{start_time_table.render()}"""


def get_formatted_time_clock_time(game_info: GameInfo):
    return f"{f'{game_info.current_period} - ' if not game_info.game_clock.lower() == FINAL.lower() and game_info.is_game_started() else ''}{game_info.game_clock}"


def get_formatted_game_start_time(start_time: datetime):
    return start_time.astimezone(datetime_util.ET).strftime(datetime_util.START_TIME_FORMAT)


def get_time_clock(game_info: GameInfo):
    time_clock = Table()
    time_clock.set(0, 0, TIME_CLOCK)
    time_clock.set(0, 1, get_formatted_time_clock_time(game_info))
    return time_clock


def get_periods(game):
    periods = Table()
    periods.set(0, 0, TEAM)
    periods.set(0, 1, game.away_team.get_team_table_entry())
    periods.set(0, 2, game.home_team.get_team_table_entry())
    for period in game.away_team_stats.periods:
        periods.set(period.period_number, 0, period.ordinal_number)
        periods.set(period.period_number, 1, period.goals)
    for period in game.home_team_stats.periods:
        periods.set(period.period_number, 2, period.goals)
    if game.away_team_stats.shootout.has_been_played:
        final_column = periods.max_x + 1
        periods.set(final_column, 0, SO)
        periods.set(final_column, 1, f"{game.away_team_stats.shootout.scores}/{game.away_team_stats.shootout.attempts}")
        periods.set(final_column, 2, f"{game.home_team_stats.shootout.scores}/{game.home_team_stats.shootout.attempts}")
    final_column = periods.max_x + 1
    periods.set(final_column, 0, TOTAL)
    periods.set(final_column, 1, game.away_team_stats.goals)
    periods.set(final_column, 2, game.home_team_stats.goals)
    return periods


def get_team_stats(game):
    team_stats = Table()
    for i, value in enumerate(TEAM_STATS_HEADER_ROW):
        team_stats.set(i, 0, value)
    team_stats.set(0, 1, game.away_team.get_team_table_entry())
    team_stats.set(0, 2, game.home_team.get_team_table_entry())
    for i, value in enumerate([game.away_team_stats, game.home_team_stats]):
        team_stats.set(1, i + 1, value.shots)
        team_stats.set(2, i + 1, value.hits)
        team_stats.set(3, i + 1, value.blocked)
        team_stats.set(4, i + 1, f'{value.fo_wins}%')
        team_stats.set(5, i + 1, value.giveaways)
        team_stats.set(6, i + 1, value.takeaways)
        team_stats.set(7, i + 1, f'{value.pp_goals}/{value.pp_opportunities}')
    return team_stats


def get_goal_details(game):
    goal_details = Table()
    if not game.goals:
        return goal_details
    for i, value in enumerate(GOALS_DETAILS_HEADER_ROW):
        goal_details.set(i, 0, value)
    for i, goal in enumerate(reversed(game.goals)):
        goal_details.set(0, i + 1, goal.period)
        goal_details.set(1, i + 1, goal.time)
        goal_details.set(2, i + 1, goal.team.get_team_table_entry())
        goal_details.set(3, i + 1, goal.strength)
        goal_details.set(4, i + 1, goal.goalie)
        goal_details.set(5, i + 1, goal.description)
    return goal_details


def get_penalty_details(game):
    penalty_details = Table()
    if not game.penalties:
        return penalty_details
    for i, value in enumerate(PENALTY_DETAILS_HEADER_ROW):
        penalty_details.set(i, 0, value)
    for i, penalty in enumerate(reversed(game.penalties)):
        penalty_details.set(0, i + 1, penalty.period)
        penalty_details.set(1, i + 1, penalty.time)
        penalty_details.set(2, i + 1, penalty.team.get_team_table_entry())
        penalty_details.set(3, i + 1, penalty.type)
        penalty_details.set(4, i + 1, penalty.min)
        penalty_details.set(5, i + 1, penalty.description)
    return penalty_details


def get_start_time_table(game):
    start_time = Table()
    for i, value in enumerate(START_TIME_HEADER_ROW):
        start_time.set(i, 0, value)
    start_time.set(0,1, game.start_time.astimezone(datetime_util.PT).strftime(datetime_util.START_TIME_FORMAT_NO_TZ))
    start_time.set(1,1, game.start_time.astimezone(datetime_util.MT).strftime(datetime_util.START_TIME_FORMAT_NO_TZ))
    start_time.set(2,1, game.start_time.astimezone(datetime_util.CT).strftime(datetime_util.START_TIME_FORMAT_NO_TZ))
    start_time.set(3,1, game.start_time.astimezone(datetime_util.ET).strftime(datetime_util.START_TIME_FORMAT_NO_TZ))
    start_time.set(4,1, game.start_time.astimezone(datetime_util.AT).strftime(datetime_util.START_TIME_FORMAT_NO_TZ))
    return start_time


def get_daily_thread_title(day: str):
    return f"[Daily Discussion Thread] All game details and discussion for games on {datetime_util.get_day_as_title_formatted(day)}"


def get_daily_thread_body(games: list[Game]):
    return f"""{get_day_score_overview_table(games).render()}
    
{LINE_BREAK}

{FOOTER_TEXT}"""


def get_day_score_overview_table(games: list[Game]):
    score_overview = Table()
    for i, value in enumerate(DAY_OVERVIEW_HEADER_ROW):
        score_overview.set(i, 0, value)
    for i, game in enumerate(games):
        game_type = game.get_game_type()
        link = ""
        if game_type in environment_util.comment_post_types:
            comment = comments_dao.get_comment(game.id)
            link = comment.get_comment_url() if comment else ""
        elif game_type in environment_util.gdt_post_types:
            game_day_thread = game_day_threads_dao.get_game_day_thread(game.id)
            link = game_day_thread.get_game_day_thread_url() if game_day_thread else ""
        score_overview.set(0, i + 1, f"{game.away_team.get_team_table_entry()}{f' {game.away_team_stats.goals}' if game.game_info.is_game_started() else ''} - {game.home_team.get_team_table_entry()}{f' {game.home_team_stats.goals}' if game.game_info.is_game_started() else ''}")
        score_overview.set(1, i + 1, f'{get_formatted_time_clock_time(game.game_info) if game.game_info.is_game_started() else get_formatted_game_start_time(game.start_time)}')
        score_overview.set(2, i + 1, f'{link}')
    return score_overview


class Table:
    def __init__(self):
        self.data = SelfGrowingTable(lambda: SelfGrowingTable(str))
        self.max_x = 0
        self.max_y = 0

    def set(self, x, y, value):
        if x > self.max_x:
            self.max_x = x
        if y > self.max_y:
            self.max_y = y
        self.data[x][y] = value

    def render(self):
        out = ''
        if self.max_x == 0 and self.max_y == 0:
            return out
        for i in range(0, self.max_x + 1):
            out = out + f'| {self.data[i][0]} '
        out += '|\n'
        for i in range(0, self.max_x + 1):
            out += '|:-:'
        out += '|\n'
        for j in range(1, self.max_y + 1):
            for i in range(0, self.max_x + 1):
                out = out + f'| {self.data[i][j]} '
            out += '|\n'
        return out[:-1]


# I'm not gonna lie, I have no freakin' clue how this works. It's some black magic.
# I shamelessly stole this from here:
# https://stackoverflow.com/questions/44629273/how-to-dynamically-resize-2d-list-in-python
class SelfGrowingTable(list):

    def __init__(self, default_factory, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_factory = default_factory

    def _extend(self, index):
        while len(self) <= index:
            self.append(self.default_factory())

    def __getitem__(self, index):
        self._extend(index)
        return super().__getitem__(index)

    def __setitem__(self, index, value):
        self._extend(index)
        super().__setitem__(index, value)
