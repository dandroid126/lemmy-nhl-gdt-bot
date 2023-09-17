from dataclasses import dataclass

from src.datatypes.teams import Team


@dataclass
class Goal:
    period: str
    time: str
    team: Team
    strength: str
    goalie: str
    description: str
