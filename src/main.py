from typing import Optional

from src.datatypes.game import Game
from src.db.comments.comments_dao import comments_dao
from src.db.daily_threads.daily_threads_dao import daily_threads_dao
from src.db.daily_threads.daily_threads_record import DailyThreadsRecord
from src.db.game_day_threads.game_day_threads_dao import game_day_threads_dao
from src.utils import nhl_api_client, post_util, datetime_util, logger
from src.utils.environment_util import environment_util
from src.utils.lemmy_client import lemmy_client
from src.utils.signal_util import signal_util

TAG = "main"

DELAY_BETWEEN_UPDATING_POSTS = 30


def handle_daily_thread(games: list[Game]) -> Optional[DailyThreadsRecord]:
    if not games:
        logger.d(TAG, "List of games is empty. Exiting.")
        return None
    if not any(game.get_game_type() in environment_util.comment_post_types for game in games) and len(games) < 2:
        logger.d(TAG, "List of games is less than 2. Don't make a daily thread.")
        return None
    current_day_idlw = datetime_util.get_current_day_as_idlw()
    filtered_games = list(filter(lambda game: datetime_util.is_same_day(game.start_time, current_day_idlw) if game else None, games))
    if not filtered_games:
        logger.d(TAG, "No games today. Don't create a daily post.")
        return None
    daily_thread = daily_threads_dao.get_daily_thread(current_day_idlw)
    if daily_thread:
        # Update daily thread
        lemmy_client.update_daily_thread(daily_thread.post_id, post_util.get_daily_thread_title(current_day_idlw), post_util.get_daily_thread_body(filtered_games))
        return daily_thread
    # Unfeature all featured daily threads
    featured_daily_threads = daily_threads_dao.get_featured_daily_threads()
    for featured_daily_thread in featured_daily_threads:
        lemmy_client.unfeature_daily_thread(featured_daily_thread.post_id)
    # Create daily thread
    created_daily_thread = lemmy_client.create_daily_thread(current_day_idlw, post_util.get_daily_thread_title(current_day_idlw), post_util.get_daily_thread_body(filtered_games))
    lemmy_client.feature_daily_thread(created_daily_thread.post_id)
    return created_daily_thread


def handle_game_day_thread(game: Game):
    post = game_day_threads_dao.get_game_day_thread(game.id)
    post_id = post.post_id if post else None
    current_time = datetime_util.get_current_time_as_utc()
    if datetime_util.is_time_to_make_post(current_time, game.start_time, game.end_time):
        if post_id is not None:
            lemmy_client.update_game_day_thread(post_util.get_title(game), post_util.get_gdt_body(game), post_id)
        else:
            lemmy_client.create_game_day_thread(post_util.get_title(game), post_util.get_gdt_body(game), game.id)
    else:
        logger.i(TAG,f"main: The post was not created/updated for game '{game.id}' due to the time. current_time: {current_time}; start_time: {game.start_time}; end_time: {game.end_time}")


def handle_comment(daily_thread: DailyThreadsRecord, game: Game):
    if not game or not daily_thread:
        logger.d(TAG, f"Game or daily thread is None. Don't make a post. daily_thread is None: {daily_thread is None}, game is None: {game is None}")
        return
    comment = comments_dao.get_comment(game.id)
    comment_id = comment.comment_id if comment else None
    current_time = datetime_util.get_current_time_as_utc()
    if datetime_util.is_time_to_make_post(current_time, game.start_time, game.end_time):
        if comment_id is not None:
            lemmy_client.update_comment(comment_id, post_util.get_game_details(game))
        else:
            lemmy_client.create_comment(daily_thread.post_id, game.id, post_util.get_game_details(game))
    else:
        logger.i(TAG,f"main: The comment was not created/updated for game '{game.id}' due to the time. current_time: {current_time}; start_time: {game.start_time}; end_time: {game.end_time}")


def filter_games_by_selected_teams(games: list[Game]):
    return list(filter(lambda game: game.home_team in environment_util.teams or game.away_team in environment_util.teams if game else None, games))


def filter_games_by_start_time(games: list[Game]):
    current_time = datetime_util.get_current_time_as_utc()
    return list(filter(lambda game: datetime_util.is_time_to_make_post(current_time, game.start_time) if game else None, games))


def merge_games_with_schedule(schedule: list[Game], games: list[Game]):
    out = schedule.copy()
    for game in games:
        if not game:
            # Sometimes a game is empty, probably due to an error in the data returned by the API.
            # If that is the case, just skip it and leave it as a scheduled game.
            continue
        try:
            out[out.index(game)] = game
        except ValueError:
            logger.e(TAG, f"Index of game with id '{game.id}' not found in schedule")
    return out


def main():
    while not signal_util.is_interrupted:
        try:
            signal_util.wait(DELAY_BETWEEN_UPDATING_POSTS)
            if signal_util.is_interrupted:
                continue
            schedule = nhl_api_client.get_schedule(datetime_util.yesterday(), datetime_util.tomorrow())
            schedule_filtered_by_selected_teams = filter_games_by_selected_teams(schedule)
            if not schedule_filtered_by_selected_teams:
                continue
            schedule_filtered_by_start_times = filter_games_by_start_time(schedule_filtered_by_selected_teams)
            games = nhl_api_client.get_games(schedule_filtered_by_start_times)
            merged_schedule_and_games = merge_games_with_schedule(schedule_filtered_by_selected_teams, games)
            daily_thread = handle_daily_thread(merged_schedule_and_games)
            for game in games:
                try:
                    if game is None:
                        logger.d(TAG, "Game is None. Skip making a post for this game.")
                        continue
                    game_type = game.get_game_type()
                    if game_type in environment_util.gdt_post_types:
                        handle_game_day_thread(game)
                    elif game_type in environment_util.comment_post_types:
                        handle_comment(daily_thread, game)
                except InterruptedError as e:
                    # If an InterruptedError is raised while processing games,
                    #  we need to break out before the catch-all below catches it and does nothing.
                    logger.e(TAG, "main: An InterruptedError was raised while processing games.", e)
                    break
                except Exception as e:
                    logger.e(TAG, "main: Some exception occurred while processing a game.", e)
        except InterruptedError as e:
            logger.e(TAG, "main: An InterruptedError was raised while sleeping.", e)
    logger.i(TAG, f"main: Reached the end. Shutting down. is_interrupted: {signal_util.is_interrupted}")


if __name__ == "__main__":
    main()
