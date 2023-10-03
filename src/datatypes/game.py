from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from src.datatypes.game_info import GameInfo
from src.datatypes.goal import Goal
from src.datatypes.penalty import Penalty
from src.datatypes.teams import Team
from src.datatypes.team_stats import TeamStats


class GameType(Enum):
    PRESEASON = 1
    REGULAR = 2
    POSTSEASON = 3
    ALLSTAR = 4


@dataclass
class Game:
    id: int
    away_team: Team
    home_team: Team
    start_time: datetime
    end_time: datetime
    game_info: GameInfo
    away_team_stats: TeamStats
    home_team_stats: TeamStats
    goals: [Goal]
    penalties: [Penalty]

    # This gets the game type by retrieving the 6th character in the game id.
    # 1 -> preseason
    # 2 -> regular season
    # 3 -> postseason
    # 4 -> allstar
    def get_game_type(self):
        return GameType(int(str(self.id)[5:6]))
