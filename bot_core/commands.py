from aiogram import Dispatcher
from aiogram import types


async def set_default_commands(dp: Dispatcher) -> None:
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Старт бота"),
            types.BotCommand("parse", "Старт парсинга"),
            types.BotCommand("settings", "Информация про параметры поиска"),
        ]
    )
