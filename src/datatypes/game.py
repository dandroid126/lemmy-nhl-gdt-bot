from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

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
    end_time: Optional[datetime]
    game_info: GameInfo
    away_team_stats: Optional[TeamStats]
    home_team_stats: Optional[TeamStats]
    goals: Optional[list[Goal]]
    penalties: Optional[list[Penalty]]

    # This gets the game type by retrieving the 6th character in the game id.
    # 1 -> preseason
    # 2 -> regular season
    # 3 -> postseason
    # 4 -> allstar
    def get_game_type(self):
        """
        Returns the game type based on the ID of the object.

        Returns:
            GameType: The game type.
        """
        # Extract the relevant part of the ID as a string
        id_str = str(self.id)[5:6]

        # Convert the string to an integer
        game_type_num = int(id_str)

        # Create a new GameType object with the converted integer
        game_type = GameType(game_type_num)

        return game_type

    def __eq__(self, other):
        """
        Check if two Game objects are equal.

        Args:
            other (object): The object to compare with.

        Returns:
            bool: True if the objects are equal, False otherwise.
        """
        if isinstance(other, Game):
            return self.id == other.id
        return False