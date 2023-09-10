from dataclasses import dataclass
from datetime import datetime

from src.datatypes.team_stats import TeamStats


# TODO: replace team names with team objects
@dataclass
class Game:
    id: int
    away_team: str
    home_team: str
    start_time: datetime
    game_clock: str
    away_team_stats: TeamStats
    home_team_stats: TeamStats
