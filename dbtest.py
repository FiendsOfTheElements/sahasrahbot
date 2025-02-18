import asyncio
import os
import urllib.parse

from dotenv import load_dotenv
from tortoise import Tortoise

from alttprbot.models import Tournaments

load_dotenv()

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = int(os.environ.get("DB_PORT", "3306"))
DB_NAME = os.environ.get("DB_NAME", "sahasrahbot")
DB_USER = os.environ.get("DB_USER", "user")
DB_PASS = urllib.parse.quote_plus(os.environ.get("DB_PASS", "pass"))

async def database():
    await Tortoise.init(
        db_url=f'mysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
        modules={'models': ['alttprbot.models']}
    )

loop = asyncio.get_event_loop()
dbtask = loop.create_task(database())
loop.run_until_complete(dbtask)
