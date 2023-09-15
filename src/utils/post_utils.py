from src.utils import datetime_utils
from src.datatypes.game import Game


def get_title(game: Game):
    return f"[GDT] {game.away_team} at {game.home_team} - {game.start_time.astimezone(datetime_utils.EST).strftime(datetime_utils.START_TIME_FORMAT)}"


# TODO: dynamically create period goals table based on number of periods
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
TEAM_STATS_HEADER_ROW = [TEAM, SHOTS, HITS, BLOCKED, FO_WINS, GIVEAWAYS, TAKEAWAYS, POWER_PLAYS]


def get_body(game: Game):
    # Time Clock
    time_clock = Table()
    time_clock.set(0, 0, TIME_CLOCK)
    time_clock.set(0, 1, game.game_clock)

    # Periods
    periods = Table()
    periods.set(0, 0, TEAM)
    periods.set(0, 1, game.away_team)
    periods.set(0, 2, game.home_team)
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

    # Team Stats
    team_stats = Table()
    for i, value in enumerate(TEAM_STATS_HEADER_ROW):
        team_stats.set(i, 0, value)
    team_stats.set(0, 1, game.away_team)
    team_stats.set(0, 2, game.home_team)
    for i, value in enumerate([game.away_team_stats, game.home_team_stats]):
        team_stats.set(1, i + 1, value.shots)
        team_stats.set(2, i + 1, value.hits)
        team_stats.set(3, i + 1, value.blocked)
        team_stats.set(4, i + 1, f'{value.fo_wins}%')
        team_stats.set(5, i + 1, value.giveaways)
        team_stats.set(6, i + 1, value.takeaways)
        team_stats.set(7, i + 1, f'{value.pp_goals}/{value.pp_opportunities}')

    # TEAM_STATS_HEADER_ROW = [TEAM, SHOTS, HITS, BLOCKED, FO_WINS, GIVEAWAYS, TAKEAWAYS, POWER_PLAYS]
    # Render everything
    return f"""{time_clock.render()}

&nbsp;

{periods.render()}

&nbsp;

{team_stats.render()}
"""


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
