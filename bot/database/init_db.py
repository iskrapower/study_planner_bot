import asyncio

from bot.database.database import engine
from bot.database.models import Base



async def init_db():

    async with engine.begin() as conn:

        await conn.run_sync(
            Base.metadata.create_all
        )



asyncio.run(init_db())