from aiogram import Dispatcher
from aiogram.utils import executor
from loguru import logger

import settings
from bot_core.commands import set_default_commands
from bot_core.loader import dp
from database.database import engine, db_session
from database.models import *


async def startup(dp: Dispatcher) -> None:
    await set_default_commands(dp)

    Base.metadata.create_all(bind=engine)
    logger.info("Start bot")


async def shutdown(dp) -> None:
    await db_session.close()
    await settings.Config.storage.close()
    logger.info("bot finished")


if __name__ == "__main__":
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=startup,
        on_shutdown=shutdown,
    )
