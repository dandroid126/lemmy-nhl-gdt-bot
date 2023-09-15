from dataclasses import dataclass

from src.datatypes.period import Period
from src.datatypes.shootout import Shootout


# TODO: consider renaming this class and file
@dataclass
class TeamStats:
    goals: int
    shots: int
    blocked: int
    hits: int
    fo_wins: str
    giveaways: int
    takeaways: int
    pp_opportunities: int
    pp_goals: int
    pp_percentage: str
    periods: list[Period]
    shootout: Shootout
