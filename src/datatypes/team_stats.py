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
    fo_wins: float
    giveaways: int
    takeaways: int
    pp_fraction: str
    periods: list[Period]
    shootout: Shootout
