import sqlite3
from sqlite3 import Error

from src.utils import logger

global connection
global cursor

TAG = 'db_client.py'

# Keeping these here for reference, but don't use them because formatted strings in queries are bad.
# TABLE_POSTS = 'posts'
# COLUMN_POST_ID = 'post_id'
# COLUMN_GAME_ID = 'game_id'
# COLUMN_POST_TYPE = 'post_type'
#
# TABLE_DB_SCHEMA = 'db_schema'
# COLUMN_ROWID = 'rowid'
# COLUMN_VERSION = 'version'

POST_TYPE_GDT = 1
POST_TYPE_DDT = 2

DB_SCHEMA_VERSION = 1


def create_connection(path_to_db):
    global connection
    global cursor
    try:
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()
        logger.i(TAG, "Connection to SQLite DB successful")
    except Error as e:
        logger.e(TAG, "Error occurred", e)


def create_tables():
    global cursor
    logger.i(TAG, "create_tables: creating tables")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS posts(post_id INTEGER PRIMARY KEY NOT NULL, game_id INTEGER NOT NULL, post_type INTEGER NOT NULL)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS db_schema(rowid INTEGER PRIMARY KEY NOT NULL, version INTEGER NOT NULL)")


def get_post_id(game_id: int):
    global cursor
    query = "SELECT post_id FROM posts WHERE game_id=?"
    params = (game_id,)
    logger.i(TAG, f"get_post_id: executing {query} with params {params}")
    val = cursor.execute(query, params).fetchone()
    if val is not None:
        return val[0]
    return None


def insert_post(post_id: int, game_id: int, post_type: int):
    global cursor
    query = "INSERT INTO posts VALUES(?, ?, ?)"
    params = (post_id, game_id, post_type)
    logger.i(TAG, f"insert_post: executing {query} with params {params}")
    cursor.execute(query, params)
    connection.commit()
    return True


def set_db_schema_version(version: int):
    global cursor
    query = "INSERT OR REPLACE INTO db_schema VALUES(0, ?)"
    params = (version,)
    logger.i(TAG, f"set_db_schema_version: executing '{query}' with params '{params}")
    cursor.execute(query, params)
    connection.commit()
    return True


def get_db_schema_version():
    global cursor
    query = "SELECT version FROM db_schema WHERE rowid = '0'"
    logger.i(TAG, f"get_db_schema_version executing: {query}")
    try:
        val = cursor.execute(query).fetchone()
        if val is not None:
            return val[0]
    except sqlite3.OperationalError:
        logger.i(TAG, "get_db_schema_version: db_schema table not found. Assuming db_schema version is 0")
        return 0
    return 0


def upgrade_db_schema():
    from_version = get_db_schema_version()
    while from_version < DB_SCHEMA_VERSION:
        upgrade = {
            # When upgrading the db schema version, increase DB_SCHEMA_VERSION, then add a function here with what to do to upgrade to that version.
            # The key is the db schema version being upgraded to. The value is the name of the upgrade function. Do not add parentheses, or it will get executed every time.
            1: create_tables,
        }
        upgrade.get(from_version + 1, lambda: None)()
        from_version = from_version + 1
    set_db_schema_version(DB_SCHEMA_VERSION)


def initialize(db_path):
    create_connection(db_path)
    upgrade_db_schema()
