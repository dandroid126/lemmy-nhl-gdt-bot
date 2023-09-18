from dataclasses import dataclass


@dataclass
class Penalty:
    period: str
    time: str
    team: str
    type: str
    min: int
    description: str
