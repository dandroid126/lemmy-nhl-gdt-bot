from src import constants
from src.datatypes.game import Game


def get_title(game: Game):
    return f"[GDT] {game.away_team} at {game.home_team} - {game.start_time.astimezone(constants.EST).strftime(constants.START_TIME_FORMAT)}"

# TODO: dynamically create period goals table based on number of periods
def get_body(game: Game):
    return f"""
| Time Clock        |
|-------------------|
| {game.game_clock} |


| Teams            | 1st                                     | 2nd                                     | 3rd                                     | Total                        |
|------------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|------------------------------|
| {game.away_team} | {game.away_team_stats.periods[0].goals} | {game.away_team_stats.periods[1].goals} | {game.away_team_stats.periods[2].goals} | {game.away_team_stats.goals} |
| {game.home_team} | {game.home_team_stats.periods[0].goals} | {game.home_team_stats.periods[1].goals} | {game.home_team_stats.periods[2].goals} | {game.home_team_stats.goals} |

| Team             | Shots                        | Hits                        | Blocked                        | FO Wins                         | Giveaways                        | Takeaways                        | Power Plays                                                             |
|------------------|------------------------------|-----------------------------|--------------------------------|---------------------------------|----------------------------------|----------------------------------|-------------------------------------------------------------------------|
| {game.away_team} | {game.away_team_stats.shots} | {game.away_team_stats.hits} | {game.away_team_stats.blocked} | {game.away_team_stats.fo_wins}% | {game.away_team_stats.giveaways} | {game.away_team_stats.takeaways} | {game.away_team_stats.pp_goals}/{game.away_team_stats.pp_opportunities} |
| {game.home_team} | {game.home_team_stats.shots} | {game.home_team_stats.hits} | {game.home_team_stats.blocked} | {game.home_team_stats.fo_wins}% | {game.home_team_stats.giveaways} | {game.home_team_stats.takeaways} | {game.home_team_stats.pp_goals}/{game.home_team_stats.pp_opportunities} |
"""
