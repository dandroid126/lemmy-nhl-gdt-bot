import json
from enum import Enum
from typing import Optional

import pydash
import requests
import inflect

from src.datatypes.Exceptions.IllegalArgumentException import IllegalArgumentException
from src.datatypes.game import Game
from src.datatypes.game_info import GameInfo
from src.datatypes.goal import Goal
from src.datatypes.penalty import Penalty
from src.datatypes.period import Period
from src.datatypes.shootout import Shootout
from src.datatypes.team_stats import TeamStats
from src.datatypes.teams import Teams, get_team_from_id
from src.utils import logger, datetime_util

TAG = "nhl_api_client.py"

URL_REPL_ID = "{{ID}}"
URL_REPL_DATE = "{{DATE}}"

NHL_API_BASE_URL = "https://api-web.nhle.com/v1"
SCHEDULE_URL = f"{NHL_API_BASE_URL}/schedule/{URL_REPL_DATE}"
LANDING_URL = f"{NHL_API_BASE_URL}/gamecenter/{URL_REPL_ID}/landing"

VIDEO_BASE_URL = "https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId="
VIDEO_URL = f"{VIDEO_BASE_URL}{URL_REPL_ID}"

DICT_KEY_GAMES = 'games'
DICT_KEY_START_TIME_UTC = 'startTimeUTC'
DICT_KEY_HOME_TEAM = 'homeTeam'
DICT_KEY_AWAY_TEAM = 'awayTeam'
DICT_KEY_AWAY = 'away'
DICT_KEY_HOME = 'home'
DICT_KEY_TEAM_ABBREV = 'teamAbbrev'
DICT_KEY_ABBREV = 'abbrev'
DICT_KEY_LINESCORE = 'linescore'
DICT_KEY_PERIOD = 'period'
DICT_KEY_PERIOD_DESCRIPTOR = 'periodDescriptor'
DICT_KEY_SHOOTOUT = 'shootout'
DICT_KEY_HOME_CONVERSIONS = 'homeConversions'
DICT_KEY_AWAY_CONVERSIONS = 'awayConversions'
DICT_KEY_HOME_ATTEMPTS = 'homeAttempts'
DICT_KEY_AWAY_ATTEMPTS = 'awayAttempts'
DICT_KEY_ID = 'id'
DICT_KEY_TIME_IN_PERIOD = 'timeInPeriod'
DICT_KEY_STRENGTH = 'strength'
DICT_KEY_EMPTY_NET = 'emptyNet'
DICT_KEY_CLOCK = 'clock'
DICT_KEY_TIME_REMAINING = 'timeRemaining'
DICT_KEY_PENALTIES = 'penalties'
DICT_KEY_GAME_WEEK = 'gameWeek'
DICT_KEY_SUMMARY = 'summary'
DICT_KEY_SHOTS_BY_PERIOD = 'shotsByPeriod'
DICT_KEY_BY_PERIOD = 'byPeriod'
DICT_KEY_SCORING = 'scoring'
DICT_KEY_GOALS = 'goals'
DICT_KEY_HIGHLIGHT_CLIP = 'highlightClip'
DICT_KEY_SEASON_SERIES = 'seasonSeries'
DICT_KEY_IN_INTERMISSION = 'inIntermission'
DICT_KEY_GAME_STATE = 'gameState'
DICT_KEY_DEFAULT = 'default'

DICT_KEY_FIRST_NAME = 'firstName'
DICT_KEY_LAST_NAME = 'lastName'
DICT_KEY_GOALS_TO_DATE = 'goalsToDate'
DICT_KEY_SHOT_TYPE = 'shotType'
DICT_KEY_ASSISTS = 'assists'
DICT_KEY_ASSISTS_TO_DATE = 'assistsToDate'

DICT_KEY_TYPE = 'type'
DICT_KEY_DURATION = 'duration'
DICT_KEY_COMMITTED_BY_PLAYER = 'committedByPlayer'
DICT_KEY_DRAWN_BY = 'drawnBy'
DICT_KEY_DESC_KEY = 'descKey'

DICT_VALUE_GOALIE = 'Goalie'

# Team Stats
DICT_KEY_TEAM_GAME_STATS = 'teamGameStats'
DICT_KEY_CATEGORY = 'category'
DICT_KEY_HOME_VALUE = 'homeValue'
DICT_KEY_AWAY_VALUE = 'awayValue'
DICT_KEY_TOTALS = 'totals'


class TeamStatCategories(Enum):
    SOG = 'sog'
    FACEOFF_PCTG = 'faceoffPctg'
    POWER_PLAY = 'powerPlay'
    PIM = 'pim'
    HITS = 'hits'
    BLOCKED_SHOTS = 'blockedShots'
    GIVEAWAYS = 'giveaways'
    TAKEAWAYS = 'takeaways'


class GameState(Enum):
    FUT = "FUT"
    PRE = "PRE"
    LIVE = "LIVE"
    FINAL = "FINAL"
    OFF = "OFF"


EMPTY_NET = "Empty Net"
TIME_CLOCK_DEFAULT = "--"
PERIOD_DEFAULT = "0"
REQUEST_TIMEOUT = 10
INTERMISSION_TIME_CLOCK = "INT"

p = inflect.engine()


def get_schedule_url(date: str) -> str:
    """
    Gets the schedule URL

    Args:
        date: the date to get the schedule for

    Returns:
        str: the schedule URL
    """
    if date is None:
        raise IllegalArgumentException(TAG, "start_date must not be None")
    return SCHEDULE_URL.replace(URL_REPL_DATE, date)


def get_landing_url(game_id: int) -> str:
    """
    Gets the feed live URL

    Args:
        game_id: the ID of the game

    Returns:
        str: the feed live URL
    """
    if game_id is None:
        raise IllegalArgumentException(TAG, "game_id must not be None")
    return LANDING_URL.replace(URL_REPL_ID, str(game_id))


def get_video_url(video_id: int) -> str:
    """
    Gets the video URL

    Args:
        video_id: the ID of the video

    Returns:
        str: the video URL
    """
    if video_id is None or video_id == 0:
        logger.w(TAG, "video_id is None or 0. Returning empty string.")
        return ""
    return VIDEO_URL.replace(URL_REPL_ID, str(video_id))


def filter_games_by_date(games: list[Game], date: str) -> list[Game]:
    """
    Filters games by date

    Args:
        games: The games to filter
        date: The date to match

    Returns:
        list[Game]: The filtered games
    """
    return list(filter(lambda game: datetime_util.is_same_day(game.start_time, date) if game else None, games))


def get_schedule(schedule_date: str = None) -> list[Game]:
    """
    Gets the schedule

    Args:
        schedule_date: the date of the schedule

    Returns:
        list[Game]: The schedule
    """
    if schedule_date is None:
        schedule_date = datetime_util.get_current_day_as_idlw()
    url = get_schedule_url(schedule_date)
    logger.i(TAG, f"get_schedule(): url: {url}")
    try:
        game_week = pydash.get(json.loads(requests.get(url, timeout=REQUEST_TIMEOUT).text), DICT_KEY_GAME_WEEK, [])
        games = []
        for date in game_week:
            game_list = pydash.get(date, DICT_KEY_GAMES, [])
            for game in game_list:
                games.append(game)
        schedule = []
        for game in games:
            schedule.append(parse_scheduled_game(game))
        schedule = filter_games_by_date(schedule, schedule_date)
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
        landing = get_landing(game.id)
        games.append(parse_game(landing))
    return games


def get_landing(game_id: int) -> dict:
    """
    Gets the landing

    Args:
        game_id: the ID of the game

    Returns:
        dict: the landing dictionary
    """
    if game_id is None:
        raise IllegalArgumentException(TAG, "game_id must not be None")
    url = get_landing_url(game_id)
    logger.i(TAG, f"get_landing(): url: {url}")
    try:
        landing = json.loads(requests.get(url, timeout=REQUEST_TIMEOUT).text)
    except requests.exceptions.Timeout as e:
        logger.e(TAG, "get_landing(): a timeout occurred", e)
        landing = {}
    except requests.exceptions.ConnectionError as e:
        logger.e(TAG, "get_landing(): A connection error occurred", e)
        landing = {}
    return landing


def parse_periods(landing: dict) -> dict:
    """
    Parses the periods

    Args:
        landing: the landing dictionary

    Returns:
        dict: the parsed periods
    """
    out = {
        DICT_KEY_HOME: [],
        DICT_KEY_AWAY: []
    }
    shots_by_period = pydash.get(landing, f"{DICT_KEY_SUMMARY}.{DICT_KEY_SHOTS_BY_PERIOD}", [])
    linescore_by_period = pydash.get(landing, f"{DICT_KEY_SUMMARY}.{DICT_KEY_LINESCORE}.{DICT_KEY_BY_PERIOD}", [])
    if not len(shots_by_period) == len(linescore_by_period):
        logger.e(TAG, "parse_periods(): shots_by_period and linescore_by_period must have the same length")
        return out
    for i in range(0, len(shots_by_period)):
        home_goals = pydash.get(linescore_by_period[i], f"{DICT_KEY_HOME}", 0)
        home_shots = pydash.get(shots_by_period[i], f"{DICT_KEY_HOME}", 0)
        away_goals = pydash.get(linescore_by_period[i], f"{DICT_KEY_AWAY}", 0)
        away_shots = pydash.get(shots_by_period[i], f"{DICT_KEY_AWAY}", 0)
        period_number = pydash.get(shots_by_period[i], DICT_KEY_PERIOD, 0)
        ordinal_number = get_period_ordinal(period_number)
        out[DICT_KEY_HOME].append(
            Period(goals=home_goals, shots=home_shots, period_number=period_number, ordinal_number=ordinal_number))
        out[DICT_KEY_AWAY].append(
            Period(goals=away_goals, shots=away_shots, period_number=period_number, ordinal_number=ordinal_number))
    return out


def get_period_ordinal(period_number: int) -> str:
    if period_number in range(1, 4):
        return p.ordinal(period_number)
    elif period_number == 4:
        return "OT"
    elif period_number == 5:
        return "SO"
    else:
        return ""


def parse_shootouts(landing: dict) -> dict:
    """
    Parses the shootouts

    Args:
        landing: the landing dictionary

    Returns:
        dict: the parsed shootouts
    """
    shootout_info = pydash.get(landing, f"{DICT_KEY_SUMMARY}.{DICT_KEY_LINESCORE}.{DICT_KEY_SHOOTOUT}", {})
    return {
        DICT_KEY_HOME: Shootout(scores=pydash.get(shootout_info, f"{DICT_KEY_HOME_CONVERSIONS}", 0),
                                attempts=pydash.get(shootout_info, f"{DICT_KEY_HOME_ATTEMPTS}", 0),
                                has_been_played=not shootout_info == {}),
        DICT_KEY_AWAY: Shootout(scores=pydash.get(shootout_info, f"{DICT_KEY_AWAY_CONVERSIONS}", 0),
                                attempts=pydash.get(shootout_info, f"{DICT_KEY_AWAY_ATTEMPTS}", 0),
                                has_been_played=not shootout_info == {}),
    }


def parse_game_info(landing: dict) -> GameInfo:
    """
    Parses the game info

    Args:
        landing: the landing dictionary

    Returns:
        GameInfo: the parsed game info
    """
    current_period = ""
    season_series = pydash.get(landing, f"{DICT_KEY_SUMMARY}.{DICT_KEY_SEASON_SERIES}", [])
    for game in season_series:
        if pydash.get(game, DICT_KEY_ID, 0) == pydash.get(landing, DICT_KEY_ID, -1):
            current_period = get_period_ordinal(pydash.get(game, f"{DICT_KEY_PERIOD}", ""))
    in_intermission = pydash.get(landing, f"{DICT_KEY_CLOCK}.{DICT_KEY_IN_INTERMISSION}", False)
    is_final = pydash.get(landing, f"{DICT_KEY_GAME_STATE}", "")

    if is_final == GameState.FINAL.value or is_final == GameState.OFF.value:
        game_clock = GameState.FINAL.value
    elif in_intermission:
        game_clock = INTERMISSION_TIME_CLOCK
    else:
        game_clock = pydash.get(landing, f"{DICT_KEY_CLOCK}.{DICT_KEY_TIME_REMAINING}", TIME_CLOCK_DEFAULT)

    return GameInfo(
        current_period=current_period if current_period else "",
        game_clock=game_clock,
    )


def parse_goals(landing: dict) -> list[Goal]:
    """
    Parses the goals

    Args:
        landing: the landing dictionary

    Returns:
        list[Goal]: the parsed goals
    """
    periods = pydash.get(landing, f"{DICT_KEY_SUMMARY}.{DICT_KEY_SCORING}", [])
    goals = []
    for period in periods:
        scoring_plays = pydash.get(period, f"{DICT_KEY_GOALS}", [])
        for play in scoring_plays:
            team = pydash.get(play, f"{DICT_KEY_TEAM_ABBREV}", "ERR")
            if type(team) is dict:
                team = pydash.get(team, DICT_KEY_DEFAULT, "ERR")
            strength = pydash.get(play, f"{DICT_KEY_STRENGTH}", "")
            goals.append(Goal(period=get_period_ordinal(pydash.get(period, f"{DICT_KEY_PERIOD}", 0)),
                              time=pydash.get(play, f"{DICT_KEY_TIME_IN_PERIOD}", ""),
                              team=Teams[team].value,
                              strength=strength_map.get(strength, strength),
                              goalie="",
                              description=get_goal_description(play),
                              video_url=get_video_url(pydash.get(play, f"{DICT_KEY_HIGHLIGHT_CLIP}", 0)),
                              ))
    return goals


strength_map = {
    "ev": "Even Strength",
    "pp": "Power Play",
    "sh": "Short Handed",
    "": "",
}

def get_goal_description(goal_dictionary: dict) -> str:
    """
    Get the description of the goal
    Example output: "Joe Pavelski (8) snap shot, assists: Joe Thornton (8), Logan Couture (8)"

    Args:
        goal_dictionary:

    Returns:
        str: The description of the goal
    """
    scorer_first_name = pydash.get(goal_dictionary, f"{DICT_KEY_FIRST_NAME}", "")
    if type(scorer_first_name) is dict:
        scorer_first_name = pydash.get(scorer_first_name, f"{DICT_KEY_DEFAULT}", "")
    scorer_last_name = pydash.get(goal_dictionary, f"{DICT_KEY_LAST_NAME}", "")
    if type(scorer_last_name) is dict:
        scorer_last_name = pydash.get(scorer_last_name, f"{DICT_KEY_DEFAULT}", "")
    goals_to_date = pydash.get(goal_dictionary, f"{DICT_KEY_GOALS_TO_DATE}", "")
    shot_type = pydash.get(goal_dictionary, f"{DICT_KEY_SHOT_TYPE}", "")

    assisted_by = []
    for player in pydash.get(goal_dictionary, f"{DICT_KEY_ASSISTS}", []):
        assistant_first_name = pydash.get(player, f"{DICT_KEY_FIRST_NAME}", "")
        if type(assistant_first_name) is dict:
            assistant_first_name = pydash.get(assistant_first_name, f"{DICT_KEY_DEFAULT}", "")
        assistant_last_name = pydash.get(player, f"{DICT_KEY_LAST_NAME}", "")
        if type(assistant_last_name) is dict:
            assistant_last_name = pydash.get(assistant_last_name, f"{DICT_KEY_DEFAULT}", "")
        assists_to_date = pydash.get(player, f"{DICT_KEY_ASSISTS_TO_DATE}", "")
        assisted_by.append(f"{assistant_first_name} {assistant_last_name} ({assists_to_date})")
    if len(assisted_by) == 0:
        assisted_by = ["None"]

    return f'{scorer_first_name} {scorer_last_name} ({goals_to_date}) {shot_type} shot, assists: {", ".join(assisted_by)}'


# shot_type_map = {
#     "snap": "Snap Shot",
#     "slap": "Slap Shot",
# }


def parse_penalties(landing: dict) -> list[Penalty]:
    """
    Parses the penalties

    Args:
        landing: the landing dictionary

    Returns:
        list[Penalty]: the parsed penalties
    """
    periods = pydash.get(landing, f"{DICT_KEY_SUMMARY}.{DICT_KEY_PENALTIES}", [])
    penalties = []
    for period in periods:
        penalty_plays = pydash.get(period, f"{DICT_KEY_PENALTIES}", [])
        for penalty in penalty_plays:
            penalty_type = pydash.get(penalty, f"{DICT_KEY_TYPE}", "")
            penalties.append(Penalty(period=get_period_ordinal(pydash.get(period, f"{DICT_KEY_PERIOD}", 0)),
                                     time=pydash.get(penalty, f"{DICT_KEY_TIME_IN_PERIOD}", ""),
                                     team=Teams[pydash.get(penalty, f"{DICT_KEY_TEAM_ABBREV}", "ERR")].value,
                                     type=penalty_type_map.get(penalty_type, penalty_type),  # If penalty type is not in the map, use the value itself as a default
                                     min=pydash.get(penalty, f"{DICT_KEY_DURATION}", 0),
                                     description=get_penalty_description(penalty)
                                     ))
    return penalties


penalty_type_map = {
    "MIN": "Minor",
    "MAJ": "Major",
    "BEN": "Bench",
    "MIS": "Misconduct",
    "GAM": "Game Misconduct",
    "MAT": "Match Penalty",
    "PS": "Penalty Shot",
}

penalty_description_map = {
    "delaying-game-puck-over-glass": "Puck Over Glass",
    "holding": "Holding",
    "hooking": "Hooking",
    "roughing": "Roughing",
    "embellishment": "Embellishment",
    "slashing": "Slashing",
}


def get_penalty_description(penalty_dictionary: dict) -> str:
    """
    Get the description of the penalty
    Example output: "Nick Foligno hooking against Miro Heiskanen"

    Args:
        penalty_dictionary:

    Returns:
        str: The description of the penalty
    """
    # TODO: add "served by" for applicable penalties
    committed_by = pydash.get(penalty_dictionary, f"{DICT_KEY_COMMITTED_BY_PLAYER}", "")
    description_key = pydash.get(penalty_dictionary, f"{DICT_KEY_DESC_KEY}", "")
    drawn_by = pydash.get(penalty_dictionary, f"{DICT_KEY_DRAWN_BY}", "")

    out = f'{committed_by} {description_key}'
    if drawn_by:
        out += f' against {drawn_by}'
    return out


def parse_team_stats(landing: dict) -> dict:
    """
    Parses the team stats

    Args:
        landing: the landing dictionary

    Returns:
        dict: the parsed team stats
    """
    periods = parse_periods(landing)
    shootouts = parse_shootouts(landing)
    out = {}
    home_shots = 0
    away_shots = 0
    home_fo_wins = "0"
    away_fo_wins = "0"
    home_pp = "0/0"
    away_pp = "0/0"
    home_blocked = 0
    away_blocked = 0
    home_hits = 0
    away_hits = 0
    home_takeaways = 0
    away_takeaways = 0
    home_giveaways = 0
    away_giveaways = 0

    home_goals = pydash.get(landing, f"{DICT_KEY_SUMMARY}.{DICT_KEY_LINESCORE}.{DICT_KEY_TOTALS}.{DICT_KEY_HOME}", 0)
    away_goals = pydash.get(landing, f"{DICT_KEY_SUMMARY}.{DICT_KEY_LINESCORE}.{DICT_KEY_TOTALS}.{DICT_KEY_AWAY}", 0)

    team_game_stats = pydash.get(landing, f"{DICT_KEY_SUMMARY}.{DICT_KEY_TEAM_GAME_STATS}", {})
    for stat in team_game_stats:
        category = pydash.get(stat, DICT_KEY_CATEGORY, "")
        match category:
            case TeamStatCategories.SOG.value:
                home_shots = int(pydash.get(stat, f"{DICT_KEY_HOME_VALUE}", 0))
                away_shots = int(pydash.get(stat, f"{DICT_KEY_AWAY_VALUE}", 0))
            case TeamStatCategories.FACEOFF_PCTG.value:
                home_fo_wins = pydash.get(stat, f"{DICT_KEY_HOME_VALUE}", "0")
                away_fo_wins = pydash.get(stat, f"{DICT_KEY_AWAY_VALUE}", "0")
            case TeamStatCategories.POWER_PLAY.value:
                home_pp = pydash.get(stat, f"{DICT_KEY_HOME_VALUE}", "0/0")
                away_pp = pydash.get(stat, f"{DICT_KEY_AWAY_VALUE}", "0/0")
            case TeamStatCategories.PIM.value:
                # Currently not storing this data
                pass
            case TeamStatCategories.HITS.value:
                home_hits = int(pydash.get(stat, f"{DICT_KEY_HOME_VALUE}", 0))
                away_hits = int(pydash.get(stat, f"{DICT_KEY_AWAY_VALUE}", 0))
            case TeamStatCategories.BLOCKED_SHOTS.value:
                home_blocked = int(pydash.get(stat, f"{DICT_KEY_HOME_VALUE}", 0))
                away_blocked = int(pydash.get(stat, f"{DICT_KEY_AWAY_VALUE}", 0))
            case TeamStatCategories.GIVEAWAYS.value:
                home_giveaways = int(pydash.get(stat, f"{DICT_KEY_HOME_VALUE}", 0))
                away_giveaways = int(pydash.get(stat, f"{DICT_KEY_AWAY_VALUE}", 0))
            case TeamStatCategories.TAKEAWAYS.value:
                home_takeaways = int(pydash.get(stat, f"{DICT_KEY_HOME_VALUE}", 0))
                away_takeaways = int(pydash.get(stat, f"{DICT_KEY_AWAY_VALUE}", 0))
            case _:
                logger.e(TAG, f"parse_team_stats: Unknown stat category: {category}")

    out[DICT_KEY_HOME] = TeamStats(
        goals=home_goals,
        shots=home_shots,
        blocked=home_blocked,
        hits=home_hits,
        fo_wins=home_fo_wins,
        giveaways=home_giveaways,
        takeaways=home_takeaways,
        pp_fraction=home_pp,
        periods=pydash.get(periods, DICT_KEY_HOME, []),
        shootout=pydash.get(shootouts, DICT_KEY_HOME, None)
    )

    out[DICT_KEY_AWAY] = TeamStats(
        goals=away_goals,
        shots=away_shots,
        blocked=away_blocked,
        hits=away_hits,
        fo_wins=away_fo_wins,
        giveaways=away_giveaways,
        takeaways=away_takeaways,
        pp_fraction=away_pp,
        periods=pydash.get(periods, DICT_KEY_AWAY, []),
        shootout=pydash.get(shootouts, DICT_KEY_AWAY, None)
    )
    return out


def parse_scheduled_game(game: dict) -> Optional[Game]:
    """
    Parses the scheduled game

    Args:
        game: the game dictionary

    Returns:
        Optional[Game]: the parsed game or None if it cannot be parsed
    """
    game_id = pydash.get(game, f"{DICT_KEY_ID}", None)
    away_team_id = pydash.get(game, f"{DICT_KEY_AWAY_TEAM}.{DICT_KEY_ID}", None)
    home_team_id = pydash.get(game, f"{DICT_KEY_HOME_TEAM}.{DICT_KEY_ID}", None)
    start_time = pydash.get(game, f"{DICT_KEY_START_TIME_UTC}", None)

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


def parse_game(landing: dict) -> Optional[Game]:
    """
    Parses the game

    Args:
        landing: the landing dictionary

    Returns:
        Optional[Game]: the parsed game or None if it cannot be parsed
    """
    team_stats = parse_team_stats(landing)

    game_id = pydash.get(landing, f"{DICT_KEY_ID}", None)
    away_team_abbr = pydash.get(landing, f"{DICT_KEY_AWAY_TEAM}.{DICT_KEY_ABBREV}", None)
    home_team_abbr = pydash.get(landing, f"{DICT_KEY_HOME_TEAM}.{DICT_KEY_ABBREV}", None)
    start_time = pydash.get(landing, f"{DICT_KEY_START_TIME_UTC}", None)
    end_time = None
    home_team_stats = pydash.get(team_stats, f"{DICT_KEY_HOME}", None)
    away_team_stats = pydash.get(team_stats, f"{DICT_KEY_AWAY}", None)

    if game_id is None or away_team_abbr is None or home_team_abbr is None or start_time is None or home_team_stats is None or away_team_stats is None:
        return None

    return Game(id=game_id,
                away_team=Teams[away_team_abbr].value,
                home_team=Teams[home_team_abbr].value,
                start_time=datetime_util.parse_datetime(start_time),
                end_time=end_time,
                game_info=parse_game_info(landing),
                home_team_stats=home_team_stats,
                away_team_stats=away_team_stats,
                goals=parse_goals(landing),
                penalties=parse_penalties(landing))
