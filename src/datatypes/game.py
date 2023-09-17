from dataclasses import dataclass
from datetime import datetime

from src.datatypes.goal import Goal
from src.datatypes.teams import Team
from src.datatypes.team_stats import TeamStats


# TODO: replace team names with team objects
@dataclass
class Game:
    id: int
    away_team: Team
    home_team: Team
    start_time: datetime
    game_clock: str
    away_team_stats: TeamStats
    home_team_stats: TeamStats
    goals: [Goal]
