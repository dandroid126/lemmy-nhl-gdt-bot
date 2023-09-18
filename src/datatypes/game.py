from dataclasses import dataclass
from datetime import datetime

from src.datatypes.goal import Goal
from src.datatypes.penalty import Penalty
from src.datatypes.teams import Team
from src.datatypes.team_stats import TeamStats


@dataclass
class Game:
    id: int
    away_team: Team
    home_team: Team
    start_time: datetime
    end_time: datetime
    game_clock: str
    away_team_stats: TeamStats
    home_team_stats: TeamStats
    goals: [Goal]
    penalties: [Penalty]
