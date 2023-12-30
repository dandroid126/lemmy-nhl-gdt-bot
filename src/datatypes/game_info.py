from dataclasses import dataclass


@dataclass
class GameInfo:
    current_period: str
    game_clock: str

    def is_game_started(self) -> bool:
        """
        Checks if the game has started.

        Returns:
            bool: True if the game has started, False otherwise.
        """
        # Check if the game clock is not equal to '--'
        # TODO: get this from an API call
        return self.game_clock != '--'
