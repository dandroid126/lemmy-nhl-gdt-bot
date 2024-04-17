import os
from typing import Final

SCRIPT_PATH: Final = os.path.realpath(__file__)
DIR_PATH: Final = f"{os.path.dirname(SCRIPT_PATH)}/../../"
OUT_PATH: Final = f"{DIR_PATH}/out/"
DB_PATH: Final = f"{OUT_PATH}/gdt_bot.db"
