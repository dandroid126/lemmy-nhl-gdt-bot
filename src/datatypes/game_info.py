from dataclasses import dataclass


@dataclass
class GameInfo:
    current_period: str
    game_clock: str

    def is_game_started(self) -> bool:
        # TODO: get this from an API call
        return self.game_clock != '--'
