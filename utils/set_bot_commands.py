from aiogram import types

from middlewares import _, __


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("terms_of_use", "Умови використання"),
            types.BotCommand("description_of_the_service", "Опис послуги")
        ]
    )
