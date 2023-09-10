import sqlite3
from sqlite3 import Error

from src import logger

global connection
global cursor

TAG = 'db_client.py'

TABLE_POSTS = 'posts'
COLUMN_POST_ID = 'post_id'
COLUMN_GAME_ID = 'game_id'


def create_connection(path_to_db):
    global connection
    global cursor
    try:
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()
        logger.d(TAG, "Connection to SQLite DB successful")
    except Error as e:
        logger.e(TAG, "Error occurred", e)


def create_tables():
    global cursor
    cursor.execute(
        f"CREATE TABLE IF NOT EXISTS posts({COLUMN_POST_ID} INTEGER PRIMARY KEY NOT NULL, {COLUMN_GAME_ID} INTEGER NOT NULL)")


def get_post_id(game_id: int):
    global cursor
    val = cursor.execute("SELECT post_id FROM posts WHERE game_id=?", (game_id,)).fetchone()
    if val is not None:
        return val[0]
    return None


def insert_row(post_id: int, game_id: int):
    global cursor
    s = f"INSERT INTO {TABLE_POSTS} ({COLUMN_POST_ID}, {COLUMN_GAME_ID}) VALUES({post_id}, {game_id})"
    logger.d(TAG, s)
    cursor.execute(f"INSERT INTO {TABLE_POSTS} ({COLUMN_POST_ID}, {COLUMN_GAME_ID}) VALUES({post_id}, {game_id})")
    connection.commit()


def initialize(db_path):
    create_connection(db_path)
    create_tables()
