from dataclasses import dataclass

from src.datatypes.period import Period


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
    pp_opportunities: int
    pp_goals: int
    pp_percentage: float
    periods: list[Period]
