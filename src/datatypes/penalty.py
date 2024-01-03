from dataclasses import dataclass

from src.datatypes.teams import Team


@dataclass
class Penalty:
    period: str
    time: str
    team: Team
    type: str
    min: int
    description: str
