import requests
import json
from src.datatypes.Exceptions.IllegalArgumentException import IllegalArgumentException

from src.datatypes.game import Game
from src.datatypes.period import Period
from src.datatypes.shootout import Shootout
from src.datatypes.team_stats import TeamStats
from src.utils import logger, datetime_utils

TAG = "nhl_api_client.py"

URL_REPL_GAME_ID = "{{GAME_ID}}"
URL_REPL_START_DATE = "{{START_DATE}}"
URL_REPL_END_DATE = "{{END_DATE}}"

BASE_URL = "https://statsapi.web.nhl.com/api/v1"
# SCHEDULE_URL = f"{BASE_URL}/schedule?date={URL_REPL_DATE}&expand=schedule.broadcasts"
SCHEDULE_URL = f"{BASE_URL}/schedule?startDate={URL_REPL_START_DATE}&endDate={URL_REPL_END_DATE}&expand=schedule.broadcasts"
FEED_LIVE_URL = f"{BASE_URL}/game/{URL_REPL_GAME_ID}/feed/live"

DICT_KEY_DATES = 'dates'
LIST_KEY_FIRST = 0
DICT_KEY_GAMES = 'games'
DICT_KEY_GAME_DATE = 'gameDate'
DICT_KEY_GAME_PK = 'gamePk'
DICT_KEY_TEAMS = 'teams'
DICT_KEY_AWAY = 'away'
DICT_KEY_HOME = 'home'
DICT_KEY_TEAM = 'team'
DICT_KEY_NAME = 'name'
DICT_KEY_STATUS = 'status'
DICT_KEY_DETAILED_STATE = 'detailedState'
DICT_KEY_SHOTS_ON_GOAL = 'shotsOnGoal'
DICT_KEY_LIVE_DATA = 'liveData'
DICT_KEY_LINE_SCORE = 'linescore'
DICT_KEY_BOX_SCORE = 'boxscore'
DICT_KEY_PERIODS = 'periods'
DICT_KEY_TEAM_STATS = 'teamStats'
DICT_KEY_TEAM_SKATER_STATS = 'teamSkaterStats'
DICT_KEY_NUM = 'num'
DICT_KEY_ORDINAL_NUM = 'ordinalNum'
DICT_KEY_SHOOTOUT_INFO = 'shootoutInfo'
DICT_KEY_SCORES = 'scores'
DICT_KEY_ATTEMPTS = 'attempts'
DICT_KEY_HAS_SHOOTOUT = 'hasShootout'

# Team Stats
DICT_KEY_GOALS = 'goals'
DICT_KEY_SHOTS = 'shots'
DICT_KEY_BLOCKED = 'blocked'
DICT_KEY_HITS = 'hits'
DICT_KEY_FO_WIN_PERCENTAGE = 'faceOffWinPercentage'
DICT_KEY_GIVEAWAYS = 'giveaways'
DICT_KEY_TAKEAWAYS = 'takeaways'
DICT_KEY_PP_OPPORTUNITIES = 'powerPlayOpportunities'
DICT_KEY_PP_GOALS = 'powerPlayGoals'
DICT_KEY_PP_PERCENTAGE = 'powerPlayPercentage'


def get_schedule_url(start_date: str, end_date: str):
    if start_date is None:
        raise IllegalArgumentException(TAG, "start_date must not be None")
    if end_date is None:
        raise IllegalArgumentException(TAG, "end_date must not be None")
    return SCHEDULE_URL.replace(URL_REPL_START_DATE, start_date).replace(URL_REPL_END_DATE, end_date)


def get_feed_live_url(game_id: int):
    if game_id is None:
        raise IllegalArgumentException(TAG, "game_id must not be None")
    return FEED_LIVE_URL.replace(URL_REPL_GAME_ID, str(game_id))


def get_games(start_date: str = None, end_date: str = None) -> list[Game]:
    if start_date is None:
        start_date = datetime_utils.yesterday()
    if end_date is None:
        end_date = datetime_utils.today()
    url = get_schedule_url(start_date, end_date)
    logger.d(TAG, f"get_games(): url: {url}")
    games = []
    dates = json.loads(requests.get(url).text)[DICT_KEY_DATES]
    for date in dates:
        games.extend(date[DICT_KEY_GAMES])
    out = []
    for game in games:
        feed_live = get_feed_live(game[DICT_KEY_GAME_PK])
        parse_team_stats(feed_live)
        out.append(parse_game(game, feed_live))  # TODO: only use feed_live
    return out


def get_feed_live(game_id: int):
    if game_id is None:
        raise IllegalArgumentException(TAG, "game_id must not be None")
    url = get_feed_live_url(game_id)
    logger.d(TAG, f"get_box_score: url: {url}")
    box_score = json.loads(requests.get(url).text)
    return box_score


def parse_periods(feed_live: dict):
    out = {
        DICT_KEY_HOME: [],
        DICT_KEY_AWAY: []
    }
    for period in feed_live[DICT_KEY_LIVE_DATA][DICT_KEY_LINE_SCORE][DICT_KEY_PERIODS]:
        out[DICT_KEY_HOME].append(
            Period(goals=period[DICT_KEY_HOME][DICT_KEY_GOALS], shots=period[DICT_KEY_HOME][DICT_KEY_SHOTS_ON_GOAL],
                   period_number=period[DICT_KEY_NUM], ordinal_number=period[DICT_KEY_ORDINAL_NUM]))
        out[DICT_KEY_AWAY].append(
            Period(goals=period[DICT_KEY_AWAY][DICT_KEY_GOALS], shots=period[DICT_KEY_AWAY][DICT_KEY_SHOTS_ON_GOAL],
                   period_number=period[DICT_KEY_NUM], ordinal_number=period[DICT_KEY_ORDINAL_NUM]))
    return out


def parse_shootouts(feed_live: dict):
    shootout_info = feed_live[DICT_KEY_LIVE_DATA][DICT_KEY_LINE_SCORE][DICT_KEY_SHOOTOUT_INFO]
    return {
        DICT_KEY_HOME: Shootout(scores=shootout_info[DICT_KEY_HOME][DICT_KEY_SCORES],
                                attempts=shootout_info[DICT_KEY_HOME][DICT_KEY_ATTEMPTS],
                                has_been_played=feed_live[DICT_KEY_LIVE_DATA][DICT_KEY_LINE_SCORE][
                                    DICT_KEY_HAS_SHOOTOUT]),
        DICT_KEY_AWAY: Shootout(scores=shootout_info[DICT_KEY_AWAY][DICT_KEY_SCORES],
                                attempts=shootout_info[DICT_KEY_AWAY][DICT_KEY_ATTEMPTS],
                                has_been_played=feed_live[DICT_KEY_LIVE_DATA][DICT_KEY_LINE_SCORE][
                                    DICT_KEY_HAS_SHOOTOUT])
    }


def parse_team_stats(feed_live: dict):
    periods = parse_periods(feed_live)
    shootouts = parse_shootouts(feed_live)
    out = {}
    for key, team in feed_live[DICT_KEY_LIVE_DATA][DICT_KEY_BOX_SCORE][DICT_KEY_TEAMS].items():
        team_skater_stats = team[DICT_KEY_TEAM_STATS][DICT_KEY_TEAM_SKATER_STATS]
        out[key] = TeamStats(
            goals=feed_live[DICT_KEY_LIVE_DATA][DICT_KEY_LINE_SCORE][DICT_KEY_TEAMS][key][DICT_KEY_GOALS],
            shots=team_skater_stats[DICT_KEY_SHOTS],
            blocked=team_skater_stats[DICT_KEY_BLOCKED],
            hits=team_skater_stats[DICT_KEY_HITS],
            fo_wins=team_skater_stats[DICT_KEY_FO_WIN_PERCENTAGE],
            giveaways=team_skater_stats[DICT_KEY_GIVEAWAYS],
            takeaways=team_skater_stats[DICT_KEY_TAKEAWAYS],
            pp_opportunities=int(team_skater_stats[DICT_KEY_PP_OPPORTUNITIES]),
            pp_goals=int(team_skater_stats[DICT_KEY_PP_GOALS]),
            pp_percentage=team_skater_stats[DICT_KEY_PP_PERCENTAGE],
            periods=periods[key],
            shootout=shootouts[key])
    return out


def parse_game(game: dict, feed_live: dict):  # TODO: only use feed_live
    team_stats = parse_team_stats(feed_live)
    return Game(id=game[DICT_KEY_GAME_PK],
                away_team=game[DICT_KEY_TEAMS][DICT_KEY_AWAY][DICT_KEY_TEAM][DICT_KEY_NAME],
                home_team=game[DICT_KEY_TEAMS][DICT_KEY_HOME][DICT_KEY_TEAM][DICT_KEY_NAME],
                start_time=datetime_utils.parse_datetime(game[DICT_KEY_GAME_DATE]),
                game_clock=game[DICT_KEY_STATUS][DICT_KEY_DETAILED_STATE],
                home_team_stats=team_stats[DICT_KEY_HOME],
                away_team_stats=team_stats[DICT_KEY_AWAY])
