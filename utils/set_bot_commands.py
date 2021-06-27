from aiogram import types

from middlewares import _, __


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", _("Запустить бота")),
            types.BotCommand("Terms_of_Use", _("Умови використання")),
            types.BotCommand("Description_of_the_service", _("Опис послуги"))
        ]
    )
