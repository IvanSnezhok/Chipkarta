import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, Text, Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboards.default.keyboard import lang_button, passport_choice
from loader import dp, db
from middlewares import _, __


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        await db.add_user(
            full_name=message.from_user.full_name,
            username=message.from_user.username,
            telegram_id=message.from_user.id
        )
    except asyncpg.exceptions.UniqueViolationError:
        await db.select_user(telegram_id=message.from_user.id)
    await db.message(message.from_user.full_name, message.from_user.id, message.text, message.date)
    msg = await message.answer(__(f"Вітаю, {message.from_user.full_name}!"))
    msg1 = await message.answer(_("Оберіть зручну для вас мову!"), reply_markup=lang_button)
    await db.message("BOT", 10001, msg, message.date.time())
    await db.message("BOT", 10001, msg1, message.date.time())


@dp.message_handler(Text(["UA", "RU", "EN"]))
async def tel_info(message: types.Message):
    await db.set_lang(message.text.lower(), message.from_user.id)
    await db.message(message.from_user.full_name, message.from_user.id, message.text, message.date)
    msg = await message.answer(_("Тепер будь-ласка відправте свій номер телефона для зв`язку з вами"),
                         reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
                             [
                                 KeyboardButton(text="📱",
                                                request_contact=True)
                             ]
                         ], one_time_keyboard=True))
    await db.message("BOT", 10001, msg, message.date.time())


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def about_bot(message: types.Message):
    await db.update_phone_number(message.contact.phone_number, message.from_user.id)
    await db.message(message.from_user.full_name, message.from_user.id, message.text, message.date)
    msg = await message.answer(_("@chipkarta_bot - телеграм-бот для швидкого оформлення чіп-карти водія.\n"
                                 "Вартість послуги - 250 грн.\n"
                                 "Вартість держ. мита - 1970 грн.\n"
                                 "Оформлення - від 7 днів.\n"
                                 "Термін дії чіп-карти - 5 років.\n"
                                 "Оплата після оформлення документів.\n"
                                 "Використовуючи цей сервіс Ви даєте згоду на обробку персональних даних."),
                               reply_markup=passport_choice)
    await db.message("BOT", 10001, msg, message.date.time())


@dp.message_handler(Text(__("Главное меню")))
async def main_menu(message: types.Message):
    await db.message(message.from_user.full_name, message.from_user.id, message.text, message.date)
    msg = await message.answer(_("@chipkarta_bot - телеграм-бот для швидкого оформлення чіп-карти водія.\n"
                                 "Вартість послуги - 250 грн.\n"
                                 "Вартість держ. мита - 1970 грн.\n"
                                 "Оформлення - від 7 днів.\n"
                                 "Термін дії чіп-карти - 5 років.\n"
                                 "Оплата після оформлення документів.\n"
                                 "Використовуючи цей сервіс Ви даєте згоду на обробку персональних даних."),
                               reply_markup=passport_choice)
    await db.message("BOT", 1001, msg, message.date.time())
