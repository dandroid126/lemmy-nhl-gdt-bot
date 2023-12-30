from typing import Optional

import pydash
import requests
import json
from src.datatypes.Exceptions.IllegalArgumentException import IllegalArgumentException
from src.datatypes.game_info import GameInfo
from src.datatypes.goal import Goal
from src.datatypes.penalty import Penalty
from src.datatypes.teams import Teams, get_team_from_id

from src.datatypes.game import Game
from src.datatypes.period import Period
from src.datatypes.shootout import Shootout
from src.datatypes.team_stats import TeamStats
from src.utils import logger, datetime_util

TAG = "nhl_api_client.py"

URL_REPL_GAME_ID = "{{GAME_ID}}"
URL_REPL_START_DATE = "{{START_DATE}}"
URL_REPL_END_DATE = "{{END_DATE}}"

BASE_URL = "https://statsapi.web.nhl.com/api/v1"
SCHEDULE_URL = f"{BASE_URL}/schedule?startDate={URL_REPL_START_DATE}&endDate={URL_REPL_END_DATE}&expand=schedule.broadcasts"
FEED_LIVE_URL = f"{BASE_URL}/game/{URL_REPL_GAME_ID}/feed/live"

DICT_KEY_DATES = 'dates'
LIST_KEY_FIRST = 0
DICT_KEY_GAMES = 'games'
DICT_KEY_GAME = 'game'
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
DICT_KEY_LINESCORE = 'linescore'
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
DICT_KEY_GAME_DATA = 'gameData'
DICT_KEY_ID = 'id'
DICT_KEY_ABBREVIATION = 'abbreviation'
DICT_KEY_PLAYS = 'plays'
DICT_KEY_ALL_PLAYS = 'allPlays'
DICT_KEY_SCORING_PLAYS = 'scoringPlays'
DICT_KEY_RESULT = 'result'
DICT_KEY_ABOUT = 'about'
DICT_KEY_PERIOD_TIME = 'periodTime'
DICT_KEY_TRI_CODE = 'triCode'
DICT_KEY_STRENGTH = 'strength'
DICT_KEY_DESCRIPTION = 'description'
DICT_KEY_EMPTY_NET = 'emptyNet'
DICT_KEY_PLAYERS = 'players'
DICT_KEY_PLAYER = 'player'
DICT_KEY_PLAYER_TYPE = 'playerType'
DICT_KEY_FULL_NAME = 'fullName'
DICT_KEY_DATETIME = 'datetime'
DICT_KEY_DATE_TIME = 'dateTime'  # WTF NHL??????? Why are these different?????
DICT_KEY_END_DATE_TIME = 'endDateTime'
DICT_KEY_CURRENT_PERIOD_TIME_REMAINING = 'currentPeriodTimeRemaining'
DICT_KEY_CURRENT_PERIOD_ORDINAL = 'currentPeriodOrdinal'
DICT_KEY_PK = 'pk'
DICT_KEY_PENALTY_PLAYS = 'penaltyPlays'
DICT_KEY_PENALTY_MINUTES = 'penaltyMinutes'
DICT_KEY_PENALTY_SEVERITY = 'penaltySeverity'

DICT_VALUE_GOALIE = 'Goalie'

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

EMPTY_NET = "Empty Net"
TIME_CLOCK_DEFAULT = "--"
PERIOD_DEFAULT = "0"
REQUEST_TIMEOUT = 10


def get_schedule_url(start_date: str, end_date: str) -> str:
    """
    Gets the schedule URL

    Args:
        start_date: the start date of the schedule
        end_date: the end date of the schedule

    Returns:
        str: the schedule URL
    """
    if start_date is None:
        raise IllegalArgumentException(TAG, "start_date must not be None")
    if end_date is None:
        raise IllegalArgumentException(TAG, "end_date must not be None")
    return SCHEDULE_URL.replace(URL_REPL_START_DATE, start_date).replace(URL_REPL_END_DATE, end_date)


def get_feed_live_url(game_id: int) -> str:
    """
    Gets the feed live URL

    Args:
        game_id: the ID of the game

    Returns:
        str: the feed live URL
    """
    if game_id is None:
        raise IllegalArgumentException(TAG, "game_id must not be None")
    return FEED_LIVE_URL.replace(URL_REPL_GAME_ID, str(game_id))


def get_schedule(start_date: str = None, end_date: str = None) -> list[Game]:
    """
    Gets the schedule

    Args:
        start_date: The start date of the schedule
        end_date: The end date of the schedule

    Returns:
        list[Game]: The schedule
    """
    if start_date is None:
        start_date = datetime_util.yesterday()
    if end_date is None:
        end_date = datetime_util.today()
    url = get_schedule_url(start_date, end_date)
    logger.i(TAG, f"get_schedule(): url: {url}")
    try:
        dates = pydash.get(json.loads(requests.get(url, timeout=REQUEST_TIMEOUT).text), DICT_KEY_DATES, [])
        games = []
        for date in dates:
            games.extend(pydash.get(date, DICT_KEY_GAMES, []))
        schedule = []
        for game in games:
            schedule.append(parse_scheduled_game(game))
    except requests.exceptions.Timeout as e:
        logger.e(TAG, "get_schedule(): a timeout occurred", e)
        schedule = []
    except requests.exceptions.ConnectionError as e:
        logger.e(TAG, "get_schedule(): A connection error occurred", e)
        schedule = []
    return schedule


def get_games(schedule: list[Game]) -> list[Game]:
    """
    Gets the games

    Args:
        schedule: The schedule

    Returns:
        list[Game]: The games
    """
    if not schedule:
        return []
    games = []
    for game in schedule:
        feed_live = get_feed_live(game.id)
        games.append(parse_game(feed_live))
    return games


def get_feed_live(game_id: int) -> dict:
    """
    Gets the feed live

    Args:
        game_id: the ID of the game

    Returns:
        dict: the feed live dictionary
    """
    if game_id is None:
        raise IllegalArgumentException(TAG, "game_id must not be None")
    url = get_feed_live_url(game_id)
    logger.i(TAG, f"get_feed_live(): url: {url}")
    try:
        box_score = json.loads(requests.get(url, timeout=REQUEST_TIMEOUT).text)
    except requests.exceptions.Timeout as e:
        logger.e(TAG, "get_games(): a timeout occured", e)
        box_score = {}
    except requests.exceptions.ConnectionError as e:
        logger.e(TAG, "get_feed_live(): A connection error occurred", e)
        box_score = {}
    return box_score


def parse_periods(feed_live: dict) -> dict:
    """
    Parses the periods

    Args:
        feed_live: the feed live dictionary

    Returns:
        dict: the parsed periods
    """
    out = {
        DICT_KEY_HOME: [],
        DICT_KEY_AWAY: []
    }
    periods = pydash.get(feed_live, f"{DICT_KEY_LIVE_DATA}.{DICT_KEY_LINESCORE}.{DICT_KEY_PERIODS}", [])
    for period in periods:
        home_goals = pydash.get(period, f"{DICT_KEY_HOME}.{DICT_KEY_GOALS}", -1)
        home_shots = pydash.get(period, f"{DICT_KEY_HOME}.{DICT_KEY_SHOTS_ON_GOAL}", -1)
        away_goals = pydash.get(period, f"{DICT_KEY_AWAY}.{DICT_KEY_GOALS}", -1)
        away_shots = pydash.get(period, f"{DICT_KEY_AWAY}.{DICT_KEY_SHOTS_ON_GOAL}", -1)
        period_number = pydash.get(period, DICT_KEY_NUM, -1)
        ordinal_number = pydash.get(period, DICT_KEY_ORDINAL_NUM, "-1")
        out[DICT_KEY_HOME].append(
            Period(goals=home_goals, shots=home_shots, period_number=period_number, ordinal_number=ordinal_number))
        out[DICT_KEY_AWAY].append(
            Period(goals=away_goals, shots=away_shots, period_number=period_number, ordinal_number=ordinal_number))
    return out


def parse_shootouts(feed_live: dict) -> dict:
    """
    Parses the shootouts

    Args:
        feed_live: the feed live dictionary

    Returns:
        dict: the parsed shootouts
    """
    shootout_info = pydash.get(feed_live, f"{DICT_KEY_LIVE_DATA}.{DICT_KEY_LINESCORE}.{DICT_KEY_SHOOTOUT_INFO}", {})
    return {
        DICT_KEY_HOME: Shootout(scores=pydash.get(shootout_info, f"{DICT_KEY_HOME}.{DICT_KEY_SCORES}", -1),
                                attempts=pydash.get(shootout_info, f"{DICT_KEY_HOME}.{DICT_KEY_ATTEMPTS}", -1),
                                has_been_played=pydash.get(feed_live, f"{DICT_KEY_LIVE_DATA}.{DICT_KEY_LINESCORE}.{DICT_KEY_HAS_SHOOTOUT}", False)),
        DICT_KEY_AWAY: Shootout(scores=pydash.get(shootout_info, f"{DICT_KEY_AWAY}.{DICT_KEY_SCORES}", -1),
                                attempts=pydash.get(shootout_info, f"{DICT_KEY_AWAY}.{DICT_KEY_ATTEMPTS}", -1),
                                has_been_played=pydash.get(feed_live, f"{DICT_KEY_LIVE_DATA}.{DICT_KEY_LINESCORE}.{DICT_KEY_HAS_SHOOTOUT}", False)),
    }


def parse_game_info(feed_live: dict) -> GameInfo:
    """
    Parses the game info

    Args:
        feed_live: the feed live dictionary

    Returns:
        GameInfo: the parsed game info
    """
    return GameInfo(
        current_period=pydash.get(feed_live, f"{DICT_KEY_LIVE_DATA}.{DICT_KEY_LINESCORE}.{DICT_KEY_CURRENT_PERIOD_ORDINAL}", ""),
        game_clock=pydash.get(feed_live, f"{DICT_KEY_LIVE_DATA}.{DICT_KEY_LINESCORE}.{DICT_KEY_CURRENT_PERIOD_TIME_REMAINING}", TIME_CLOCK_DEFAULT),
    )


def parse_goals(feed_live: dict) -> list[Goal]:
    """
    Parses the goals

    Args:
        feed_live: the feed live dictionary

    Returns:
        list[Goal]: the parsed goals
    """
    scoring_plays = pydash.get(feed_live, f"{DICT_KEY_LIVE_DATA}.{DICT_KEY_PLAYS}.{DICT_KEY_SCORING_PLAYS}", [])
    goals = []
    for play in scoring_plays:
        scoring_play_details = pydash.get(feed_live, f"{DICT_KEY_LIVE_DATA}.{DICT_KEY_PLAYS}.{DICT_KEY_ALL_PLAYS}.{play}", {})
        goalie = EMPTY_NET
        for player in pydash.get(scoring_play_details, DICT_KEY_PLAYERS, []):
            if pydash.get(player, DICT_KEY_PLAYER_TYPE, "") == DICT_VALUE_GOALIE:
                # NOTE: if the player's last name has a space in it, this won't work.
                #  If that ever happens, do it the long way.
                #  Map the player's ID to the "players" list in JSON[gameData][players][ID...]
                goalie = pydash.get(player,f"{DICT_KEY_PLAYER}.{DICT_KEY_FULL_NAME}", "").split(" ")[-1]
        goals.append(Goal(period=pydash.get(scoring_play_details, f"{DICT_KEY_ABOUT}.{DICT_KEY_ORDINAL_NUM}", ""),
                          time=pydash.get(scoring_play_details, f"{DICT_KEY_ABOUT}.{DICT_KEY_PERIOD_TIME}", ""),
                          team=Teams[pydash.get(scoring_play_details, f"{DICT_KEY_TEAM}.{DICT_KEY_TRI_CODE}", "ERR")].value,
                          strength=pydash.get(scoring_play_details, f"{DICT_KEY_RESULT}.{DICT_KEY_STRENGTH}.{DICT_KEY_NAME}", ""),
                          goalie=goalie,
                          description=pydash.get(scoring_play_details, f"{DICT_KEY_RESULT}.{DICT_KEY_DESCRIPTION}", "")))
    return goals


def parse_penalties(feed_live: dict) -> list[Penalty]:
    """
    Parses the penalties

    Args:
        feed_live: the feed live dictionary

    Returns:
        list[Penalty]: the parsed penalties
    """
    penalty_plays = pydash.get(feed_live, f"{DICT_KEY_LIVE_DATA}.{DICT_KEY_PLAYS}.{DICT_KEY_PENALTY_PLAYS}", [])
    penalties = []
    for play in penalty_plays:
        penalty_play_details = pydash.get(feed_live, f"{DICT_KEY_LIVE_DATA}.{DICT_KEY_PLAYS}.{DICT_KEY_ALL_PLAYS}.{play}", {})
        penalties.append(Penalty(period=pydash.get(penalty_play_details, f"{DICT_KEY_ABOUT}.{DICT_KEY_ORDINAL_NUM}", ""),
                                 time=pydash.get(penalty_play_details, f"{DICT_KEY_ABOUT}.{DICT_KEY_PERIOD_TIME}", ""),
                                 team=Teams[pydash.get(penalty_play_details, f"{DICT_KEY_TEAM}.{DICT_KEY_TRI_CODE}", "ERR")].value,
                                 type=pydash.get(penalty_play_details, f"{DICT_KEY_RESULT}.{DICT_KEY_PENALTY_SEVERITY}", ""),
                                 min=pydash.get(penalty_play_details, f"{DICT_KEY_RESULT}.{DICT_KEY_PENALTY_MINUTES}", -1),
                                 description=pydash.get(penalty_play_details, f"{DICT_KEY_RESULT}.{DICT_KEY_DESCRIPTION}", "")))
    return penalties


def parse_team_stats(feed_live: dict) -> dict:
    """
    Parses the team stats

    Args:
        feed_live: the feed live dictionary

    Returns:
        dict: the parsed team stats
    """
    periods = parse_periods(feed_live)
    shootouts = parse_shootouts(feed_live)
    out = {}
    for key, team in pydash.get(feed_live, f"{DICT_KEY_LIVE_DATA}.{DICT_KEY_BOX_SCORE}.{DICT_KEY_TEAMS}", {}).items():
        team_skater_stats = pydash.get(team, f"{DICT_KEY_TEAM_STATS}.{DICT_KEY_TEAM_SKATER_STATS}", {})
        out[key] = TeamStats(
            goals=pydash.get(feed_live, f"{DICT_KEY_LIVE_DATA}.{DICT_KEY_LINESCORE}.{DICT_KEY_TEAMS}.{key}.{DICT_KEY_GOALS}", ""),
            shots=pydash.get(team_skater_stats, f"{DICT_KEY_SHOTS}", ""),
            blocked=pydash.get(team_skater_stats, f"{DICT_KEY_BLOCKED}", ""),
            hits=pydash.get(team_skater_stats, f"{DICT_KEY_HITS}", ""),
            fo_wins=pydash.get(team_skater_stats, f"{DICT_KEY_FO_WIN_PERCENTAGE}", ""),
            giveaways=pydash.get(team_skater_stats, f"{DICT_KEY_GIVEAWAYS}", ""),
            takeaways=pydash.get(team_skater_stats, f"{DICT_KEY_TAKEAWAYS}", ""),
            pp_opportunities=int(pydash.get(team_skater_stats, f"{DICT_KEY_PP_OPPORTUNITIES}", -1)),
            pp_goals=int(pydash.get(team_skater_stats, f"{DICT_KEY_PP_GOALS}", -1)),
            pp_percentage=pydash.get(team_skater_stats, f"{DICT_KEY_PP_PERCENTAGE}", ""),
            periods=pydash.get(periods, key, []),
            shootout=pydash.get(shootouts, key, None))
    return out


def parse_scheduled_game(game: dict) -> Optional[Game]:
    """
    Parses the scheduled game

    Args:
        game: the game dictionary

    Returns:
        Optional[Game]: the parsed game or None if it cannot be parsed
    """
    game_id = pydash.get(game, f"{DICT_KEY_GAME_PK}", None)
    away_team_id = pydash.get(game, f"{DICT_KEY_TEAMS}.{DICT_KEY_AWAY}.{DICT_KEY_TEAM}.{DICT_KEY_ID}", None)
    home_team_id = pydash.get(game, f"{DICT_KEY_TEAMS}.{DICT_KEY_HOME}.{DICT_KEY_TEAM}.{DICT_KEY_ID}", None)
    start_time = pydash.get(game, f"{DICT_KEY_GAME_DATE}", None)

    if not game_id or not away_team_id or not home_team_id or not start_time:
        return None

    away_team = get_team_from_id(away_team_id)
    home_team = get_team_from_id(home_team_id)

    if not away_team or not home_team:
        return None

    return Game(id=game_id,
                away_team=away_team,
                home_team=home_team,
                start_time=datetime_util.parse_datetime(start_time),
                end_time=None,
                game_info=GameInfo(current_period=PERIOD_DEFAULT, game_clock=TIME_CLOCK_DEFAULT),
                home_team_stats=None,
                away_team_stats=None,
                goals=None,
                penalties=None)


def parse_game(feed_live: dict) -> Optional[Game]:
    """
    Parses the game

    Args:
        feed_live: the feed live dictionary

    Returns:
        Optional[Game]: the parsed game or None if it cannot be parsed
    """
    team_stats = parse_team_stats(feed_live)

    game_id = pydash.get(feed_live, f"{DICT_KEY_GAME_DATA}.{DICT_KEY_GAME}.{DICT_KEY_PK}", None)
    away_team_abbr = pydash.get(feed_live, f"{DICT_KEY_GAME_DATA}.{DICT_KEY_TEAMS}.{DICT_KEY_AWAY}.{DICT_KEY_ABBREVIATION}", None)
    home_team_abbr = pydash.get(feed_live, f"{DICT_KEY_GAME_DATA}.{DICT_KEY_TEAMS}.{DICT_KEY_HOME}.{DICT_KEY_ABBREVIATION}", None)
    start_time = pydash.get(feed_live, f"{DICT_KEY_GAME_DATA}.{DICT_KEY_DATETIME}.{DICT_KEY_DATE_TIME}", None)
    end_time = pydash.get(feed_live, f"{DICT_KEY_GAME_DATA}.{DICT_KEY_DATETIME}.{DICT_KEY_END_DATE_TIME}", None)
    if end_time is not None:
        end_time = datetime_util.parse_datetime(end_time)
    home_team_stats = pydash.get(team_stats, f"{DICT_KEY_HOME}", None)
    away_team_stats = pydash.get(team_stats, f"{DICT_KEY_AWAY}", None)

    if game_id is None or away_team_abbr is None or home_team_abbr is None or start_time is None or home_team_stats is None or away_team_stats is None:
        return None

    return Game(id=game_id,
                away_team=Teams[away_team_abbr].value,
                home_team=Teams[home_team_abbr].value,
                start_time=datetime_util.parse_datetime(start_time),
                end_time=end_time,
                game_info=parse_game_info(feed_live),
                home_team_stats=home_team_stats,
                away_team_stats=away_team_stats,
                goals=parse_goals(feed_live),
                penalties=parse_penalties(feed_live))
