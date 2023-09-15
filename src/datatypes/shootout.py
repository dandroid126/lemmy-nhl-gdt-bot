from dataclasses import dataclass


@dataclass
class Shootout:
    scores: int
    attempts: int
    has_been_played: bool
